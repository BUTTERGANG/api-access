# Illinois (IL)

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
