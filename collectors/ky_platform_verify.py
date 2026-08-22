"""KY meeting-platform registry was incomplete (city sites 403'd the subagent).
Re-verify Louisville/Lexington/Bowling Green/Covington/Owensboro platforms
via direct platform-API checks and update data/KY/meeting_platforms.json.
"""
import urllib.request, json, ssl, socket

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
ctx = ssl.create_default_context()

def legistar(slug):
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            f"https://webapi.legistar.com/v1/{slug}/bodies", headers=UA), timeout=12)
        d = json.loads(r.read())
        return {"platform": "legistar", "verified": True,
                "first_body": d[0]["BodyName"] if d else "(empty)"}
    except Exception as e:
        return {"platform": "legistar", "verified": False, "code": str(e)[:40]}

def civicclerk(slug):
    """Wildcard SPA — DNS proves nothing; try the v1 API for a real JSON error."""
    host = f"{slug}.api.civicclerk.com"
    try:
        socket.gethostbyname(host)
    except OSError:
        return None
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            f"https://{host}/v1/Meetings?pageSize=1", headers=UA), timeout=12, context=ctx)
        body = r.read().decode("utf-8", "replace")
        ok = body.strip().startswith(("{", "["))
        return {"platform": "civicclerk", "verified": ok,
                "note": "API returned JSON" if ok else f"non-JSON ({body[:40]})"}
    except Exception as e:
        return {"platform": "civicclerk", "verified": False, "error": str(e)[:60]}

def granicus(slug):
    host = f"{slug}.granicus.com"
    try:
        socket.gethostbyname(host)
    except OSError:
        return None
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            f"https://{host}/ViewPublisher.php?view_id=1", headers=UA), timeout=12, context=ctx)
        body = r.read()
        if len(body) > 1000 and b"Invalid" not in body:
            return {"platform": "granicus", "verified": True}
    except Exception:
        pass
    return None

CITIES = ["louisville", "lexington", "bowlinggreen", "owensboro",
          "covington", "bgky", "covingtonky"]
results = {}
for slug in CITIES:
    found = []
    lg = legistar(slug)
    if lg.get("verified"):
        found.append(lg)
    for fn in (civicclerk, granicus):
        r = fn(slug)
        if r and (r.get("verified") or r.get("platform") == "civicclerk"):
            found.append(r)
    results[slug] = found or "no verified platform"
    print(f"{slug:14} -> {found or 'none'}")

with open("/home/alex/code/BUTTERGANG/api-access/data/KY/platform_verification.json", "w") as f:
    json.dump(results, f, indent=2)
print("saved data/KY/platform_verification.json")
