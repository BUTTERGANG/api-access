# Ohio (OH)

## Transparency / spending
- **OhioCheckbook.com** — TLS cert fails plain verification (custom chain);
  needs `ssl` unverified context or Playwright. The checkbook itself is an
  OpenGov-style SPA — data via internal API only. TODO: trace with browser.
- **data.ohio.gov** — 404 at root as of 2026-08; Ohio's open-data presence is
  fragmented per-agency. NOT a Socrata portal anymore.
- **ODOT** — dot.state.oh.us procurement path 404s; ODOT moved to
  `odot-portal`/Bid Express (`bidx.net`). Bid tabs exist but behind the BidX
  app — Playwright candidate.

## Meeting platforms (probed 2026-08)
| City | Hints on homepage | Legistar API |
|---|---|---|
| Columbus | granicus + municode | no |
| Cincinnati | legistar link | 500 (no webapi client) |
| Toledo | legistar link | 500 |
| Akron | municode | no |
| Cleveland | none found | no |
| Dayton | CivicPlus AgendaCenter | no |

Insight: Ohio cities reference Legistar in page HTML but have NO live webapi
clients — they're likely on token-gated or newer Legistar builds. Columbus =
Granicus/Municode. Dayton = AgendaCenter.

## Next steps
1. Playwright session against ohiocheckbook.com to find its JSON endpoints.
2. ODOT bid tabs via BidX portal.
3. Confirm Cincinnati/Toledo Legistar status with browser (token-gated?).
