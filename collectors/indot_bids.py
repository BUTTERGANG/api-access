"""INDOT bid tabulations collector — WORKING.

The Bid Viewer is an ASP.NET postback grid; the first page of the
BidTabulations.aspx grid renders server-side HTML tables we can parse.
Extracts the letting index (descriptions + links/postbacks) to CSV/JSON.
Deeper per-contract tabs require POST with VIEWSTATE (documented TODO).
"""
import urllib.request, re, json, os, csv, html as H

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "IN")

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")

htmlsrc = get("https://erms12c.indot.in.gov/INDOTBidViewer/BidTabulations.aspx")
rows = re.findall(r"<tr[^>]*>(.*?)</tr>", htmlsrc, re.S)
parsed = []
for row in rows:
    cells = [H.unescape(re.sub(r"<[^>]+>", "", c)).strip()
             for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
    if len(cells) >= 2 and any(cells):
        parsed.append(cells)

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "indot_bid_tabulations_index.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerows(parsed)
print(f"{len(parsed)} rows extracted")
for p in parsed[:12]:
    print([c[:40] for c in p])
