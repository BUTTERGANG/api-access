"""Indiana Gateway unit report collector — WORKING.

Discovers units via geo_response.aspx autocomplete, then pulls the
unitreports_ajax.aspx HTML (report links per unit). Saves raw JSON/HTML
under data/IN/gateway/<unit_id>/.
"""
import urllib.request, urllib.parse, json, os, re, time, sys

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
BASE = "https://gateway.ifionline.org/report_builder/"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "IN", "gateway")

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")

UNITS = [
    "Indianapolis",   # Marion County
    "Carmel",         # Hamilton County
    "Fort Wayne",     # Allen County
    "Evansville",     # Vanderburgh
    "South Bend",     # St. Joseph
    "Fishers",
    "Noblesville",
]

def main():
    os.makedirs(OUT, exist_ok=True)
    index = []
    for name in UNITS:
        try:
            geo = json.loads(get(BASE + "geo_response.aspx?" +
                                 urllib.parse.urlencode({"term": name})))
        except Exception as e:
            print(name, "geo ERR", e); continue
        # take the first CIVIL CITY/TOWN result
        pick = next((g for g in geo if "CIVIL" in g["label"].upper()), geo[0] if geo else None)
        if not pick:
            print(name, "no results"); continue
        uid = pick["code1"]
        try:
            html = get(BASE + f"unitreports_ajax.aspx?unit_id={uid}")
        except Exception as e:
            print(pick["label"], "unitreports ERR", e); continue
        d = os.path.join(OUT, uid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "unit.html"), "w") as f:
            f.write(html)
        with open(os.path.join(d, "meta.json"), "w") as f:
            json.dump({"query": name, "id": uid, "label": pick["label"],
                       "url": BASE + f"unitreports_ajax.aspx?unit_id={uid}"}, f, indent=2)
        # extract report types offered
        rpts = sorted(set(re.findall(r'data-rpt="([^"]+)"', html)))
        index.append({"query": name, "id": uid, "label": pick["label"], "report_types": rpts})
        print(f"{pick['label']} (id {uid}): {len(rpts)} report types")
        time.sleep(1.5)
    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(index, f, indent=2)
    print("saved", len(index), "units -> data/IN/gateway/index.json")

if __name__ == "__main__":
    sys.exit(main())
