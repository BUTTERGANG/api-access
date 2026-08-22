"""TDOT bid letting index + first-batch downloader.

Crawls tn.gov TDOT construction bid-letting pages (year indexes -> per-letting
pages), records every letting and its document URLs, and downloads a first
batch (2026 lettings: ApparentBidResults.pdf + BidAuth.xlsx).

NOTE: plain urllib is reset by the tn.gov WAF; requests must use a browser-like
User-Agent via curl-equivalent headers (verified working).

Outputs:
  data/TN/tdot/tdot_lettings_index.json   full crawl index
  data/TN/tdot/<letting>/...              downloaded docs for first batch
  data/TN/tdot/download_log.csv           what was fetched, sizes
"""
import csv, json, os, re, subprocess, time

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
BASE = "https://www.tn.gov"
OUT = "/home/alex/code/BUTTERGANG/api-access/data/TN/tdot"
LET_ROOT = "/tdot/tdot-construction-division/bid-lettings"


def fetch_raw(url):
    r = subprocess.run(["curl", "-sS", "-A", UA, "--max-time", "60", url],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[:200])
    return r.stdout


def fetch(url):
    """HTML/text fetch -> str."""
    out = fetch_raw(url)
    return out.decode("utf-8", "replace")


def fetch_binary(url):
    """Binary fetch -> bytes."""
    return fetch_raw(url)


def main():
    os.makedirs(OUT, exist_ok=True)
    years = {}
    for year in range(2016, 2027):
        url = f"{BASE}{LET_ROOT}/{year}-bid-lettings.html"
        try:
            html = fetch(url)
        except Exception as e:
            print(year, "fetch failed:", e)
            continue
        lets = sorted(set(
            m.group(0) for m in re.finditer(
                rf"{LET_ROOT}/{year}-bid-lettings/[a-z0-9\-]+\.html", html.lower())))
        if lets or f"{year}-bid-lettings" in html.lower():
            years[year] = {"index_url": url, "n_lettings": len(lets),
                           "lettings": [l.replace(f"{LET_ROOT}/", "") for l in lets]}
    print({y: v["n_lettings"] for y, v in years.items()})

    # per-letting doc inventory (all years we indexed)
    index = []
    for year, yv in years.items():
        for rel in yv["lettings"]:
            path = f"{LET_ROOT}/{rel}"
            try:
                html = fetch(BASE + path)
                docs = sorted(set(m.group(1).replace("&amp;", "&")
                                  for m in re.finditer(
                                      'href="(/content/dam/tn/tdot/[^"]+)"', html)))
                index.append({"year": year, "page": path,
                              "docs": ["https://www.tn.gov" + d for d in docs]})
            except Exception as e:
                index.append({"year": year, "page": path, "error": str(e)})
            time.sleep(0.4)
    with open(f"{OUT}/tdot_lettings_index.json", "w") as f:
        json.dump(index, f, indent=2)
    n_docs = sum(len(e.get("docs", [])) for e in index)
    print(f"indexed {len(index)} lettings, {n_docs} doc links")

    # First batch: 2026 lettings -> apparent bid results PDF + bid auth xlsx
    log = []
    for e in index:
        if e["year"] != 2026 or "docs" not in e:
            continue
        name = e["page"].rsplit("/", 1)[-1].replace(".html", "")
        d = os.path.join(OUT, name)
        os.makedirs(d, exist_ok=True)
        for url in e["docs"]:
            fn = url.rsplit("/", 1)[-1]
            if not re.search(r"(ApparentBidResults|ContractAwards|SummaryOfBids)\.pdf|BidAuth\.xlsx|Call__.*\.xlsx",
                             fn, re.I):
                continue
            dest = os.path.join(d, fn)
            if os.path.exists(dest):
                continue
            try:
                data = fetch_binary(url.replace(" ", "%20"))
                open(dest, "wb").write(data)
                log.append([name, fn, len(data)])
                print("got", name, fn, len(data))
            except Exception as err:
                log.append([name, fn, f"ERROR {err}"])
            time.sleep(0.4)
    with open(f"{OUT}/download_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["letting", "file", "bytes"])
        w.writerows(log)
    ok = sum(1 for r in log if isinstance(r[2], int))
    print(f"downloaded {ok} files")


if __name__ == "__main__":
    main()
