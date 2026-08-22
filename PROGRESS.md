# Progress Tracker

Machine-readable version: `PROGRESS.json` (update both).

**Next up (alphabetical): AL → AK → AZ → AR → CA**

## Summary

| Status | Count | States |
|---|---|---|
| done | 3 | IN, KY, TN, WI → *4* |
| partial | 3 | IL, MI, OH |
| todo | 44 | everything else |

## Per-state one-liners

- **IN** ✅ Gateway AJAX API + INDOT bids + 7 city platforms (no Legistar in IN)
- **KY** ✅ OpenDoor REST API (300 records) + KYTC lettings + Louisville/Lexington Legistar
- **TN** ✅ 117 TDOT lettings, 30 PDFs + Nashville Legistar
- **WI** ✅ 622 WisDOT contract IDs + Milwaukee/Madison/Racine Legistar
- **IL** 🔶 Socrata live (state + Chicago); IDOT + city platforms TODO
- **MI** 🔶 Socrata live; MDOT 403 (Playwright); platforms unverified
- **OH** 🔶 Everything behind browser walls — OhioCheckbook TLS, BidX, 404 portals
- All others: todo

## Playbook per state (in order)

1. Transparency/spending portal — find API or bulk export; save sample to `data/<ST>/`
2. DOT bid lettings/tabs — index + first batch
3. City platform registry — top 5-6 cities, Legistar via webapi only
4. `data/<ST>/README.md` + update `PROGRESS.json` + this file

## Gotchas (see PROGRESS.json lessons)

- Legistar wildcard DNS — verify via webapi only
- 403 WAF sites → Playwright, don't fight
- CivicClerk/Granicus subdomains can wildcard too
