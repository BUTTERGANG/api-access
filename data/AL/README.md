# Alabama (AL)

## Transparency / spending
- **open.alabama.gov** — reachable (11KB homepage via curl with browser UA;
  plain urllib gets gzip-mangled 0-byte bodies — use `curl --compressed`).
  No obvious REST API on the landing page; deeper endpoint mapping TODO.
- **data.alabama.gov** — does not resolve. Alabama has no state Socrata portal.
- comptroller.alabama.gov — reachable; no API found yet.

## DOT bids — SOLVED
- The real portal is **`alletting.dot.state.al.us`** (found via "Letting
  Information" link on aldot.gov; dot.state.al.us BidTab pages are Page-Not-
  Found shells behind a Dynatrace bot-check).
- Structure: per-year bid tab indexes (`DW_Pages/Bid_Tabs/Bidtab_YYYY.html`,
  years back to **1996**!) → per-letting PDFs at `/BidTabs/bidtab_pdf/l<date>.pdf`.
- Also available: letting files (plans, proposals, addenda CBMPP calls) e.g.
  `DW_Pages/Letting_Files/2026/LettingFiles_082826.html`.
- Collected: `aldot/aldot_letting_data.json` (index links + Aug 28 2026 letting
  file list) and a real bid tab PDF sample: `aldot/lfeb2726.pdf` (1.9 MB).

## Meeting platforms (probed 2026-08)
| City | Finding |
|---|---|
| Huntsville | Municode code library only (no meetings platform found) |
| Mobile | Municode hint on homepage |
| Tuscaloosa | Granicus hint on homepage |
| Birmingham | city site live but council page has no platform links (agenda flow unclear) |
| Montgomery | 403 WAF — Playwright needed |

No Legistar clients verified for AL major cities.

## Next steps
1. Bulk-collect ALDOT bid tab PDFs by year index (1996→2026 archive is gold).
2. Tuscaloosa Granicus ViewPublisher scrape.
3. Montgomery/Birmingham via Playwright.
