"""WisDOT highway construction bid letting collector — WORKING.

Letting index pages live at
  https://wisconsindot.gov/Pages/doing-bus/contractors/hcci/bid-let/<YEAR>/<YYYYMMDD>..aspx
Each page lists per-contract plan/proposal PDFs plus letting-level
apparent-bids and all-bids-received PDFs. This extracts the letting +
contract index to CSV/JSON and downloads one sample xlsx (schedule of
items) and the all-bids PDF for the most recent past letting.
"""
import urllib.request, re, json, os, csv, ssl

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
BASE = "https://wisconsindot.gov"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "WI")
LET = BASE + "/Pages/doing-bus/contractors/hcci/bid-let/{y}/{d}.aspx"
YEAR_IDX = BASE + "/Pages/doing-bus/contractors/hcci/bid-let-{y}.aspx"

def letting_dates(year):
    """Parse the year index page for actual letting-date pages."""
    try:
        html = get(YEAR_IDX.format(y=year))
    except Exception:
        return []
    return sorted(set(re.findall(rf"/hcci/bid-let/{year}/(\d{{8}})\.aspx", html)))

def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
    return b if binary else b.decode("utf-8", "replace")

def collect_year(year):
    records = []
    for d in letting_dates(year):
        url = LET.format(y=year, d=d)
        try:
            html = get(url)
        except Exception:
            continue
        letting = d
        links = re.findall(r'href="(/hccidocs/[^"]+)"[^>]*>([^<]*)', html)
        contracts = sorted({m.group(1) for u, _ in links
                            for m in [re.search(r"(202\d{5}\d{3})", u)]
                            if m and "plans-proposals" in u})
        rec = {"letting": letting, "url": url, "n_contracts": len(contracts),
               "contracts": contracts}
        for u, label in links:
            lab = label.strip().lower()
            if "apparent bid" in lab:
                rec["apparent_bids_pdf"] = BASE + u
            if "all bids" in lab:
                rec["all_bids_pdf"] = BASE + u
            if "schedule of items" in lab:
                rec["bid_items_xlsx"] = BASE + u
        records.append(rec)
        print(letting, len(contracts), "contracts",
              rec.get("all_bids_pdf", "-"))
    return records

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    recs = collect_year(2026) + collect_year(2025)
    with open(os.path.join(OUT, "wisdot_bid_lettings.json"), "w") as f:
        json.dump(recs, f, indent=2)
    with open(os.path.join(OUT, "wisdot_bid_lettings.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["letting", "n_contracts", "url", "all_bids_pdf", "apparent_bids_pdf"])
        for r in recs:
            w.writerow([r["letting"], r["n_contracts"], r["url"],
                        r.get("all_bids_pdf", ""), r.get("apparent_bids_pdf", "")])
    past = [r for r in recs if r["letting"] <= "202608" and r.get("bid_items_xlsx")]
    if past:
        s = past[-1]
        for key, name in [("bid_items_xlsx", "wisdot_sample_bid_items.xlsx"),
                          ("all_bids_pdf", "wisdot_sample_allbids.pdf")]:
            if s.get(key):
                b = get(s[key], binary=True)
                with open(os.path.join(OUT, name), "wb") as f:
                    f.write(b)
                print("sample:", name, len(b), "bytes")
    print(f"TOTAL: {len(recs)} lettings, "
          f"{sum(r['n_contracts'] for r in recs)} contracts indexed")
