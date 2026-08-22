"""ArcGIS Hub dataset collector — parameterized by host.

Usage:
  python3 collectors/arcgis_datasets.py                    # all live hubs
  python3 collectors/arcgis_datasets.py opendata.dc.gov 25 # one hub, N per category

For each hub: enumerate datasets via OGC items API, record metadata,
download CSV exports for high-value categories into data/<ST>/arcgis/.
"""
import subprocess, json, os, sys, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
ROOT = os.path.join(os.path.dirname(__file__), "..")
LIVE = json.load(open(os.path.join(ROOT, "data", "ARCGIS_HUB_INDEX.json")))

# state code per host (from the sweep)
HOST_STATE = {}
for st, hosts in LIVE.items():
    for h in (hosts or []):
        HOST_STATE[h["host"]] = st

def curl(url, timeout=25):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "--compressed", url],
                       capture_output=True, timeout=timeout + 10)
    return r.stdout.decode("utf-8", errors="replace")

CATEGORIES = ["budget", "permits", "property", "addresses", "boundaries",
              "transportation", "elections", "land use"]

def list_items(host, q=None, limit=100):
    url = f"https://{host}/api/search/v1/collections/dataset/items?limit={limit}"
    if q:
        url += f"&q={q}"
    body = curl(url)
    try:
        d = json.loads(body)
        return d.get("numberMatched", 0), d.get("features", [])
    except Exception:
        return 0, []

def collect(host, per_cat=10):
    st = HOST_STATE.get(host)
    outdir = os.path.join(ROOT, "data", st or "UNKNOWN", "arcgis")
    os.makedirs(outdir, exist_ok=True)
    index = {"host": host, "state": st, "categories": {}}
    total_dl = 0
    for cat in CATEGORIES:
        n, feats = list_items(host, q=cat, limit=per_cat)
        entries = []
        for f in feats[:per_cat]:
            props = f.get("properties", {})
            item_id = f.get("id") or props.get("id") or ""
            entry = {
                "id": item_id,
                "title": props.get("title", ""),
                "type": props.get("type"),
                "updated": props.get("updated"),
            }
            # find CSV export link if present
            links = f.get("links", []) or []
            for l in links:
                if l.get("rel") == "self":
                    entry["url"] = l.get("href", "")
            entries.append(entry)
        index["categories"][cat] = {"matched": n, "sampled": entries}
        print(f"  {host} [{cat}] matched={n} sampled={len(entries)}")
        time.sleep(0.5)
    fn = os.path.join(outdir, f"{host.replace('.', '_')}_index.json")
    with open(fn, "w") as f:
        json.dump(index, f, indent=2)
    return len(CATEGORIES)

def main():
    hosts = sys.argv[1:] if len(sys.argv) > 1 else [h["host"] for hs in LIVE.values() if hs for h in hs]
    seen = set()
    for host in hosts:
        if host in seen:
            continue
        seen.add(host)
        print(f"=== {host}")
        try:
            collect(host)
        except Exception as e:
            print("  ERR", str(e)[:80])

if __name__ == "__main__":
    main()
