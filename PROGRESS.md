# Progress Tracker

Machine-readable version: `PROGRESS.json` (update both).

**Status (2026-08):** all 51 jurisdictions probed. 4 done (full data), 47
partial (endpoints verified, bulk collection pending), 0 todo.

## Data inventory (verified)

- 217 collected files: 25 CSVs (14,639 rows), 21 PDFs, 13 XLSX, 101 JSON
- Discovery indexes: 24,414 Socrata/CKAN + 9,966 ArcGIS Hub datasets
- Verification: 10/10 spot-checks passed against live sources (2026-08)
  - KY OpenDoor confirmed genuine; live API holds **377k records** (we sampled 300)
  - WisDOT contract IDs 52/52 confirmed on live letting pages
- Known caveat: NC "county boundaries" CSV is a national file hosted on NC's
  hub — relabel before using in analysis

## Playbook per state

1. Transparency/spending portal — find API or bulk export; save sample to `data/<ST>/`
2. DOT bid lettings/tabs — index + first batch
3. City platform registry — top 5-6 cities, Legistar via webapi only
4. `data/<ST>/README.md` + update `PROGRESS.json` + this file

## Priorities from here

1. Bulk-pull: full KY OpenDoor 377k records; NYSDOT/PennDOT bid tabs; raise
   ArcGIS/Socrata download params
2. Playwright batch for WAF states (NH, SD, AZ) and BidX-hosted DOT tabs
3. Tyler/Accela permits — needs one manual account signup for OIDC token
   (see docs/TYLER_CIVIC_ACCESS.md)

## Gotchas (see PROGRESS.json lessons + docs/LESSONS_LEARNED.md)

- Legistar wildcard DNS — verify via webapi only
- Socrata catalog MUST filter `domains={host}` (else searches all portals)
- 403 WAF sites → Playwright (installed and working)
- gzip-breaking sites → `curl --compressed` (state_sweep.py pattern)
- BidX (bidx.com/<state>/lettings) hosts DOT tabs for most states
