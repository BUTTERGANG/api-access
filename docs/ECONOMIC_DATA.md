# Economic Data — collectors, sources, status

Goal: collect a very large volume of public economic data, then aggregate it
into cross-source insights (cost of living vs. debt burden vs. energy costs
vs. government spending, by state/metro).

## Sources & status (verified 2026-08-23)

| Source | What | Access | Collector | Status |
|---|---|---|---|---|
| BLS CPI v1 API | Cost of living: CPI national + metros (all items, shelter, energy, gasoline) | Keyless POST JSON (10yr window keyless) | `bls_cpi.py` | ✅ WORKING — 6 series pulled |
| USAspending v2 | Federal spending by state/month (contracts/grants/loans/direct) | Keyless POST | `usaspending_spending.py` | ✅ WORKING — IN FY2025 $207B/12mo |
| NY Fed HHDC | Household debt balances + delinquency rates by loan type (Equifax panel aggregates) | PDF download + pymupdf text extraction | `nyfed_household_debt.py` | ✅ WORKING — 4 quarterly reports |
| Census ACS 5yr | Income, home value, rent, poverty, tenure by state/county | **KEY REQUIRED** (2026: anonymous = "Missing Key" HTML) | `census_acs.py` | ⏳ needs CENSUS_API_KEY |
| FRED | Mortgage rates (PMMS), card delinquency/charge-off rates, revolving credit, GDP | KEY required (`FRED_API_KEY`) | `fred_series.py` | ⏳ needs key |
| EIA v2 | Gas/diesel retail prices, electricity $/kWh by state, natgas prices | KEY required (`EIA_API_KEY`, no anonymous tier) | `eia_prices.py` | ⏳ needs key |

## Keys to register (all free)
- EIA: https://www.eia.gov/opendata/register.php → `EIA_API_KEY`
- FRED: https://fredaccount.stlouisfed.org/apikeys → `FRED_API_KEY`
- Census: https://api.census.gov/data/key_signup.html → `CENSUS_API_KEY`
- BLS optional (raises limits): https://data.bls.gov/registrationEngine/

## Gotchas learned here
- BLS metro series IDs `CUURA311SA0` (NY), `CUURA322SA0` (LA), `CUURA411SA0`
  (Chicago) are DISCONTINUED / empty. Working metro series use S-size-class
  IDs like `CUURS49ASA0` (SF), `CUURS12ASA0` (Seattle), `CUURS35ASA0`.
  Keyless API also caps at a 10-year window.
- USAspending `/api/v1/search/spending_by_category/` and even the v2 variant
  return 404; working route is `/api/v2/search/spending_over_time/` with
  `group=month`. FY date ranges are Oct 1–Sep 30 (see FY_DATES in collector).
- NY Fed hhdc XLSX paths (`/medialibrary/interactives/householdcredit/data/xls/*`)
  return an HTML page regardless of quarter; only the PDF at `.../pdf/HHDC_<Y>Q<q>`
  is real. Future quarters return a small HTML stub (~95KB) — check size/page
  count before treating as valid.
- Census API now requires a key for ALL requests (used to allow low-volume
  anonymous).

## Insight composites this unlocks (once keys land)
- State-level: median income/rent/home value (ACS) × energy burden (EIA) ×
  gas prices (EIA) × federal spend per capita (USAspending)
- National trend: mortgage rate (FRED PMMS) vs. delinquency transitions (NY Fed)
- Credit stress dashboard: card delinquency/charge-off (FRED bank data) +
  household delinquency rates (NY Fed) + bankruptcies (NY Fed report text)

## Not available publicly (do not chase)
Individual consumer credit data (who specifically is past due) lives at the
credit bureaus under FCRA — no public source exists. All sources above are
legitimate aggregates or public records.
