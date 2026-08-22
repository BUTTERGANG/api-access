"""Federal collectors — all keyless:
  1. Federal Register: latest rules/notices (excellent JSON API)
  2. USGS earthquakes M4.5+ last 30 days
  3. NWS active weather alerts for Indiana
  4. data.gov CKAN dataset count sample
Saves to data/federal/.
"""
import urllib.request, json, os

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "federal")
os.makedirs(OUT, exist_ok=True)

def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

# 1. Federal Register
fr = get_json("https://www.federalregister.gov/api/v1/documents.json?per_page=20&order=newest&conditions%5Btype%5D%5B%5D=RULE")
docs = [{"title": d["title"], "agency": d["agencies"][0]["name"] if d.get("agencies") else "",
         "date": d["publication_date"], "url": d["html_url"]} for d in fr.get("results", [])]
json.dump(docs, open(f"{OUT}/federal_register_latest.json", "w"), indent=2)
print("Federal Register:", len(docs), "latest rules")

# 2. USGS earthquakes
eq = get_json("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=4.5&orderby=time")
feats = eq.get("features", [])
json.dump({"count": len(feats), "latest": [
    {"mag": f["properties"]["mag"], "place": f["properties"]["place"],
     "time": f["properties"]["time"]} for f in feats[:10]]},
    open(f"{OUT}/usgs_earthquakes.json", "w"), indent=2)
print("USGS quakes:", len(feats))

# 3. NWS Indiana alerts
al = get_json("https://api.weather.gov/alerts/active?area=IN")
n = len(al.get("features", []))
json.dump({"count": n, "alerts": [f["properties"]["headline"] or f["properties"]["event"]
           for f in al.get("features", [])[:20]]},
    open(f"{OUT}/nws_indiana_alerts.json", "w"), indent=2)
print("NWS IN alerts:", n)

# 4. data.gov catalog count
ck = get_json("https://catalog.data.gov/api/3/action/package_search?q=indiana&rows=0")
cnt = ck["result"]["count"]
json.dump({"query": "indiana", "dataset_count": cnt}, open(f"{OUT}/datagov_indiana_count.json", "w"), indent=2)
print("data.gov 'indiana' datasets:", cnt)
