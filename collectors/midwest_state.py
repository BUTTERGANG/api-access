"""Generic Midwest state collector: transparency portal probe + city
meeting-platform fingerprint + Legistar API verification.

Usage: python3 collectors/midwest_state.py OH|MI|IL
Writes: data/<ST>/probe_results.json, meeting_platforms.json, README.md (skeleton)
"""
import urllib.request, urllib.error, ssl, json, os, socket, sys, time

UA = "api-access-collector/0.1 (alex@buttergang.dev)"
HDRS = {"User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"}
ctx = ssl.create_default_context()
ROOT = os.path.join(os.path.dirname(__file__), "..")

CITIES = {
    "OH": {"Columbus": "columbus.gov", "Cleveland": "clevelandohio.gov",
           "Cincinnati": "cincinnati-oh.gov", "Toledo": "toledo.oh.gov",
           "Akron": "akronohio.gov", "Dayton": "daytonohio.gov"},
    "MI": {"Detroit": "detroitmi.gov", "Grand Rapids": "grcity.us",
           "Ann Arbor": "a2gov.org", "Lansing": "lansingmi.gov",
           "Flint": "cityofflint.com", "Sterling Heights": "sterling-heights.net"},
    "IL": {"Chicago": "chicago.gov", "Aurora": "aurora-il.org",
           "Naperville": "naperville.il.us", "Joliet": "joliet.gov",
           "Rockford": "rockfordil.gov", "Springfield": "sprinf ill".replace(" ", ""), },
}
CITIES["IL"]["Springfield"] = "springfield.il.us"  # fix typo-safe

PLATFORMS = ["legistar", "granicus", "municode", "civicclerk", "agendacenter",
             "iqm2", "primegov", "civicweb", "novusagenda", "boarddocs"]

def get(url, timeout=20):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.status, r.read()

def probe_portal(name, url):
    try:
        status, body = get(url)
        return {"url": url, "status": status, "size": len(body),
                "note": "reachable"}
    except Exception as e:
        return {"url": url, "error": str(e)[:90]}

def legistar_live(slug):
    """Definitive check — wildcard DNS makes site checks useless."""
    try:
        status, body = get(f"https://webapi.legistar.com/v1/{slug}/bodies")
        data = json.loads(body.decode())
        first = data[0].get("BodyName") if data else "(empty)"
        return {"live": True, "first_body": first}
    except urllib.error.HTTPError as e:
        return {"live": False, "code": e.code}
    except Exception as e:
        return {"live": False, "error": str(e)[:60]}

def main(st):
    out = os.path.join(ROOT, "data", st)
    os.makedirs(out, exist_ok=True)

    portals = {
        "OH": [("OhioCheckbook", "https://ohiocheckbook.com/"),
               ("data.ohio.gov", "https://data.ohio.gov/"),
               ("ODOT bidding", "https://www.dot.state.oh.us/Divisions/Procurement/Pages/default.aspx")],
        "MI": [("data.michigan.gov", "https://data.michigan.gov/"),
               ("MI transparency", "https://www.michigan.gov/transparency"),
               ("MDOT bids", "https://www.michigan.gov/mdot/business/bidding")],
        "IL": [("Illinois OpenBook", "https://openbook.illinoiscomptroller.gov/"),
               ("data.illinois.gov", "https://data.illinois.gov/"),
               ("IDOT bids", "https://idot.illinois.gov/doing-business/procurements/bid-letting/index")],
    }[st]

    results = {"transparency_portals": {}}
    for name, url in portals:
        results["transparency_portals"][name] = probe_portal(name, url)
        print(name, "->", results["transparency_portals"][name])
        time.sleep(1)

    # Socrata liveness for the state data portal (DNS + HTTP)
    results["socrata"] = {}
    for cand in ["data.ohio.gov", "data.michigan.gov", "data.illinois.gov"]:
        try:
            status, body = get(f"https://{cand}/", timeout=15)
            results["socrata"][cand] = {"status": status, "size": len(body)}
        except Exception as e:
            results["socrata"][cand] = {"error": str(e)[:90]}
    print("socrata:", results["socrata"])

    mp = {}
    for city, domain in CITIES[st].items():
        entry = {"domain": domain, "portal_hints": []}
        try:
            _, html = get(f"https://{domain}/")
            low = html.decode("utf-8", "replace").lower()
            entry["portal_hints"] = [p for p in PLATFORMS if p in low]
        except Exception as e:
            entry["error"] = str(e)[:90]
        slug = city.lower().replace(" ", "")
        lv = legistar_live(slug)
        if lv.get("live"):
            entry["legistar"] = lv
        mp[city] = entry
        print(city, "->", entry.get("portal_hints"), "| legistar:", lv)
        time.sleep(1)

    with open(os.path.join(out, "meeting_platforms.json"), "w") as f:
        json.dump(mp, f, indent=2)
    with open(os.path.join(out, "probe_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("saved probes -> data/%s/" % st)

if __name__ == "__main__":
    main(sys.argv[1].upper())
