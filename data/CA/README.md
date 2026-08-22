# California (CA)

## Open data — excellent
- **data.ca.gov is a LIVE CKAN portal** (not Socrata): verified with
  `/api/3/action/package_search?q=transportation` → 181 datasets. Full CKAN
  API available (`/api/3/action/...`).
- **data.lacity.org — LIVE Socrata** (catalog API returns results).

## DOT bids
- Caltrans procurement page live (23KB) — structure TODO; Caltrans uses
  BidX-style e-bidding (https://dot.ca.gov → "Contract Advertisements").

## Meeting platforms — strong Legistar state
| City | Finding |
|---|---|
| **San Jose** | ✅ LIVE Legistar ("City Council") |
| **Fresno** | ✅ LIVE Legistar ("City Council") |
| San Diego | Granicus hint on homepage |
| Los Angeles | city council on its own Legistar clone (`losangeles.legistar.com` — webapi slug `la` errors, needs token per NYC pattern) |
| San Francisco | live site; SF Board of Supervisors has own legislation system |

## Next steps
1. CKAN bulk pulls from data.ca.gov (rich state datasets).
2. San Diego Granicus ViewPublisher scrape.
3. LA Legistar token request (free, emailed).
4. Caltrans contract advertisements parse.
