"""Dataset discovery across all state portals.

For every live Socrata/CKAN/ArcGIS portal found in the sweep, query its
catalog API and record: total dataset count, top categories, and sample
high-value datasets (budgets, contracts, salaries, permits, crime).
Writes data/DATASET_INDEX.json.
"""
import subprocess, json, os, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
ROOT = os.path.join(os.path.dirname(__file__), "..")

def curl(url, timeout=20):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "--compressed", url],
                       capture_output=True, timeout=timeout + 10)
    return r.stdout.decode("utf-8", errors="replace")

SOCRATA = {
    "NY": ("data.ny.gov", None), "WA": ("data.wa.gov", None),
    "OR": ("data.oregon.gov", None), "PA": ("data.pa.gov", None),
    "TX": ("data.texas.gov", None), "NJ": ("data.nj.gov", None),
    "MD": ("data.maryland.gov", "opendata.maryland.gov"),
    "CO": ("data.colorado.gov", None), "CT": ("data.ct.gov", None),
    "MO": ("data.mo.gov", None), "DE": ("data.delaware.gov", None),
    "VT": ("data.vermont.gov", None),
}
CKAN = {"CA": "data.ca.gov"}
CITY_SOCRATA = {
    "IL-Chicago": "data.cityofchicago.org",
    "LA-NewOrleans": "data.nola.gov",
    "CA-LosAngeles": "data.lacity.org",
}
# ArcGIS Open Data portals (OGC search API)
ARCGIS = {"DC": "opendata.dc.gov"}

HIGH_VALUE_QUERIES = ["budget", "contracts", "salaries", "permits"]

def socrata_count(host, domain=None):
    """CRITICAL: catalog API searches ALL Socrata domains unless filtered
    with domains=<host>. Returns real per-domain count + category breakdown."""
    dom = domain or host
    counts = {}
    for q in ["budget", "contracts", "salaries", "permits", "crime",
              "education", "health", "transportation", "environment",
              "housing"]:
        body = curl(f"https://{host}/api/catalog/v1?q={q}&limit=1&domains={dom}")
        try:
            d = json.loads(body)
            counts[q] = int(d.get("resultSetSize") or 0)
        except Exception:
            pass
        time.sleep(0.3)
    body = curl(f"https://{host}/api/catalog/v1?limit=1&domains={dom}")
    try:
        total = int(json.loads(body).get("resultSetSize") or 0)
    except Exception:
        total = None
    return total, counts

def socrata_query(host, q):
    body = curl(f"https://{host}/api/catalog/v1?q={q}&limit=3&domains={host}")
    out = []
    try:
        d = json.loads(body)
        for r in d.get("results", [])[:3]:
            res = r.get("resource", {})
            out.append({"name": res.get("name"), "id": res.get("id"),
                        "category": res.get("category")})
    except Exception:
        pass
    return out

def ckan_count(host):
    body = curl(f"https://{host}/api/3/action/package_search?q=&rows=0")
    try:
        return json.loads(body)["result"]["count"]
    except Exception:
        return None

def arcgis_count(host):
    body = curl(f"https://{host}/api/search/v1/collections/dataset?limit=1")
    try:
        d = json.loads(body)
        m = d.get("numberMatched") or len(d.get("features", []))
        return m
    except Exception:
        return None

def main():
    index = {}
    for st, (host, domain) in SOCRATA.items():
        n, cat_counts = socrata_count(host, domain)
        samples = {}
        for q in HIGH_VALUE_QUERIES:
            samples[q] = socrata_query(host, q)
            time.sleep(0.4)
        index[f"{st} ({host})"] = {"platform": "socrata", "datasets": n,
                                   "category_counts": cat_counts,
                                   "high_value_samples": samples}
        print(f"{st:4} {host:26} top-category={n} counts={cat_counts}")
        time.sleep(0.5)

    for st, host in CKAN.items():
        n = ckan_count(host)
        index[f"{st} ({host})"] = {"platform": "ckan", "datasets": n}
        print(f"{st:4} {host:26} datasets={n}")

    for label, host in CITY_SOCRATA.items():
        n, cat_counts = socrata_count(host)
        samples = {q: socrata_query(host, q) for q in HIGH_VALUE_QUERIES[:2]}
        index[f"{label} ({host})"] = {"platform": "socrata-city",
                                      "datasets": n, "category_counts": cat_counts,
                                      "high_value_samples": samples}
        print(f"{label:18} datasets={n}")
        time.sleep(0.5)

    for st, host in ARCGIS.items():
        n = arcgis_count(host)
        index[f"{st} ({host})"] = {"platform": "arcgis", "datasets": n}
        print(f"{st:4} {host:26} datasets={n}")

    with open(os.path.join(ROOT, "data", "DATASET_INDEX.json"), "w") as f:
        json.dump(index, f, indent=2)
    total = sum(v["datasets"] or 0 for v in index.values())
    print(f"\nTOTAL discoverable datasets across live portals: {total:,}")
    print("saved -> data/DATASET_INDEX.json")

if __name__ == "__main__":
    main()
