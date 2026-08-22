# Lessons Learned — api-access project

Living document. Add new lessons as we hit them; this is the institutional
memory that keeps us from re-scraping the same wall twice.

---

## 1. Platform identification

### Wildcard DNS is everywhere — never trust DNS checks
- `{anything}.legistar.com` resolves and returns a 19-byte "Invalid parameters!"
  page for non-clients. A DNS lookup or even HTTP 200 proves nothing.
- `*.api.civicclerk.com` serves a wildcard SPA — even `zznotacity` returns 200.
- **Verify via the platform's real API instead:**
  - Legistar: `webapi.legistar.com/v1/{slug}/bodies` → 200 = live client,
    500 = not a client, 403 = token-gated (NYC, LA).
- Indiana has ZERO Legistar clients despite being a big state; the coasts
  don't generalize.

### Socrata catalog searches ALL domains by default
- `https://data.ny.gov/api/catalog/v1?q=budget` without `domains=data.ny.gov`
  returns results from every Socrata portal on earth (capped at 10,000, so
  every state looked identical). Always pass `domains={host}`.
- Some portals serve under a different domain than the URL: Maryland's
  catalog lives under `opendata.maryland.gov`, not `data.maryland.gov`.
- resultSetSize caps at 10k — per-category queries give truer counts.

### Portal platforms migrate — yesterday's API may be gone
- data.wi.gov: DNS gone entirely.
- data.ok.gov, Iowa, Massachusetts, Hawaii: moved off Socrata to custom
  Next.js apps; old endpoints return HTML error pages instead of 404s.
- opendoor.ky.gov: legacy host dead; the live API moved to
  `secure2.kentucky.gov/TransparencyWebApi/v1/`.
- data.gov's CKAN catalog API returns 404 — even the federal aggregator decays.
- **Check liveness with a real query, not just a homepage fetch.**

---

## 2. HTTP mechanics

### Plain urllib breaks in three common ways
1. **gzip**: some gov sites return gzip regardless of Accept-Encoding →
   zero-byte or binary garbage bodies. Fix: `curl --compressed`.
2. **WAF/bot walls** (403): michigan.gov, tn.gov, louisvilleky.gov, most CT/
   SD cities, openbooks.az.gov. Don't fight with headers — use Playwright.
3. **Non-UTF8 bytes**: decode with `errors="replace"` or subprocess crashes
   mid-collection (Biloxi's site has cp1252 chars).

### ASP.NET postback apps need session archaeology
- Indiana Gateway contract search, WI OpenBook, IL OpenBook: VIEWSTATE /
  CSRF tokens / Telerik enums buried in JS bundles.
- Playbook: read the page's own `.js` files for AJAX endpoint paths and
  header names — the frontend code IS the API documentation.
- KY OpenDoor's REST API was found exactly this way (in the Angular app).

---

## 3. Endpoint archaeology (the meta-skill)

The SPA bundle files are the API docs governments won't publish:
- Tyler EnerGov: full route map extracted from `/apps/selfservice/app/energov`
  (`rootUrl="..."` definitions + `webApiBaseUrl + "..."` concatenations).
- Header names found by grepping bundles: `tenantId`, `Tyler-TenantUrl`,
  `Tyler-Tenant-Culture`.
- Search-payload field names from minified controller code
  (`searchCriteria.PageSize`, `PageNumber`, `ModuleId`, ...).
- Grep patterns that work: `rootUrl\s*=`, `webApiBaseUrl\s*\+`,
  `["\']([^"\']*(?:api|search)[^"\']*)["\']`, custom header prefixes
  (`X-...`, `Tyler-...`).

### ArcGIS Hub quirks
- `numberMatched` only appears on `/items`, not the collection endpoint.
- `q=*` matches nothing; use empty q or a real term.
- Dataset items may need `_0`..`_9` layer suffixes on their IDs.
- FeatureServer/MapServer roots must be resolved to a layer id before query.
- `f=csv` often unsupported → fetch JSON, convert yourself.

---

## 4. Vendor platforms = the real data moat

Modern portals are curated front pages. The systems of record hold everything:
- **Tyler Technologies**: permits/courts in all 50 states (4,953+ contracts).
  Public search gated behind Portico OIDC — anonymous token minting requires
  the interactive browser flow (see docs/TYLER_CIVIC_ACCESS.md).
- **Accela**: permitting system of record, 100+ agencies, CKAN-based civic
  data platform.
- **Granicus/Legistar/CivicClerk/PrimeGov/BoardDocs**: meeting records —
  ~80%+ of municipalities on a handful of platforms; one adapter each.
- One free account registration can unlock thousands of tenants' data —
  manual signup beats fighting OIDC programmatically.

---

## 5. Process lessons

### Sub-agents drift without hard guardrails
- Wave-1 agents either delivered excellently (KY/TN/WI) or died silently
  (empty responses); wave-2 agents invented unrelated projects entirely
  (built a barbell-price scraper when told "Ohio").
- Every subagent claim must be verified against disk: claims matched reality
  in only ~half of runs. Files exist? Row counts correct? Endpoints actually
  return what was claimed?
- For state-by-state sweeps, doing it inline with a parameterized collector
  (`state_sweep.py`) beat delegation.

### Verify everything, trust nothing
- The Legistar wildcard trap produced a fake "17/17 cities matched" result.
- Subagent reported "300 spending records" — true only after checking JSON.
- Magic-byte checks (`%PDF`, `PK`) catch corrupted downloads.

### Progress tracking
- PROGRESS.json (machine) + PROGRESS.md (human) updated at the end of every
  state run. Statuses: done > partial > todo > blocked. A state is "done"
  only with collected data on disk, not just verified endpoints.

---

## 6. Quick reference — verified live sources

| Source | Type | Access |
|---|---|---|
| Indiana Gateway Report Builder | AJAX JSON | keyless |
| Kentucky OpenDoor | REST v1 | keyless |
| INDOT / TN TDOT / WisDOT / NYSDOT / PennDOT bid tabs | HTML/PDF/XLSX | keyless |
| Federal Register, USGS, NWS | REST | keyless |
| 13 Socrata states + Chicago/NOLA/LA | SODA REST | keyless |
| California data.ca.gov | CKAN | keyless |
| 11 ArcGIS Hubs (AK AZ CA DC HI MD MI NC NJ NY UT) | OGC search | keyless |
| Legistar clients (~20 cities verified) | OData | keyless/token |
| CivicClerk hubs | REST | varies |

*Last updated: after ArcGIS CSV download wiring + Tyler prototype.*
