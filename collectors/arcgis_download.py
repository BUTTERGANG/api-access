"""ArcGIS dataset downloader: pull actual records (JSON->CSV) from sampled
Feature Services in each hub's index.

ArcGIS REST pattern:
  {service_url}/query?where=1=1&outFields=*&resultRecordCount=N&f=json
f=csv is often unsupported; we fetch JSON and convert. Paginates via
exceededTransferLimit + resultOffset up to --max-rows.
"""
import subprocess, json, os, csv, sys, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
ROOT = os.path.join(os.path.dirname(__file__), "..")

def curl_json(url, timeout=60):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "--compressed", url],
                       capture_output=True, timeout=timeout + 10)
    try:
        return json.loads(r.stdout.decode("utf-8", errors="replace"))
    except Exception:
        return None

def fetch_layer(service_url, max_rows, outfile):
    """Paginate a Feature Layer query into CSV."""
    offset = 0
    rows = []
    fields = None
    while offset < max_rows:
        url = (f"{service_url}/query?where=1%3D1&outFields=*"
               f"&resultRecordCount=1000&resultOffset={offset}&f=json")
        d = curl_json(url)
        if not d or "features" not in d:
            return False
        feats = d.get("features", [])
        if not feats:
            break
        if fields is None and feats:
            fields = list(feats[0]["attributes"].keys())
        for f in feats:
            rows.append([f["attributes"].get(k) for k in fields])
        if not d.get("exceededTransferLimit"):
            break
        offset += 1000
        time.sleep(0.4)
    if rows:
        with open(outfile, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(fields)
            w.writerows(rows[:max_rows])
        return len(rows)
    return 0

def main(per_hub=2, max_rows=5000):
    indexes = []
    for dirpath, _, files in os.walk(os.path.join(ROOT, "data")):
        for fn in files:
            if fn.endswith("_index.json") and "arcgis" in dirpath:
                indexes.append(os.path.join(dirpath, fn))
    print(f"{len(indexes)} hub indexes found")
    grand = 0
    for idx_path in indexes:
        idx = json.load(open(idx_path))
        host = idx["host"]
        outdir = os.path.dirname(idx_path)
        downloaded = 0
        # pick top categories by match count, take per_hub datasets total
        picks = []
        for cat, c in sorted(idx["categories"].items(),
                             key=lambda kv: -kv[1]["matched"]):
            for s in c["sampled"]:
                picks.append((cat, s))
                if len(picks) >= per_hub:
                    break
            if len(picks) >= per_hub:
                break
        for cat, s in picks:
            detail_url = s.get("url")
            if not detail_url:
                continue
            # Some hubs return a Feature (geometry) for the bare item id —
            # the real dataset item has an "_N" layer suffix. Try as-is,
            # then _0.._9.
            detail = curl_json(detail_url)
            if not detail or not (detail.get("properties") or {}).get("url"):
                for suffix in range(10):
                    detail = curl_json(f"{detail_url}_{suffix}")
                    if detail and (detail.get("properties") or {}).get("url"):
                        break
            if not detail:
                continue
            svc = (detail.get("properties", {}) or {}).get("url", "")
            if not svc:
                continue
            # FeatureServer/MapServer roots need a layer id appended;
            # query the first layer from the service metadata.
            if svc.rstrip("/").split("/")[-1] in ("FeatureServer", "MapServer"):
                meta = curl_json(f"{svc}?f=json")
                layers = (meta or {}).get("layers", [])
                if not layers:
                    continue
                svc = f"{svc}/{layers[0]['id']}"
            title = "".join(ch if ch.isalnum() else "_" for ch in s["title"])[:60]
            outfile = os.path.join(outdir, f"{title}.csv")
            n = fetch_layer(svc, max_rows, outfile)
            if n:
                s["downloaded_csv"] = {"file": os.path.basename(outfile),
                                       "rows": n}
                downloaded += 1
                grand += n
                print(f"  {idx['state']} {s['title'][:40]:42} {n} rows -> {os.path.basename(outfile)}")
            time.sleep(0.5)
        with open(idx_path, "w") as f:
            json.dump(idx, f, indent=2)
        print(f"{host}: {downloaded} files")
    print(f"\nGRAND TOTAL: {grand} rows downloaded")

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2,
         int(sys.argv[2]) if len(sys.argv) > 2 else 5000)
