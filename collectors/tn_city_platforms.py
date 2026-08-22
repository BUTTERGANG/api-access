"""TN city meeting-platform registry.

Probes the six largest TN cities' websites for meeting-platform fingerprints
and verifies Legistar clients through webapi.legistar.com (wildcard DNS makes
DNS checks useless). Output: data/TN/meeting_platforms.json
"""
import json, ssl, re, urllib.request

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
CTX = ssl.create_default_context()
OUT = "/home/alex/code/BUTTERGANG/api-access/data/TN"

CITIES = {
    "Nashville": "nashville.gov",
    "Memphis": "memphistn.gov",
    "Knoxville": "knoxvilletn.gov",
    "Chattanooga": "chattanooga.gov",
    "Clarksville": "cityofclarksville.com",
    "Murfreesboro": "murfreesborotn.gov",
}

FINGERPRINTS = {
    "legistar": r"legistar",
    "granicus": r"granicus",
    "civicclerk": r"civicclerk",
    "civicplus_agendacenter": r"AgendaCenter",
    "municode_meetings": r"municodemeetings|municode\.com.*agenda",
    "primegov": r"primegov",
    "novusagenda": r"novusagenda",
    "boarddocs": r"boarddocs",
    "iqm2": r"iqm2\.com",
}


def get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read()


def check_legistar(slug):
    """webapi check: 200 = live client, 500 = no such client."""
    try:
        body = get(f"https://webapi.legistar.com/v1/{slug}/bodies?$top=3")
        bodies = json.loads(body)
        return {"status": "live", "slug": slug,
                "bodies_sample_count": len(bodies),
                "bodies": [{"Id": b.get("BodyId"), "Name": b.get("BodyName")}
                           for b in bodies]}
    except Exception as e:
        code = getattr(e, "code", None)
        return {"status": "no-client" if code == 500 else "error", "detail": str(e)}


def main():
    reg = {}
    for city, domain in CITIES.items():
        entry = {"domain": domain, "portal_hints": [], "legistar": None}
        slug = domain.split(".")[0]
        # homepage fingerprint
        try:
            html = get(f"https://www.{domain}/").decode("utf-8", "replace").lower()
            for plat, pat in FINGERPRINTS.items():
                if re.search(pat, html):
                    entry["portal_hints"].append(plat)
        except Exception as e:
            entry["homepage_error"] = str(e)
        # verify legistar regardless of hint (hints miss JS-driven widgets)
        entry["legistar"] = check_legistar(slug)
        if entry["legistar"]["status"] != "live":
            for alt in (city.lower().replace(" ", ""), domain.split(".")[0] + "tn"):
                r = check_legistar(alt)
                if r["status"] == "live":
                    entry["legistar"] = r
                    break
        reg[city] = entry
        print(city, entry["portal_hints"], entry["legistar"]["status"])

    with open(f"{OUT}/meeting_platforms.json", "w") as f:
        json.dump(reg, f, indent=2)
    print("wrote meeting_platforms.json")


if __name__ == "__main__":
    main()
