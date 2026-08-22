"""Verify Wisconsin city Legistar slugs via webapi.legistar.com (wildcard
DNS means content check is mandatory) and probe granicus/civicclerk
variants for the rest. Writes data/WI/meeting_platforms.json.
"""
import urllib.request, ssl, json, os

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "WI")
CITIES = ["milwaukee", "madison", "greenbay", "kenosha", "racine", "appleton"]

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
            return r.status, r.read()
    except Exception as e:
        return None, repr(e)[:120].encode()

def legistar_client(slug):
    st, b = get(f"https://webapi.legistar.com/v1/{slug}/bodies?skip=0&top=100")
    if st == 200 and b and b'"' in b:
        try:
            bodies = json.loads(b)
            return {"platform": "legistar", "slug": slug,
                    "webapi": f"https://webapi.legistar.com/v1/{slug}/",
                    "calendar": f"https://{slug}.legistar.com/Calendar.aspx",
                    "bodies_count": len(bodies),
                    "sample_bodies": [x.get("BodyName") for x in bodies[:5]]}
        except Exception:
            return None
    return None

def alt_probe(slug):
    """Probe common alternative meeting platforms."""
    found = []
    for pat, url in [
        ("granicus", f"https://{slug}.granicus.com/ViewPublisher.php?view_id=1"),
        ("civicclerk", f"https://{slug}.civicclerk.com/web/home.aspx"),
        ("civicplus", f"https://{slug}.civicplus.com/"),
    ]:
        st, b = get(url)
        if st == 200 and len(b) > 1000 and b"Invalid parameters" not in b:
            found.append({"platform": pat, "slug": slug, "url": url})
    return found

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    registry, notes = [], []
    for c in CITIES:
        hit = legistar_client(c) or None
        if hit:
            print(f"LIVE legistar: {c} ({hit['bodies_count']} bodies)")
            registry.append(hit)
        else:
            alts = alt_probe(c)
            if alts:
                registry.extend(alts)
                print(f"LIVE alt: {c} -> {[a['platform'] for a in alts]}")
            else:
                print(f"NO platform found: {c}")
                notes.append({"city": c, "status": "no legistar/granicus/civicclerk hit; needs manual check"})
    with open(os.path.join(OUT, "meeting_platforms.json"), "w") as f:
        json.dump({"verified": registry, "unresolved": notes}, f, indent=2)
    print(f"\n{len(registry)} verified platforms, {len(notes)} unresolved")
