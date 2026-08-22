# Tennessee (TN) — collected data

Collected 2026-08-22. Collectors in `collectors/tn_*.py`.

## Files

| File | Source | Records |
|---|---|---|
| `tdot/tdot_lettings_index.json` | tn.gov TDOT construction bid-letting pages | 117 lettings (2016–2026), 1,510 doc links |
| `tdot/<letting>/` + `download_log.csv` | TDOT per-letting docs | 30 files downloaded (6 of 7 scheduled 2026 lettings × ApparentBidResults/ContractAwards/SummaryOfBids PDFs + BidAuth & Call xlsx); 7.3 MB. October 2, 2026 letting has no results posted yet |
| `meeting_platforms.json` | 6 largest cities probed | Nashville = Legistar (`nashville`, verified via webapi, 21 bodies); Clarksville hints CivicClerk; Memphis/Knoxville/Chattanooga/Murfreesboro = no Legistar client, platform TBD |
| `legistar_nashville_sample.json` | webapi.legistar.com/v1/nashville | 21 bodies + 5 most-recent events (Metropolitan Council et al., 2026-08-18) |
| `legistar_probe_raw.json` | webapi.legistar.com probes | raw per-slug probe output |
| `transparency_probe.json` | data.tn.gov / transparenttn | probe verdicts (see below) |

## Findings

- **data.tn.gov is not Socrata**: Apache 403 on `/`, 404 on
  `/api/catalog/v1` even with a browser UA. No state SODA API. City portals
  ARE Socrata: `data.nashville.gov`, `data.memphistn.gov`.
- **Transparent Tennessee** is at `tn.gov/transparenttn.html`
  (checkbook / contracts / interactive budget / local sections; PeopleSoft
  supplier-contract search on hub.edison.tn.gov).
- **Salary Search** (`salary.app.tn.gov/searchsalary`) is server-rendered and
  rejects plain GET/POST → Playwright candidate.
- **tn.gov WAF**: plain `urllib` gets connection-reset; browser-like
  User-Agent via curl works for HTML pages. All TN collectors use this.
- **TDOT structure**: year index pages → per-letting pages under
  `/tdot/tdot-construction-division/bid-lettings/{year}-bid-lettings/…`,
  each linking `/content/dam/tn/tdot/construction/...` docs
  (ApparentBidResults.pdf, SummaryOfBids.pdf, ContractAwards.pdf,
  BidAuth.xlsx, Call xlsx). No API; plain file downloads.

## Rerun

```
python3 collectors/tn_tdot_bids.py       # re-index lettings, download new 2026 docs
python3 collectors/tn_city_platforms.py  # re-probe city platforms + legistar slugs
python3 collectors/tn_transparency.py    # rewrite transparency probe verdicts
```
