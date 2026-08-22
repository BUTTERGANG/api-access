# Wisconsin (WI) Data Collectors

Collected 2026-08-22. User-Agent: `api-access-collector/0.1 (alex@buttergang.dev)`.
Scripts live in `collectors/` (`wisdot_bids.py`, `wi_openbook_probe.py`, `wi_legistar_registry.py`).

## WisDOT highway construction bid lettings — WORKING

- Source: `https://wisconsindot.gov/Pages/doing-bus/contractors/hcci/bid-let-{YEAR}.aspx`
  → per-letting pages `/hcci/bid-let/<YYYY>/<YYYYMMDD>.aspx` (second Tuesday monthly).
- Collector: `collectors/wisdot_bids.py` — parses year index → letting pages,
  extracts contract IDs (11-digit: letting date + 3-digit sequence) from
  plan/proposal links plus apparent-bids / all-bids-received / bid-items URLs.
- Output: `wisdot_bid_lettings.json`, `wisdot_bid_lettings.csv`,
  samples: `wisdot_sample_bid_items.xlsx` (498 KB), `wisdot_sample_allbids.pdf` (1.9 MB).
- **Records: 21 lettings (2025–2026), 622 contracts indexed.**
- Note: wisconsindot.gov serves fingerprinting JS (`x-bni-*` cookies); plain
  urllib worked during this run but may need Playwright if blocked later.
  Per-contract bid tabulation detail lives inside the all-bids PDFs (parsing TODO).

## OpenBook (DOA spending transparency) — PARTIAL

- Site: `openbook.wi.gov` (ASP.NET WebForms + Telerik). No public REST API
  (`/api` and `/swagger` are 404).
- Search/export runs through ASP.NET AJAX **PageMethods** JSON POSTs:
  `{Contracts|Expenditures}.aspx/SetSearchType` and `.../ExportWebService(
  UserControl, ExportType, FiscalYear, ComparisonYear, SearchType, SearchString,
  CategoryCode, AgencyCode, ObjectCode, ProviderCode, FundCode,
  ReferenceTransactionNumbers, TransactionNumber, SortField, SortAscending,
  SuppressAmountColumns)`. Endpoint accepts POSTs (HTTP 200) but returns the
  app's own validation error without correct enum values, which live inside
  ScriptResource bundles. **TODO:** trace real calls via Playwright and replay.
- Saved: `openbook_contracts_sample.html` (41 KB), `probe_results.json`.

## data.wi.gov (Socrata) — DEAD

- `data.wi.gov` does not resolve (NXDOMAIN confirmed via DoH as of 2026-08).
  The state Socrata portal appears retired; agency portals (DNR/DPI ArcGIS Hub)
  are the replacement candidates for a future collector.

## City meeting platforms — VERIFIED via webapi.legistar.com

`meeting_platforms.json` (6/6 cities resolved):

| City | Platform | API |
|---|---|---|
| Milwaukee | Legistar | `webapi.legistar.com/v1/milwaukee/` (191 bodies) |
| Madison | Legistar | `webapi.legistar.com/v1/madison/` (252 bodies) |
| Racine | Legistar | `webapi.legistar.com/v1/racine/` (47 bodies) |
| Green Bay | CivicClerk | `greenbay.civicclerk.com/web/home.aspx` |
| Kenosha | CivicClerk | `kenosha.civicclerk.com/web/home.aspx` |
| Appleton | CivicClerk | `appleton.civicclerk.com/web/home.aspx` |

Legistar slugs verified by fetching `/v1/{slug}/bodies` (wildcard DNS makes
content checks mandatory). CivicClerk hits verified by HTTP 200 + non-trivial body.

## Record counts

- WisDOT: 21 letting records, 622 contract IDs, 2 sample documents.
- Meeting platforms: 6 verified entries.
- OpenBook: probe report + 1 sample page; no bulk data extracted yet.
