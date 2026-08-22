"""Broader Indiana meeting-platform sweep: check each city's own website for
portal links (legistar/granicus/municode/civicclerk/agendacenter/iqm2) by
probing common subdomains AND searching city sites. Keep it DNS+HTTP based.
"""
import urllib.request, ssl, json, socket

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
ctx = ssl.create_default_context()

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode("utf-8", "replace")

def dns(host):
    try:
        socket.gethostbyname(host); return True
    except OSError:
        return False

# city official domains (common patterns)
CITY_SITES = {
    "Fort Wayne": "cityoffortwayne.org",
    "South Bend": "southbendin.gov",
    "Carmel": "carmel.in.gov",
    "Fishers": "fishersin.gov",
    "Noblesville": "noblesville.in.gov",
    "Muncie": "muncie.in.gov",
    "Bloomington": "bloomington.in.gov",
    "West Lafayette": "westlafayette.in.gov",
    "Lafayette": "lafayette.in.gov",
    "Anderson": "cityofanderson.net",
    "Kokomo": "cityofkokomo.org",
    "Gary": "gary.gov",
    "Hammond": "gohammond.com",
    "Greenwood": "greenwood.in.gov",
    "Terre Haute": "terrehaute.in.gov",
    "Evansville": "evansville.in.gov",
    "Indianapolis": "indy.gov",
}

results = {}
for city, domain in CITY_SITES.items():
    entry = {"domain": domain, "portal_hints": []}
    try:
        html = fetch(f"https://{domain}/")
        low = html.lower()
        for plat, needle in [
            ("legistar", "legistar"), ("granicus", "granicus"),
            ("municode", "municode"), ("civicclerk", "civicclerk"),
            ("agendacenter", "agendacenter"), ("iqm2", "iqm2"),
            ("primegov", "primegov"), ("civicweb", "civicweb"),
            ("novusagenda", "novusagenda"), ("boarddocs", "boarddocs"),
        ]:
            if needle in low:
                entry["portal_hints"].append(plat)
    except Exception as e:
        entry["error"] = str(e)[:80]
    results[city] = entry
    print(city, "->", entry.get("portal_hints") or entry.get("error", "?"))

with open("/home/alex/code/BUTTERGANG/api-access/data/IN/meeting_platforms.json", "w") as f:
    json.dump(results, f, indent=2)
print("saved meeting_platforms.json")
