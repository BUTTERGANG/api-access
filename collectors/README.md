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
