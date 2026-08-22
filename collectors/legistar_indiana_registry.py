"""Find Indiana's actual Legistar client slugs by probing the calendar
subdomains with real HTTP (the wildcard DNS means we must check content).
Legistar calendar pages for live clients return full HTML; wildcard returns
'Invalid parameters!' (19 bytes). Also probe granicus/civicclerk variants.
"""
import urllib.request, ssl, json

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
ctx = ssl.create_default_context()

def live(host_path):
    """True if the portal returns real content (>1000 bytes, no 'Invalid parameters')."""
    try:
        req = urllib.request.Request("https://" + host_path, headers=UA)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            body = r.read()
            return len(body) > 1000 and b"Invalid parameters" not in body
    except Exception:
        return False

cities = ["indianapolis", "fortwayne", "evansville", "southbend", "carmel",
          "fishers", "noblesville", "muncie", "gary", "hammond", "bloomington",
          "terrehaute", "lafayette", "westlafayette", "anderson", "greenwood",
          "kokomo", "indy", "marioncounty"]
found = []
for slug in cities:
    if live(f"{slug}.legistar.com/Calendar.aspx"):
        found.append(("legistar", slug))
        print(f"LIVE legistar: {slug}.legistar.com")
    if live(f"{slug}.granicus.com/ViewPublisher.php?view_id=1"):
        found.append(("granicus", slug))
        print(f"LIVE granicus: {slug}.granicus.com")

print("\nfound:", found)
with open("/home/alex/code/BUTTERGANG/api-access/data/IN/legistar_registry.json", "w") as f:
    json.dump([{"platform": p, "slug": s} for p, s in found], f, indent=2)
