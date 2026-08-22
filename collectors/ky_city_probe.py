"""Kentucky city meeting-platform probe (Louisville, Lexington, Bowling Green,
Owensboro, Covington).

Method mirrors city_site_probe.py (IN): fingerprint each city's homepage +
common meeting-page paths for platform needles, then verify any Legistar slug
against webapi.legistar.com/v1/{client}/bodies (200=live, 403=token required,
404/500=no such client). Legistar wildcard DNS resolves everything — never
trust DNS alone.

Output: data/KY/meeting_platforms.json
"""
import json, os, re, socket, ssl, urllib.request

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "KY")
ctx = ssl.create_default_context()

NEEDLES = [("legistar", "legistar"), ("granicus", "granicus"),
           ("municode", "municode"), ("civicclerk", "civicclerk"),
           ("agendacenter", "agendacenter"), ("iqm2", "iqm2"),
           ("primegov", "primegov"), ("civicweb", "civicweb"),
           ("novusagenda", "novusagenda"), ("boarddocs", "boarddocs")]

CITIES = {
    "Louisville": "louisvilleky.gov",
    "Lexington": "lexingtonky.gov",
    "Bowling Green": "bgky.org",
    "Owensboro": "owensboro.org",
    "Covington": "covingtonky.gov",
}

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode("utf-8", "replace")

def dns(host):
    try:
        socket.gethostbyname(host); return True
    except OSError:
        return False

def verify_legistar(client):
    url = f"https://webapi.legistar.com/v1/{client}/bodies?skip=0&top=1"
    try:
        body = fetch(url)
        return {"status": 200, "live": True, "sample": body[:300]}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "live": False}

def extract_legistar_slug(text):
    m = re.search(r"https?://([a-z0-9-]+)\.legistar\.com", text.lower())
    return m.group(1) if m else None

results = {}
for city, domain in CITIES.items():
    entry = {"domain": domain, "portal_hints": [], "urls_checked": []}
    paths = [f"https://{domain}/",
             f"https://{domain}/government/",
             f"https://{domain}/city-clerk/" ,
             f"https://{domain}/agenda/", f"https://{domain}/meetings/"]
    html_all = ""
    for u in paths:
        try:
            t = fetch(u)
            entry["urls_checked"].append(u)
            html_all += t.lower()
        except Exception:
            pass
    if not html_all:
        entry["error"] = "all paths failed (possible 403/bot-block)"
    else:
        entry["portal_hints"] = [p for p, n in NEEDLES if n in html_all]
        slug = extract_legistar_slug(html_all)
        if slug:
            entry["legistar_slug"] = slug
            entry["legistar_verify"] = verify_legistar(slug)
    # subdomain guesses regardless (recorded as unverified unless hinted)
    entry["subdomain_dns_guesses"] = {
        s: dns(f"{s}.granicus.com") for s in []} if False else {}
    results[city] = entry
    print(city, "->", entry.get("portal_hints") or entry.get("error", "?"))

# targeted granicus/municode guesses common for KY cities
guesses = {
    "louisville metrocouncil granicus": "louisville.granicus.com",
    "lexington granicus": "lexington.granicus.com",
    "bowling green granicus": "bowlinggreen.granicus.com",
    "owensboro granicus": "owensboro.granicus.com",
    "covington municode meetings": "covingtonky.municodemeetings.com",
    "bowling green civicclerk": "bgky.civicclerk.com",
    "covington civicclerk": "covingtonky.civicclerk.com",
}
# NOTE: *.civicclerk.com is a WILDCARD SPA — any slug serves the same shell
# (verified: zznotacity.civicclerk.com also 200s). DNS/HTTP presence is NOT
# proof of a client; api.civicclerk.com/v1/Events returns 404 for all slugs
# we tried, so civicclerk hits are recorded as UNVERIFIED.
extra = {}
for label, host in guesses.items():
    extra[label] = {"host": host, "dns_resolves": dns(host)}
    if dns(host):
        try:
            body = fetch(f"https://{host}/")
            extra[label]["http_status"] = 200
            low = body.lower()
            extra[label]["looks_live"] = ("viewer" in low or "agenda" in low or "meeting" in low)
        except Exception as e:
            extra[label]["http_status"] = getattr(e, "code", None) or f"error: {str(e)[:90]}"

# legistar webapi verification for plausible KY clients
for client in ["louisville", "lexington", "bowlinggreen", "owensboro", "covington"]:
    v = verify_legistar(client)
    results.setdefault("_legistar_webapi_checks", {})[client] = v
    print("legistar", client, "->", v["status"])

with open(os.path.join(OUT, "meeting_platforms.json"), "w") as f:
    json.dump({"cities": results, "subdomain_guesses": extra}, f, indent=2)
print("saved meeting_platforms.json")
