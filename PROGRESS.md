# Progress Tracker

Machine-readable version: `PROGRESS.json` (update both).

**Next up (alphabetical):** first `todo` state after DC.

## Summary

| Status | Count | States |
|---|---|---|
| done | 4 | IN, KY, TN, WI |
| partial | 47 | AK, AL, AR, AZ, CA, CO, CT, DC, DE, FL, GA, HI, IA, ID, IL, KS, LA, MA, MD, ME, MI, MN, MO, MS, MT, NC, ND, NE, NH, NJ, NM, NV, NY, OH, OK, OR, PA, RI, SC, SD, TX, UT, VA, VT, WA, WV, WY |
| todo | 0 | — |

## Playbook per state

1. Transparency/spending portal — find API or bulk export; save sample to `data/<ST>/`
2. DOT bid lettings/tabs — index + first batch
3. City platform registry — top 5-6 cities, Legistar via webapi only
4. `data/<ST>/README.md` + update `PROGRESS.json` + this file

## Gotchas (see PROGRESS.json lessons)

- Legistar wildcard DNS — verify via webapi only
- 403 WAF sites → Playwright, don't fight
- Several states gzip-break plain urllib → use `curl --compressed` (see collectors/state_sweep.py)
- BidX (bidx.com/<state>/lettings) hosts DOT tabs for most states; needs free account or Playwright
