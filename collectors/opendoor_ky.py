"""Kentucky OpenDoor transparency portal — API discovery + sample collector.

Findings (verified 2026-08):
- opendoor.ky.gov TIMES OUT from this network (connection timeout). The app
  now lives at https://secure2.kentucky.gov/OpenDoor/ (Angular 2 SPA) and the
  SharePoint front at transparency.ky.gov links to it.
- API base is host-root-relative: UrlHostNameService returns
  'https://secure2.kentucky.gov/' and services append
  'TransparencyWebApi/v1/...' — i.e.
  https://secure2.kentucky.gov/TransparencyWebApi/v1/<Endpoint>
- Endpoints (from app/spending/spending.service.js):
    SpendingAndVendorDetail   (?dataGroupingView=VendorView&requestYear=...)
    SpendingAndVendorDetail/Get
    SpendingListData          (?ListType=...&requestYear=...)
    SpendingVenderNameList    (?requestYear=..&vendorNameLookup=)
    SpendingDownload          (CSV export)
    SpendingVendorDetail(Extract)
  Common params: requestYear, branchCode, cabinetCode, departmentCode,
  classCode, objectCode, vendorName, beginDate, endDate, maxReturnRows,
  startingIndex.

Collects a first sample batch to data/KY/.
"""
import json, os, urllib.request, ssl

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
BASE = "https://secure2.kentucky.gov/TransparencyWebApi/v1"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "KY")
ctx = ssl.create_default_context()

def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        data = r.read()
        return data if binary else data.decode("utf-8", "replace")

def spend_url(view="VendorView", year="2025", maxrows=100, start=0, **kw):
    q = {
        "dataGroupingView": view, "requestYear": year, "branchCode": "",
        "cabinetCode": "", "departmentCode": "", "classCode": "",
        "objectCode": "", "vendorName": "", "beginDate": "", "endDate": "",
        "maxReturnRows": maxrows, "startingIndex": start,
    }
    q.update(kw)
    return BASE + "/SpendingAndVendorDetail?" + "&".join(f"{k}={v}" for k, v in q.items())

os.makedirs(OUT, exist_ok=True)

# 0) probe legacy host status for the record
probe = {"opendoor.ky.gov": "TIMEOUT (connection timed out; legacy/dead)",
         "secure2.kentucky.gov/OpenDoor/": "200 Angular SPA",
         "transparency.ky.gov": "200 SharePoint front-end"}
with open(os.path.join(OUT, "opendoor_probe.json"), "w") as f:
    json.dump(probe, f, indent=2)

# 1) dropdown list data (cabinets/departments for FY2025)
list_types = ["Branch", "Cabinet", "Department"]
for lt in list_types:
    try:
        d = json.loads(get(f"{BASE}/SpendingListData?ListType={lt}&requestYear=2025"
                           "&branchCode=&cabinetCode=&departmentCode=&classCode="
                           "&objectCode=&beginDate=&endDate="))
        n = len(d.get("spendingListDatas", d.get("listDatas", []))) or len(json.dumps(d))
        print("ListType", lt, "-> keys:", list(d)[:6])
        with open(os.path.join(OUT, f"opendoor_list_{lt.lower()}_2025.json"), "w") as f:
            json.dump(d, f, indent=2)
    except Exception as e:
        print("ListType", lt, "FAILED:", str(e)[:100])

# 2) paginated vendor-view spending rows, FY2025 — first 3 pages of 100
total = 0
pages = []
for page in range(3):
    url = spend_url(start=page * 100)
    d = json.loads(get(url))
    rows = d.get("spendingVendorDetails") or []
    pages.append(rows)
    total += len(rows)
    print(f"page {page}: {len(rows)} rows")
    if not rows:
        break

with open(os.path.join(OUT, "opendoor_spending_fy2025_sample.json"), "w") as f:
    json.dump({"source": BASE + "/SpendingAndVendorDetail",
               "view": "VendorView", "fiscal_year": "2025",
               "pages_collected": sum(bool(p) for p in pages),
               "record_count": total,
               "records": [r for p in pages for r in p]}, f, indent=2)
print("TOTAL spending records:", total)
