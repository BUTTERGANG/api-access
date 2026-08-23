# api-access — collectors

One script per source. All keyless unless noted. Run from repo root:

```
python3 collectors/gateway_units.py        # Indiana Gateway unit reports
python3 collectors/indot_bids.py           # INDOT bid tabulations index
python3 collectors/city_site_probe.py      # IN city meeting-platform registry
python3 collectors/federal.py              # Fed Register, USGS, NWS
python3 collectors/gen_state_index.py      # regenerate states/SOURCES.md
```

## Working collectors (verified output in data/)

| Script | Source | Output |
|---|---|---|
| `gateway_units.py` | Indiana Gateway Report Builder AJAX (`/report_builder/geo_response.aspx`, `unitreports_ajax.aspx?unit_id=`) | `data/IN/gateway/<unit_id>/` + index.json — 7 units, 53–65 report types each |
| `indot_bids.py` | INDOT Bid Viewer grid | `data/IN/indot_bid_tabulations_index.csv` (24 rows; deep tabs need VIEWSTATE POST — TODO) |
| `city_site_probe.py` + `city_site_probe2.py` | IN city homepages → platform fingerprint | `data/IN/meeting_platforms.json` |
| `opendoor_ky.py` | KY Transparency REST API (`secure2.kentucky.gov/TransparencyWebApi/v1/`) | `data/KY/opendoor_*` — 300-record FY2025 sample |
| `kytc_bids.py` | KYTC letting index + proposal/bid-tab PDFs | `data/KY/kytc_lettings_index.json`, `kytc_letting_details_batch1.*` |
| `ky_city_probe.py` | KY city meeting-platform registry (webapi-verified Legistar) | `data/KY/meeting_platforms.json` |
| `tn_tdot_bids.py` | TDOT bid-letting pages (browser-UA curl; tn.gov WAF resets urllib) | `data/TN/tdot/` — 117 lettings indexed, 30 docs downloaded |
| `tn_city_platforms.py` | TN 6-city platform probe + webapi.legistar.com verification | `data/TN/meeting_platforms.json`, `legistar_nashville_sample.json` |
| `tn_transparency.py` | TransparentTN / data.tn.gov verdicts | `data/TN/transparency_probe.json` |
| `federal.py` | Federal Register, USGS, NWS | `data/federal/*.json` |

## Findings encoded in the code

- **Legistar wildcard DNS trap**: `{anything}.legistar.com` resolves and returns
  a 19-byte "Invalid parameters!" — DNS checks are useless; verify via
  `webapi.legistar.com/v1/{client}/bodies` (200 = live client, 500 = no client,
  403 = token required e.g. NYC). Indiana has NO live Legistar clients among
  the 19 slugs probed — the state skews CivicPlus AgendaCenter / Municode /
  Granicus.
- **Gateway unit discovery**: autocomplete endpoint `geo_response.aspx?term=X`
  returns JSON with unit IDs covering every political subdivision (cities,
  towns, schools, libraries, nonprofits with contracts).
- **Gateway contract search** is an ASP.NET postback form — needs VIEWSTATE
  session handling to script (TODO).
- **data.gov CKAN API** (`catalog.data.gov/api/3/`) returns 404 — appears
  retired; use dataset search page or agency APIs directly.
- Several IN city sites (southbendin.gov, fishersin.gov, bloomington.in.gov,
  westlafayette.in.gov, terrehaute.in.gov) 403 plain HTTP clients → need
  Playwright probe (see equipment-price-scraper skill pattern).

## Conventions

- User-Agent: `api-access-collector/0.1 (alex@buttergang.dev)` — required
  etiquette for SEC/Census; be polite everywhere (sleep between calls).
- Raw output lands in `data/<STATE>/`; never hand-edit collected files.
- Each collector is idempotent and safe to cron.

## Sweep-era collectors (added after 50-state expansion)

| Script | Purpose |
|---|---|
| `state_sweep.py` | Generic per-state prober: portals + Socrata check + city platforms. `python3 collectors/state_sweep.py ST "Name" '{"City":"domain"}' "label\|url" ...` |
| `midwest_state.py` | OH/MI/IL probe variant |
| `dataset_index.py` | Enumerates datasets across all live Socrata/CKAN/ArcGIS portals → `data/DATASET_INDEX.json`. **Must pass `domains={host}` to Socrata catalog** |
| `arcgis_sweep.py` | Finds live ArcGIS Hub portals per state → `data/ARCGIS_HUB_INDEX.json` (11 live, 9,966 datasets) |
| `arcgis_datasets.py` | Per-hub category indexes → `data/<ST>/arcgis/` |
| `arcgis_download.py` | Downloads actual CSVs from ArcGIS FeatureServers (handles layer-id + `_N` suffix quirks). Params: `[per_hub] [max_rows]` |
| `update_progress.py` | Updates PROGRESS.json + regenerates PROGRESS.md summary |

### Verification results (2026-08)
10/10 spot-checks passed against live sources. Key finding: KY OpenDoor API
holds **377,039 spending records** — bulk pull is the top-priority quick win.
Caveat: NC county-boundaries CSV is a national file hosted on NC's hub.

## Economic data collectors
| Script | Source | Notes |
|---|---|---|
| `eia_prices.py` | EIA v2 API | gas/diesel/electricity/natgas; needs `EIA_API_KEY` |
| `fred_series.py` | FRED | mortgage rates, delinquencies, credit, CPI; needs `FRED_API_KEY` |
| `bls_cpi.py` | BLS v1 API | CPI national+metros, keyless |
| `census_acs.py` | Census ACS 5yr | income/home value/rent/poverty; needs `CENSUS_API_KEY` |
| `usaspending_spending.py` | USAspending v2 | federal $ by state/month, keyless |
| `nyfed_household_debt.py` | NY Fed HHDC | household debt + delinquency PDFs, keyless |

See docs/ECONOMIC_DATA.md for status and gotchas.
