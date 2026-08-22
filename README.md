# api-access

Central catalog of free (mostly government) APIs we can pull data from, with notes
on auth, rate limits, and **what insight each source gives us**. This is the
reference doc to open when designing a new project — before writing a single
scraper.

## Already in use across BUTTERGANG repos

| Source | Used in | What we pulled | Key needed |
|---|---|---|---|
| FRED (St. Louis Fed) | POLYBOT | CPI (CPIAUCSL), unemployment (UNRATE), GDP, Fed funds (FEDFUNDS), payrolls (PAYEMS) | Yes — free, fred.stlouisfed.org |
| Congress.gov API v3 | POLYBOT | Bill search, status, latest actions | Yes — free, api.congress.gov |
| BLS OEWS wage data | JOB-HUNTER | State-level occupational wages (bulk ZIP download, `oesm24st.zip`) | No |
| Manifold Markets | POLYBOT | Prediction-market probabilities | No |

> FRED and Congress keys are NOT currently in `~/.hermes/.env` — each project
> carried its own. Register once and store centrally when we build collectors.

---

## 1. Economic & Financial (highest insight-per-call)

### FRED — Federal Reserve Economic Data
- Base: `https://api.stlouisfed.org/fred/`
- Auth: free API key. Limits: 120 req/min.
- Endpoints: `/series/observations`, `/series/search`, `/category/series`, `/release/dates`
- **Insight:** every major macro series — inflation, employment, GDP, rates,
  housing starts, consumer sentiment, retail sales, state-level employment.
  Use for: market timing, pricing models, "is now a good time" features,
  wedding-industry health proxies (consumer discretionary spending).
- Example: `GET /fred/series/observations?series_id=CPIAUCSL&api_key=KEY&file_type=json`

### Treasury Fiscal Data
- Base: `https://api.fiscaldata.treasury.gov/services/api/fiscal_service/`
- Auth: none.
- **Insight:** federal spending by category/state, national debt, interest
  payments, daily Treasury statement, Treasury yield curve rates.
- Yield curve (`/v2/accounting/od/avg_interest_rates`) = recession-signal data.

### SEC EDGAR
- Base: `https://www.sec.gov/cgi-bin/browse-edgar`, full-text: `https://efts.sec.gov/LATEST/search-index?q=`
- Auth: none, but User-Agent with contact email required. 10 req/s.
- **Insight:** company filings, insider trades, 10-K/10-Q financials. Use for
  competitor research on public companies (e.g. HoneyBook competitors if public).

### USAspending
- Base: `https://api.usaspending.gov/api/v2/`
- Auth: none.
- **Insight:** every federal award, grant, and contract — who got government
  money, where, for what. Use for: B2G market research, competitor grant intel.

---

## 2. Labor & Demographics

### BLS (Bureau of Labor Statistics)
- Base: `https://api.bls.gov/public/api/v2/timeseries/data/`
- Auth: optional key (higher limits: 500/day vs 25/day).
- **Insight:** employment by industry (CES), unemployment by state/metro (LAUS),
  CPI detail (CPI-U by category), wage data (OES — we already bulk-download this).
  Use for: pricing local services, hiring-market analysis, JOB-HUNTER wage data.

### Census Bureau API
- Base: `https://api.census.gov/data/{year}/{dataset}`
- Auth: optional key (free, raises limits).
- Datasets: ACS (demographics/income/housing down to block group), Decennial,
  County Business Patterns (business counts by industry by county!), Nonemployer
  Statistics (self-employed by industry — direct competitor density data).
- **Insight:** for any wedding/local-services project: median income, household
  count, marriage rates (ACS), number of photography/venues businesses per county
  (CBP NAICS 5122/7213). This is the single best source for market sizing.

### BEA (Bureau of Economic Analysis)
- Base: `https://apps.bea.gov/api/data/`
- Auth: free key.
- **Insight:** regional GDP, personal income by metro/county, consumer spending
  by state. Market-sizing complement to Census.

---

## 3. Business & Industry

### County Business Patterns (via Census API — see above)
- NAICS-coded business establishment counts per county. **Direct competitor
  density maps** for any vertical we enter.

### SAM.gov (federal contract opportunities)
- Base: `https://api.sam.gov/`
- Auth: free key.
- **Insight:** live federal contracting opportunities + entity registrations.

### SBA
- Base: `https://api.sba.gov/` (licenses/permits by state, loans data)
- Auth: some endpoints keyless.
- **Insight:** what licenses a business needs per state — useful for
  business-recon and onboarding vendors.

---

## 4. Legal, Legislative & Regulatory

### Congress.gov API v3
- Base: `https://api.congress.gov/v3/`
- Auth: free key (api.congress.gov/sign-up). 5,000 req/hour.
- **Insight:** bills, amendments, votes, members, committees. Already used in
  POLYBOT. Use for: regulatory tracking affecting our industries (e.g. AI,
  photography drones, gig-work rules).

### Federal Register
- Base: `https://www.federalregister.gov/api/v1/`
- Auth: none.
- **Insight:** every federal rule/proposed rule/executive order as it happens.
  Early-warning system for regulatory changes. JSON, excellent API design.

### Court records: PACER (paid-ish), CourtListener (free)
- Base: `https://www.courtlistener.com/api/rest/v4/`
- **Insight:** federal case law, RECAP archive of PACER documents. Litigation
  research without PACER fees.

---

## 5. Weather, Environment & Geospatial

### NWS (National Weather Service)
- Base: `https://api.weather.gov/`
- Auth: none (be polite; set User-Agent).
- **Insight:** forecasts, alerts, historical observations. Use for: outdoor
  event planning (weddings!), weather-risk features.

### USGS
- Earthquakes: `https://earthquake.usgs.gov/fdsnws/event/1/query`
- Water: `https://api.waterdata.usgs.gov/`
- **Insight:** real-time sensor data nationwide; earthquake feeds are the
  canonical free streaming API for demos.

### EPA
- Base: `https://www.epa.gov/airdata` / AQS API
- Auth: free key.
- **Insight:** air quality by monitor, facility emissions, enforcement actions.

### FEMA
- Base: `https://www.fema.gov/api/open/v2/` (no auth) + Hazard Mitigation API
- **Insight:** disaster declarations, flood insurance claims by area —
  property-risk data for any real-estate-adjacent project.

---

## 6. Health & Food

### openFDA
- Base: `https://api.fda.gov/`
- Auth: none for low volume (240/min with key).
- **Insight:** drug recalls, adverse events, food recalls, device registrations.

### CDC / data.cdc.gov
- Base: Socrata API `https://data.cdc.gov/resource/{id}.json` — SODA query language
- Auth: optional app token.
- **Insight:** mortality, vaccination, disease surveillance by county.

### ClinicalTrials.gov
- Base: `https://clinicaltrials.gov/api/v2/`
- Auth: none.
- **Insight:** all registered US clinical trials.

---

## 7. Education

### College Scorecard
- Base: `https://api.data.gov/ed/collegescorecard/v1/schools`
- Auth: free api.data.gov key.
- **Insight:** every US college: cost, graduation rates, earnings by major.

### NCES
- Base: `https://api.data.gov/education/v1/` + bulk downloads
- **Insight:** school districts, enrollment, finances — for family-facing products.

---

## 8. Transport & Infrastructure

### NHTSA
- Base: `https://api.nhtsa.gov/` (recalls, complaints, VIN decode — keyless)
- **Insight:** VIN decoding + recall lookup. Great utility API.

### EIA (Energy Information Administration)
- Base: `https://api.eia.gov/v2/`
- Auth: free key.
- **Insight:** gas/electricity prices by state, energy production. Cost-of-living
  and logistics-cost signals.

### FCC
- Base: `https://opendata.fcc.gov/` (broadband maps, license search)
- **Insight:** broadband availability by address.

---

## 9. Cross-cutting gateways & catalogs

### api.data.gov
- One free key (`https://api.data.gov/signup/`) covers 450+ APIs across 25
  agencies (FDA, DOE, ED, FCC, NHTSA, ...). Register once, reuse everywhere.

### Data.gov (CKAN)
- Base: `http://catalog.data.gov/api/3/` — metadata for 300k+ datasets.
- Auth: none. Use it to *discover* datasets, then hit the source API directly.

---

## 10. Financial market data (free tiers, no payment)

| Source | Auth | Free limits | What you get |
|---|---|---|---|
| **Finnhub** | free key, no card | 60 calls/min | Real-time quotes (US), fundamentals, earnings calendar, news sentiment, crypto/forex. Most generous free tier. |
| **Tiingo** | free key, no card | 1,000 req/day | Best free EOD price history (decades), clean REST, IEX real-time. Best for backtesting. |
| **Twelve Data** | free key | 800 req/day, 8/min | Stocks/FX/crypto time series, 120+ countries, technical indicators. |
| **Alpha Vantage** | free key | 25 req/day (5/min) | Quotes, 50+ technical indicators, fundamentals, forex, plus its own economic indicators (overlaps FRED). Small daily cap — use for low-volume reference pulls. |
| **Financial Modeling Prep (FMP)** | free key | 250 calls/day | 30+ years of financial statements/fundamentals — best free source of income/balance/cash-flow statements. |
| **Alpaca** | free key, no card | unlimited-ish | Free real-time IEX feed + paper trading API. Good for live prices without payment. |
| **SEC EDGAR / FRED / Treasury** | see above | free | Fundamentals, macro, yields — the zero-cost backbone. |

Practical stack: **Tiingo (history) + Finnhub (real-time + news) + FMP (fundamentals) + FRED/Treasury (macro)** — all free, all key-only registration, no credit card.

---

## 11. Local government / municipal (bids, council meetings, agendas)

This is where our municipality projects live. The big insight: **~80% of US
municipalities post meetings/bids through just four vendor platforms**, each
with predictable URL patterns — so one adapter per platform covers most cities.

### Meeting platforms (agendas, minutes, votes, video)
- **Legistar (Granicus)** — `https://webapi.legistar.com/v1/{client}/matters`, `/events`,
  `/eventitems/{id}/votes` — a genuine free OData REST API, no key. Cities: Chicago,
  Seattle, NYC, LA, most big cities. **Best-in-class; start here.**
- **Granicus** — `{slug}.granicus.com` video/agenda portals; some have APIs, rest scrape.
- **PrimeGov** — `{slug}.primegov.com` has JSON meeting endpoints.
- **CivicWeb / CivicClerk** — scrape-able portals.
- An Apify actor (`municipal-council-minutes-agenda-scraper`) already wraps all four —
  proof the adapter pattern works and reference for endpoint shapes.

### Bids & procurement (federal — free)
- **SAM.gov** — free API (open.gsa.gov/api) for all federal solicitations >$25k.
  Saved-search email alerts are free too. Federal only.
- **USAspending + FPDS** — who won what, at what price. Free.

### Bids & procurement (state/local — mostly paid, workarounds)
- The commercial aggregators (BidNet $500/mo, DemandStar $400/mo, GovWin
  $1,000+/mo, BidClerk $350/mo) are just reselling what agencies post for free
  on their own portals. The free path: **monitor agency portals directly** —
  PlanetBids (free vendor registration, CA/west), Public Purchase (free),
  InstantMarkets (free public search), state DOT bid lettings (all free),
  and city/county purchasing pages. A per-portal scraper set is the $0
  alternative to a $500/mo subscription.

---

## Reference repos studied

- public-api-lists/public-api-lists (★15.5k) — pattern: machine-readable JSON index
- marcelscruz/public-apis (★9.4k) — pattern: metadata table (auth/HTTPS/CORS)
- i-dot-ai/awesome-gov-datasets, makegov/awesome-procurement-data — domain deep-dives

## Conventions for collectors (future)

- One script per source under `collectors/<source>.py`, writing raw JSON to `data/<source>/`.
- Keys live in `~/.hermes/.env` (FRED_API_KEY, CONGRESS_API_KEY, API_DATA_GOV_KEY, ...).
- Always set a descriptive User-Agent with contact email (required by SEC/Census etiquette).
- Respect published rate limits; cache aggressively (see POLYBOT TTL pattern).
