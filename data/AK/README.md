# Alaska (AK)

## Transparency / spending
- No state Socrata portal (data.alaska.gov, data.ak.gov, data.soalaska.gov all dead).
- commerce.alaska.gov transparency portal redirects to a 770B shell — thin.
- Anchorage muni.org is live and substantial (112KB homepage).

## DOT bids
- **AKDOT&PF procurement** (`dot.alaska.gov/procurement/`) is live with real
  structure: `/procurement/bidding/results/`, `awp/bids.html`, current-bids SEF page.
- AK uses **Bid Express** (`bidx.com/ak/lettings`) — the standard BidX app;
  bid tab downloads need a (free) BidX account or Playwright.

## Meeting platforms
| City | Finding |
|---|---|
| Juneau | Municode + CivicClerk hints on homepage |
| Anchorage | live site; no platform hints found on homepage (muni uses separate systems) |
| Fairbanks | site unreachable |

No Legistar clients verified for AK cities.

## Next steps
1. Juneau CivicClerk slug verification via `{slug}.api.civicclerk.com/v1/Meetings`.
2. AKDOT results page deeper parse.
3. BidX free account for tab downloads (shared across all BidX states).
