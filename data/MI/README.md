# Michigan (MI)

## Transparency / spending
- **data.michigan.gov — LIVE Socrata** (595KB homepage, catalog API verified:
  `/api/catalog/v1?q=…` returns JSON). This is Michigan's main programmatic
  source. Query pattern:
  `https://data.michigan.gov/api/catalog/v1?q=<term>&limit=10`
- michigan.gov/transparency and MDOT bidding pages → 403 for plain HTTP
  clients (WAF). MDOT bid lettings are on michigan.gov/mdot — Playwright needed.

## Meeting platforms (probed 2026-08)
| City | Hints | Legistar API |
|---|---|---|
| Detroit | municode | no |
| Lansing | municode + civicclerk | no |
| Ann Arbor | legistar link | 500 (no webapi client) |
| Grand Rapids / Flint / Sterling Heights | none | no |

Insight: Michigan skews Municode/CivicClerk. Ann Arbor references Legistar but
no live API client — same token-gated pattern as Ohio cities.

## Next steps
1. Pull real datasets from data.michigan.gov Socrata (roads, budgets).
2. Playwright for MDOT bid lettings.
3. Verify Lansing CivicClerk slug via `{slug}.api.civicclerk.com/v1/Meetings`.
