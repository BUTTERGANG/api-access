"""Write READMEs for OH, MI, IL from probe results."""
import json, os

ROOT = "/home/alex/code/BUTTERGANG/api-access/data"

READMES = {
"OH": """# Ohio (OH)

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
""",
"MI": """# Michigan (MI)

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
""",
"IL": """# Illinois (IL)

## Transparency / spending
- **data.illinois.gov — LIVE Socrata** (catalog API verified). Main
  programmatic state source:
  `https://data.illinois.gov/api/catalog/v1?q=<term>&limit=10`
- **Illinois OpenBook** (openbook.illinoiscomptroller.gov) — reachable (200);
  ASP.NET app; export endpoints need form posts (TODO).
- IDOT bid-letting URL 404'd; IDOT procurement lives under
  idot.illinois.gov/doing-business — needs site nav (TODO).

## Chicago
- chicago.legistar.com returns the 19-byte wildcard stub → Chicago's council
  site is NOT classic Legistar hosting (or requires token). BUT:
- **data.cityofchicago.org — LIVE Socrata**, verified with a real resource pull
  (944 bytes from a dataset endpoint). Chicago's open data portal is one of
  the best in the country — permits, budgets, contracts, crimes. Use it as
  the primary Chicago source instead of Legistar.
- Cook County webapi also 500; `chicagoparkdistrict` IS a live Legistar
  client (200) — useful niche anchor.

## Meeting platforms (probed 2026-08)
| City | Hints | Notes |
|---|---|---|
| Chicago | — | use data.cityofchicago.org (Socrata) |
| Aurora | granicus | |
| Springfield | municode | |
| Naperville / Joliet / Rockford | none found | TODO deeper probe |

## Next steps
1. Catalog pulls from data.illinois.gov + data.cityofchicago.org.
2. IDOT letting index via site navigation.
3. Aurora Granicus ViewPublisher scrape.
""",
}

for st, md in READMES.items():
    with open(os.path.join(ROOT, st, "README.md"), "w") as f:
        f.write(md)
    print("wrote", st, "README")
