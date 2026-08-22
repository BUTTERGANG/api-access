"""Generic state prober — the workhorse for the alphabetical 50-state sweep.

Usage: python3 collectors/state_sweep.py AK "Alaska" '{"Anchorage":"muni.org","Juneau":"juneau.org"}' \
    "https://data.alaska.gov/" "https://dot.alaska.gov/procurement"

For each state: probe transparency/data portals (incl. Socrata catalog check),
DOT bid pages, and city platform fingerprints + Legistar API verification.
Writes data/<ST>/probe_results.json. Idempotent.
"""
import subprocess, json, os, re, sys, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
ROOT = os.path.join(os.path.dirname(__file__), "..")
PLATFORMS = ["legistar", "granicus", "municode", "civicclerk",
             "agendacenter", "iqm2", "primegov", "civicweb", "boarddocs"]

def curl(url, timeout=25):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "--compressed", "-w", "\n__S__%{http_code}", url],
                       capture_output=True, timeout=timeout + 10)
    text = r.stdout.decode("utf-8", errors="replace")
    m = re.search(r"\n__S__(\d+)$", text)
    return (int(m.group(1)) if m else 0), (text[:m.start()] if m else "")

def legistar(slug):
    code, body = curl(f"https://webapi.legistar.com/v1/{slug}/bodies", timeout=15)
    try:
        d = json.loads(body)
        return {"platform": "legistar", "verified": True,
                "first_body": d[0]["BodyName"] if d else "(empty)"}
    except Exception:
        return None

def granicus_live(slug):
    code, body = curl(f"https://{slug}.granicus.com/ViewPublisher.php?view_id=1")
    if code == 200 and len(body) > 1000 and "Invalid" not in body:
        return {"platform": "granicus", "verified": True}
    return None

def socrata(host):
    """Check if a host is a live Socrata portal via its catalog API."""
    code, body = curl(f"https://{host}/api/catalog/v1?q=test&limit=1", timeout=15)
    if code == 200 and body.strip().startswith("{"):
        try:
            n = json.loads(body).get("resultSize", "?")
            return {"socrata": True, "resultSize": n}
        except Exception:
            return None
    return None

def main(st, name, cities_json, *portals):
    cities = json.loads(cities_json)
    out = os.path.join(ROOT, "data", st)
    os.makedirs(out, exist_ok=True)
    results = {"state": name}

    # portals: transparency + DOT
    tp = {}
    for label, url in [p.split("|", 1) for p in portals]:
        code, body = curl(url)
        hints = [pl for pl in PLATFORMS if pl in body.lower()] if code == 200 else []
        api_hint = bool(re.search(r'(api\.|/api/|\.json|socrata|arcgis)', body[:20000], re.I)) if code == 200 else False
        tp[label] = {"url": url, "status": code, "size": len(body),
                     "platform_hints": hints, "api_hints": api_hint}
        print(f"{label}: {code} {len(body)}B hints={hints} api={api_hint}")
        time.sleep(0.8)

    # Socrata candidates passed as portal labels containing 'socrata:'
    for label, url in [p.split("|", 1) for p in portals]:
        if "socrata" in label.lower():
            host = url.split("/")[2]
            r = socrata(host) or {"socrata": False}
            tp[label]["socrata_check"] = r
            print(" socrata:", host, r)

    # cities
    cr = {}
    for city, domain in cities.items():
        entry = {"domain": domain}
        code, body = curl(f"https://{domain}/")
        entry["status"] = code
        entry["size"] = len(body)
        if code == 200:
            low = body.lower()
            entry["hints"] = [p for p in PLATFORMS if p in low]
        slug = city.lower().replace(" ", "")
        lg = legistar(slug)
        if lg:
            entry["legistar"] = lg
        gr = granicus_live(slug)
        if gr:
            entry["granicus"] = gr
        cr[city] = entry
        print(city, code, len(body), entry.get("hints"), entry.get("legistar") or entry.get("granicus") or "")
        time.sleep(0.6)

    with open(os.path.join(out, "probe_results.json"), "w") as f:
        json.dump({"portals": tp, "cities": cr}, f, indent=2)
    print(f"saved -> data/{st}/probe_results.json")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], *sys.argv[4:])
