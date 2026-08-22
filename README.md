# api-access

Central catalog of free (mostly government) APIs plus working collectors and
collected data. Reference doc for designing new projects — what data exists,
how to get it, and what insight it gives.

## Repo layout

| Path | What it is |
|---|---|
| `README.md` | API catalog: 12 sections covering federal, financial, municipal, and all-50-state sources |
| `PROGRESS.json` / `PROGRESS.md` | State-by-state progress tracker (machine + human) |
| `states/SOURCES.md` | Per-state source index (transparency portals, DOT bids, meeting platforms) |
| `collectors/` | One script per source — see `collectors/README.md` |
| `data/<ST>/` | Collected raw data per state (+ `federal/`, `TYLER/`) |
| `data/DATASET_INDEX.json` | 24,414 Socrata/CKAN datasets indexed across 16 live portals |
| `data/ARCGIS_HUB_INDEX.json` | 9,966 ArcGIS Hub datasets across 11 jurisdictions |
| `docs/LESSONS_LEARNED.md` | Institutional memory: traps, gotchas, verification results |
| `docs/PLATFORM_LANDSCAPE.md` | Full vendor map beyond Socrata (Tyler, Accela, OpenGov, BoardDocs) |
| `docs/TYLER_CIVIC_ACCESS.md` | Tyler EnerGov architecture + API route map + OIDC blocker analysis |

## Current state of the data

**Status:** 4 states done (IN, KY, TN, WI), 47 partial, 0 todo — every state
has verified endpoints documented; "partial" = endpoints proven but bulk
collection not yet run.

### Data on disk (verified 2026-08)
- 217 files: 25 CSVs (14.6k rows), 21 PDFs, 13 XLSX, 101 JSON
- All spot-checked against live sources (10/10 verification pass):
  - KY OpenDoor spending sample confirmed genuine; live API holds **377k records**
  - WisDOT contract IDs 52/52 confirmed on live letting pages
  - Indiana Gateway unit reports byte-consistent with live
  - Legistar clients live-confirmed via webapi

### Discovery indexes (pullable on demand)
| Index | Count | Collector |
|---|---|---|
| Socrata/CKAN (13 states + 3 cities) | 24,414 datasets | `dataset_index.py` |
| ArcGIS Hubs (11 jurisdictions) | 9,966 datasets | `arcgis_sweep.py` |
| TN TDOT lettings | 117 lettings, 1,510 docs | `tn_tdot_bids.py` |

## Proven collection patterns

| Pattern | Collector | Notes |
|---|---|---|
| Socrata catalog + pulls | `dataset_index.py` | MUST filter `domains={host}` |
| CKAN package search | `dataset_index.py` | CA only so far |
| ArcGIS Hub OGC search → REST query | `arcgis_sweep.py`, `arcgis_datasets.py`, `arcgis_download.py` | handles layer-id + `_N` suffix quirks |
| State sweep (portals + cities) | `state_sweep.py`, `midwest_state.py` | parameterized by state |
| Indiana Gateway AJAX | `gateway_units.py` | geo_response + unitreports_ajax |
| INDOT bid tabs | `indot_bids.py` / `aldot_bids.py` | postback grid parsing |
| Legistar client registry | `legistar_indiana_registry.py`, `wi_legistar_registry.py` | webapi-only verification |

## Next steps (by value)

1. **Bulk-pull the big indexes**: full KY OpenDoor (377k records), raise
   ArcGIS/Socrata download params, NYSDOT/PennDOT bid-tab parses
2. **Playwright batch**: WAF-blocked sites (NH, SD, AZ, MDOT, ODOT/BidX,
   OhioCheckbook) — browser is installed and working
3. **Tyler/Accela permits**: needs one manual free account signup to capture
   an OIDC token; then thousands of tenants' permit data unlock
   (see `docs/TYLER_CIVIC_ACCESS.md`)
4. **BoardDocs school-board scraper** (thousands of districts nationwide)

## Conventions

- User-Agent: `api-access-collector/0.1 (alex@buttergang.dev)`
- Raw output lands in `data/<ST>/`; never hand-edit collected files
- Collectors are idempotent and cron-safe
- Every dataset claim must survive a disk/live-source check (see LESSONS_LEARNED §5)
