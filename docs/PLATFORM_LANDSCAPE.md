# Beyond Socrata: the full landscape of government data platforms

Research findings on where data hides outside the Socrata ecosystem.
This is the map of "the rest of the iceberg" — most government data is NOT
on modern open-data portals.

## Platform taxonomy (what we've covered vs not)

| Platform family | Status | Where it lives | API quality |
|---|---|---|---|
| **Socrata** | ✅ indexed (13 states + 3 cities, 24k datasets) | data.<state>.gov | Excellent SODA REST |
| **CKAN** | ✅ CA indexed (4,569) | data.ca.gov, OpenGov-hosted portals | Good `/api/3/action/` |
| **ArcGIS Open Data (Esri)** | ⚠️ DC only so far | opendata.dc.gov, county GIS sites | OGC search + GeoJSON/CSV export |
| **OpenGov** (CKAN-based) | ❌ unexplored | Boston, ~100s of cities/counties | CKAN-compatible |
| **Accela Civic Data** | ❌ unexplored | permitting/licensing systems of record, 100+ agencies | CKAN-based civic platform |
| **Tyler Technologies** | ❌ unexplored | EnerGov/Civic Access — permits, courts; **4,953+ govt contracts**, all 50 states | Civic Access public portals scrapeable |
| **Granicus/Legistar** | ✅ meetings side done | agendas/votes | Legistar OData excellent |
| **Municode** | ⚠️ hints only | municipal codes + meetings | HTML/PDF |
| **CivicClerk / IQM2 / PrimeGov** | ⚠️ partial | meeting portals | REST endpoints exist |
| **BoardDocs** | ❌ unexplored | school boards nationwide | HTML/PDF |
| **Junar** | ❌ rare | Palo Alto, Sacramento County | REST |
| **Legacy ASP.NET transparency apps** | ⚠️ known (KY OpenDoor, WI OpenBook, IN Gateway) | comptroller/DFA sites | form-post archaeology |

## The big uncovered categories

### 1. Permitting & property records (Accela/Tyler EnerGov)
The single largest untapped source. Every building permit, code violation,
business license, and inspection flows through Accela or Tyler. Public-facing
portals:
- Tyler Civic Access: `{city}.selfservicetax.com` or
  `{city}-portal.tylertech.com` patterns — permit search is scrape-able
- Accela Citizen Access: `{agency}.accela.com/CitizenAccess/` pattern
- Accela's CKAN-based open-data platform exposes some agency data directly

**Insight:** permit volume = construction activity leading indicator;
code violations = property neglect signals; license issuances = new business
formation per city.

### 2. Court records (Tyler Courts — 22+ states)
Tyler runs court case management in 22+ states. Public case search portals
vary but are scriptable.

### 3. County property appraisers
Every county has one (often legacy ASP). Assessed values, sales, ownership.
ScrapingDome built a business on exactly this — proof it works at scale.

### 4. Esri/ArcGIS geoportals (huge and underused)
Most states ALSO run ArcGIS Hub sites we haven't checked — separate from any
Socrata portal. Check `{state}.arcgis.com` and `gis-<state>.gov` patterns.
DC verified working with the OGC search API (`/api/search/v1/collections/dataset`).

### 5. ERP/finance legacy systems
- PeopleSoft (TN supplier contracts), SAP, Workday vendor-payment extracts
- State comptroller "openbook" apps (ASP.NET postbacks — the KY/WI pattern)

### 6. FOIA/records portals
NextRequest, JustFOIA, GovQA — public records request logs themselves are
public and reveal what journalists/lawyers are digging into.

## Priority order for us
1. **ArcGIS Hub sweep** across all 50 states (same API shape as DC — cheap win)
2. **Tyler Civic Access / Accela Citizen Access** portal adapters (permit data)
3. BoardDocs school-board scraper (thousands of districts)
4. Legacy finance-app archaeology (we have 3 proven playbooks already)
