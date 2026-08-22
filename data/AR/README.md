# Arkansas (AR)

## Transparency / spending
- **transparency.arkansas.gov** — live (20KB). Sections: payments to
  cities/counties, state contracts with vendors, employee compensation.
- Employee-comp data lives on `ark.org/dfa/transparency/employee_compensation.php`
  — a CSRF-token form app (`ina_sec_csrf` tokens) — scriptable but needs
  session handling. Financial disclosures at
  `financial-disclosures.sos.arkansas.gov` (Angular SPA `#/EthicsReports`,
  `#/lobbyistReports`) — API behind it TODO.
- No state Socrata.

## DOT bids
- ARDOT procurement 403s plain clients — Playwright candidate.

## Meeting platforms
| City | Finding |
|---|---|
| Little Rock | Municode hint |
| Fayetteville | Municode hint |
| Springdale | live, small homepage |
| Fort Smith | 403 WAF |

No Legistar clients verified for AR major cities.

## Next steps
1. Script the ark.org transparency forms (CSRF token flow).
2. Probe financial-disclosures SPA's backing API.
3. ARDOT via Playwright.
