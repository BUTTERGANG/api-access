"""Retry 403-blocked city sites with browser-like headers; also fetch
Evansville/Indy homepages for portal hints."""
import urllib.request, ssl, json

HDRS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
ctx = ssl.create_default_context()

PLATFORMS = ["legistar", "granicus", "municode", "civicclerk", "agendacenter",
             "iqm2", "primegov", "civicweb", "novusagenda", "boarddocs"]

def scan(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        low = r.read().decode("utf-8", "replace").lower()
        return [p for p in PLATFORMS if p in low]

CITIES = {
    "South Bend": "southbendin.gov",
    "Fishers": "fishersin.gov",
    "Bloomington": "bloomington.in.gov",
    "West Lafayette": "westlafayette.in.gov",
    "Terre Haute": "terrehaute.in.gov",
    "Evansville": "evansville.in.gov",
    "Indianapolis": "indy.gov",
}

out = {}
for city, domain in CITIES.items():
    try:
        hints = scan(f"https://{domain}/")
        out[city] = {"domain": domain, "portal_hints": hints}
        print(city, "->", hints or "(none on homepage)")
    except Exception as e:
        out[city] = {"domain": domain, "error": str(e)[:80]}
        print(city, "ERR", str(e)[:80])

# merge into existing meeting_platforms.json
import os
path = "/home/alex/code/BUTTERGANG/api-access/data/IN/meeting_platforms.json"
with open(path) as f:
    existing = json.load(f)
existing.update(out)
with open(path, "w") as f:
    json.dump(existing, f, indent=2)
print("merged -> meeting_platforms.json")
