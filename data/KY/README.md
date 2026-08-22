# Kentucky (KY) — collected data

Collectors: `collectors/opendoor_ky.py`, `collectors/kytc_bids.py`,
`collectors/ky_city_probe.py` (run from repo root). All verified with real
HTTP calls, 2026-08-22.

## 1) State transparency portal — OpenDoor / Transparency

- **`opendoor.ky.gov` is DEAD from this network** — connection timeout on
  every path. Do not use.
- The live app is an Angular SPA at `https://secure2.kentucky.gov/OpenDoor/`
  with SharePoint front at `https://transparency.ky.gov/`.
- **REST API (verified, keyless, JSON):**
  `https://secure2.kentucky.gov/TransparencyWebApi/v1/<Endpoint>`
  Endpoints found by reading `app/spending/spending.service.js` +
  `app/shared/UrlHostNameService.js`:
  - `SpendingAndVendorDetail?dataGroupingView=VendorView&requestYear=YYYY&...&maxReturnRows=N&startingIndex=N`
    (also `/Get`, views incl. BranchView/VendorView)
  - `SpendingListData?ListType=Branch|Cabinet|Department&requestYear=...`
    → returns fiscalYears, branches, cabinets, departments, classCodes, objectCodes
  - `SpendingVenderNameList?requestYear=..&vendorNameLookup=` (typeahead)
  - `SpendingDownload` / `SpendingVendorDetailExtract` (CSV bulk export)
  - Params: requestYear, branchCode, cabinetCode, departmentCode, classCode,
    objectCode, vendorName, beginDate, endDate, maxReturnRows, startingIndex.

Files: `opendoor_probe.json` (host status), `opendoor_list_*_2025.json`
(dropdown reference data), `opendoor_spending_fy2025_sample.json`
(**300 spending records** — 3 pages × 100 rows, VendorView FY2025).

## 2) KYTC bid lettings / bid tabs

SharePoint site; no HTML grid like INDOT — structured data ships as PDFs.

- Lettings calendar list: `transportation.ky.gov/construction-procurement/lists/lettings/lettings.aspx`
  → **15 letting dates** indexed (`kytc_lettings_index.json`).
- Per letting: `transportation.ky.gov/Construction-Procurement/Pages/Lettings.aspx?letting=M/D/YYYY`
  - proposal PDFs: `/Construction-Procurement/Proposals/*.pdf`
    (filename pattern `NNN-COUNTY-CID ... .pdf`; CID = `NN-NNNN`)
  - award results: `/Construction-Procurement/Archived%20Letting%20Results/LettingResults<date>.pdf`
  - unit price bid tabs: `/Construction-Procurement/Publications/<YYYY-MM-DD>/Unit%20Bid%20Tabulations.pdf`

Files: `kytc_letting_details_batch1.json/.csv` — batch of the 3 most recent
lettings (7/23/2026, 8/20/2026, 9/3/2026): **27 contract-ID rows**, 33
proposal PDF links. Sample PDFs in `kytc_bid_tabs/` (1 Unit Bid Tabulations
PDF, 112 KB). TODO: parse the bid-tab PDFs into tables; results-PDF URL 404s
for future-dated lettings (results only exist after the letting).

## 3) City meeting platforms

Verified via webapi (`webapi.legistar.com/v1/{client}/bodies`) and HTTP:

| City | Platform | Status |
|---|---|---|
| Louisville | **Legistar** client `louisville` | VERIFIED (webapi 200; Metro Council BodyId 138). Site louisvilleky.gov 403s plain clients → Playwright needed for site scraping |
| Louisville | Granicus video (`louisville.granicus.com`) | LIVE (200, viewer page) |
| Lexington | **Legistar** client `lexington` | VERIFIED (webapi 200; Urban County Council BodyId 138) |
| Bowling Green | CivicClerk (`bgky.civicclerk.com`) | UNVERIFIED — see wildcard note |
| Covington | CivicClerk (`covingtonky.civicclerk.com`) | UNVERIFIED — see wildcard note |
| Owensboro | Municode — code library only (`library.municode.com/ky/owensboro`); meetings via own site + livestreams page | no third-party agenda platform found |

File: `meeting_platforms.json`.

### Wildcard traps (both bite in KY)
- Legistar: any `{slug}.legistar.com` resolves → always verify through
  `webapi.legistar.com/v1/{slug}/bodies`. In KY both `louisville` and
  `lexington` are live; `bowlinggreen`, `owensboro`, `covington` are not (500).
- CivicClerk: any `{slug}.civicclerk.com` serves the same SPA shell (verified
  `zznotacity.civicclerk.com` returns 200). `{slug}.api.civicclerk.com/v1/Events`
  returned 404 for every slug tried — no verification path found yet.

## Insight notes

- Kentucky's transparency stack moved off opendoor.ky.gov to a clean,
  paginated REST API on secure2.kentucky.gov — better than expected; CSV bulk
  export endpoint exists but wasn't exercised (large).
- KYTC publishes everything as PDFs; per-contract award data requires PDF
  parsing, unlike INDOT's HTML grid.
- Louisville + Lexington both run Legistar → same collector shape as other
  Legistar states works out of the box.
