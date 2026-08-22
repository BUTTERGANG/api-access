"""KYTC bid letting / bid tabulation collector — WORKING.

transportation.ky.gov is SharePoint. Verified structure (2026-08):
- Lettings calendar list:
  /construction-procurement/lists/lettings/lettings.aspx
- Per-letting detail page:
  /Construction-Procurement/Pages/Lettings.aspx?letting=M/D/YYYY
  -> contains proposal PDFs (/Construction-Procurement/Proposals/*.pdf),
     letting results PDFs (/Construction-Procurement/Archived Letting Results/...),
     and Unit Bid Tabulations PDFs under
     /Construction-Procurement/Publications/<MM-DD-YYYY>/Unit%20Bid%20Tabulations.pdf
Bid tabs are PDFs (no HTML grid like INDOT); we index them + download samples.
"""
import csv, json, os, re, ssl, html as H, urllib.request, urllib.parse

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
ROOT = "https://transportation.ky.gov"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "KY")
PDFS = os.path.join(OUT, "kytc_bid_tabs")
ctx = ssl.create_default_context()

def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        data = r.read()
        return data if binary else data.decode("utf-8", "replace")

os.makedirs(PDFS, exist_ok=True)

# 1) letting index from the lettings list page
idx_html = get(f"{ROOT}/construction-procurement/lists/lettings/lettings.aspx")
lettings = sorted(set(H.unescape(m) for m in
                      re.findall(r"Lettings\.aspx\?letting=([^\"&]+)", idx_html)))
print(f"{len(lettings)} letting dates indexed")
with open(os.path.join(OUT, "kytc_lettings_index.json"), "w") as f:
    json.dump({"source": f"{ROOT}/construction-procurement/lists/lettings/lettings.aspx",
               "letting_dates": lettings, "count": len(lettings)}, f, indent=2)

# 2) detail pages for a first batch (most recent 3 lettings)
detail_recs = []
tab_pdfs, proposal_pdfs, results_pdfs = [], [], []
for letting in lettings[-3:]:
    url = f"{ROOT}/Construction-Procurement/Pages/Lettings.aspx?letting=" + \
          urllib.parse.quote(letting, safe="")
    h = get(url)
    links = [H.unescape(l) for l in re.findall(r'href="([^"]+\.pdf)"', h, re.I)]
    props = sorted(set(l for l in links if "/Proposals/" in l))
    tabs = sorted(set(l for l in links if "Unit%20Bid" in l or "Unit Bid" in l))
    results = sorted(set(l for l in links if "LettingResults" in l or "Archived" in l))
    # proposals look like "NNN-COUNTY-CID ... .pdf" -> parse contract ids
    cids = sorted(set(re.search(r"-(\d{2}-\d{4})", H.unescape(p)).group(1)
                      for p in props if re.search(r"-(\d{2}-\d{4})", p)))
    rec = {"letting_date": letting, "url": url, "proposal_count": len(props),
           "contract_ids": cids, "bid_tab_pdfs": tabs, "results_pdfs": results}
    detail_recs.append(rec)
    tab_pdfs += tabs; proposal_pdfs += props; results_pdfs += results
    print(letting, "->", len(props), "proposals,", len(cids), "contract IDs,", len(tabs), "bid-tab PDFs")

with open(os.path.join(OUT, "kytc_letting_details_batch1.json"), "w") as f:
    json.dump(detail_recs, f, indent=2)

# 3) download up to 2 Unit Bid Tabulations PDFs as structured-data samples
dl = []
for link in dict.fromkeys(tab_pdfs):
    if len(dl) >= 2:
        break
    full = urllib.parse.quote(ROOT + link, safe="/:%") if link.startswith("/") \
        else link
    name = re.sub(r"[^A-Za-z0-9._-]", "_", full.split("/")[-1])[:80]
    try:
        data = get(full, binary=True)
        with open(os.path.join(PDFS, name), "wb") as f:
            f.write(data)
        dl.append({"url": full, "file": f"data/KY/kytc_bid_tabs/{name}",
                   "bytes": len(data)})
        print("saved", name, len(data), "bytes")
    except Exception as e:
        print("download failed:", full[:90], str(e)[:80])

# also grab one letting-results PDF (award totals per contract)
if results_pdfs:
    link = results_pdfs[0]
    full = urllib.parse.quote(ROOT + link, safe="/:%") if link.startswith("/") \
        else link
    name = re.sub(r"[^A-Za-z0-9._-]", "_", full.split("/")[-1])[:80]
    try:
        data = get(full, binary=True)
        with open(os.path.join(PDFS, name), "wb") as f:
            f.write(data)
        dl.append({"url": full, "file": f"data/KY/kytc_bid_tabs/{name}",
                   "bytes": len(data)})
        print("saved", name, len(data), "bytes")
    except Exception as e:
        print("download failed:", full[:90], str(e)[:80])

with open(os.path.join(OUT, "kytc_pdf_samples.json"), "w") as f:
    json.dump(dl, f, indent=2)

# 4) flat CSV of the letting batch
with open(os.path.join(OUT, "kytc_letting_details_batch1.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["letting_date", "contract_id", "proposal_count"])
    for r in detail_recs:
        for cid in r["contract_ids"]:
            w.writerow([r["letting_date"], cid, r["proposal_count"]])
print("done:", sum(len(r["contract_ids"]) for r in detail_recs), "contract-id rows in CSV")
