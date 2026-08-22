# State source index

Per-state entry points for transparency/spending portals, DOT bid
tabulations, open data portals, and meeting platforms. Indiana is the
fully-researched template. Every state entry needs the same three
collectors: (1) spending/transparency bulk, (2) DOT bid tabs,
(3) meeting-platform registry.

## AL — Alabama
- Transparency/spending: open.alabama.gov
- DOT (bid lettings/tabs): dot.state.al.us
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## AK — Alaska
- Transparency/spending: data.alaska.gov
- DOT (bid lettings/tabs): dot.alaska.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## AZ — Arizona
- Transparency/spending: openbooks.az.gov
- DOT (bid lettings/tabs): azdot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## AR — Arkansas
- Transparency/spending: transparency.arkansas.gov
- DOT (bid lettings/tabs): ardot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## CA — California
- Transparency/spending: openbook.ca.gov / data.ca.gov
- DOT (bid lettings/tabs): dot.ca.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## CO — Colorado
- Transparency/spending: colorado.gov/transparency / data.colorado.gov
- DOT (bid lettings/tabs): codot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## CT — Connecticut
- Transparency/spending: portal.ct.gov (OpenCheck)
- DOT (bid lettings/tabs): portal.ct.gov/DOT
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## DE — Delaware
- Transparency/spending: openstates / data.delaware.gov
- DOT (bid lettings/tabs): deldot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## FL — Florida
- Transparency/spending: floridahasright.com / data.floridapfo.org
- DOT (bid lettings/tabs): fdot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## GA — Georgia
- Transparency/spending: open.georgia.gov
- DOT (bid lettings/tabs): dot.ga.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## HI — Hawaii
- Transparency/spending: data.hawaii.gov
- DOT (bid lettings/tabs): hidot.hawaii.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## ID — Idaho
- Transparency/spending: transparency.idaho.gov
- DOT (bid lettings/tabs): itd.idaho.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## IL — Illinois
- Transparency/spending: illinoiscomptroller.gov / data.illinois.gov
- DOT (bid lettings/tabs): idot.illinois.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## IN — Indiana
- Transparency/spending: gateway.ifionline.org (BEST-IN-CLASS)
- DOT (bid lettings/tabs): erms12c.indot.in.gov/INDOTBidViewer
### Meeting platforms (VERIFIED by probing, 2026-08)
- Indianapolis/Marion County → **Municode Meetings** (`indianapolis-in.municodemeetings.com`)
- Evansville → **Granicus** (`evansville.granicus.com`) — LIVE
- West Lafayette → **Granicus** (`westlafayette.granicus.com`) — LIVE
- Fort Wayne → CivicPlus **AgendaCenter** (cityoffortwayne.org)
- Lafayette → CivicPlus **AgendaCenter**
- Noblesville → CivicPlus **AgendaCenter**
- Muncie → **Municode** Meetings
- South Bend, Fishers, Bloomington, West Lafayette, Terre Haute → sites block
  plain HTTP clients (403); need browser-based probe (Playwright) — TODO
- Legistar: NO Indiana clients found via API probe (webapi.legistar.com 500s for
  all IN slugs tried) — Indiana skews CivicPlus/Municode/Granicus, unlike coasts.

### State data infrastructure (VERIFIED live)
- **Indiana Gateway** `gateway.ifionline.org` — bulk downloads (budgets, AFR,
  disbursements, debt, cash, grants, pensions; 2012–present, pipe-delimited);
  Report Builder AJAX API (`/report_builder/geo_response.aspx?term=X` → unit IDs,
  `unitreports_ajax.aspx?unit_id=N` → 50-65 report types per unit); Local
  Contract Search (statutory contracts >$50k); TIF viewer; compliance status.
- **INDOT Bid Viewer** `erms12c.indot.in.gov/INDOTBidViewer/BidTabulations.aspx` —
  ASP.NET postback grid; first page parses to CSV (24 rows collected). Deep
  tabs need VIEWSTATE POST — TODO.
- budgetnotices.in.gov — live (155KB HTML).


## IA — Iowa
- Transparency/spending: dom.iowa.gov (transparency)
- DOT (bid lettings/tabs): iowadot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## KS — Kansas
- Transparency/spending: admin.ks.gov (KanView)
- DOT (bid lettings/tabs): ksdot.org
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## KY — Kentucky
- Transparency/spending: opendoor.ky.gov is DEAD (times out). Live API:
  `https://secure2.kentucky.gov/TransparencyWebApi/v1/*` (keyless, JSON,
  paginated; CSV via SpendingDownload) — see data/KY/README.md
- DOT (bid lettings/tabs): transportation.ky.gov Construction-Procurement —
  SharePoint; lettings list + per-letting proposal/award/bid-tab PDFs
### Meeting platforms (VERIFIED by probing, 2026-08)
- Louisville → **Legistar** (`louisville` — webapi 200, Metro Council);
  also Granicus video (louisville.granicus.com LIVE). louisvilleky.gov 403s plain clients
- Lexington → **Legistar** (`lexington` — webapi 200, Urban County Council)
- Bowling Green / Covington → CivicClerk slugs resolve but UNVERIFIED (wildcard SPA)
- Owensboro → Municode code library only; no third-party agenda platform

## LA — Louisiana
- Transparency/spending: laopenbooks.com / data.la.gov
- DOT (bid lettings/tabs): dotd.la.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## ME — Maine
- Transparency/spending: maine.gov/transparency
- DOT (bid lettings/tabs): maine.gov/mdot
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MD — Maryland
- Transparency/spending: openmaryland / data.maryland.gov
- DOT (bid lettings/tabs): roads.maryland.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MA — Massachusetts
- Transparency/spending: mass.gov /cthru
- DOT (bid lettings/tabs): mass.gov/orgs/massdot
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MI — Michigan
- Transparency/spending: michigan.gov/transparency / data.michigan.gov
- DOT (bid lettings/tabs): michigan.gov/mdot
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MN — Minnesota
- Transparency/spending: mn.gov (Open Checkbook) / data.web.health.mn
- DOT (bid lettings/tabs): dot.state.mn.us
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MS — Mississippi
- Transparency/spending: transparency.ms.gov
- DOT (bid lettings/tabs): mdot.ms.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MO — Missouri
- Transparency/spending: openbooks.mo.gov / data.mo.gov
- DOT (bid lettings/tabs): modot.org
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## MT — Montana
- Transparency/spending: transparency.mt.gov / data.mt.gov
- DOT (bid lettings/tabs): mdt.mt.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NE — Nebraska
- Transparency/spending: openspending.nebraska.gov
- DOT (bid lettings/tabs): dot.nebraska.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NV — Nevada
- Transparency/spending: openbook.nv.gov / data.nv.gov
- DOT (bid lettings/tabs): dot.nv.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NH — New Hampshire
- Transparency/spending: das.nh.gov transparency / data.nh.gov
- DOT (bid lettings/tabs): dot.nh.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NJ — New Jersey
- Transparency/spending: yourmoney.nj.gov / data.nj.gov
- DOT (bid lettings/tabs): state.nj.us/transportation
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NM — New Mexico
- Transparency/spending: transparent.nm.gov / data.cabq / data.nm.gov
- DOT (bid lettings/tabs): dot.nm.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NY — New York
- Transparency/spending: openbook.newyorkstate.us / data.ny.gov
- DOT (bid lettings/tabs): dot.ny.gov (bid tabs: dot.ny.gov/doing-business/opportunities/const-tabulations)
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## NC — North Carolina
- Transparency/spending: ncopenbook.gov / data.nc.gov
- DOT (bid lettings/tabs): ncdot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## ND — North Dakota
- Transparency/spending: nd.gov/openspending / data.nd.gov
- DOT (bid lettings/tabs): dot.nd.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## OH — Ohio
- Transparency/spending: ohiocheckbook.com / data.ohio.gov
- DOT (bid lettings/tabs): dot.state.oh.us
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## OK — Oklahoma
- Transparency/spending: openbooks.ok.gov / data.ok.gov
- DOT (bid lettings/tabs): odot.org
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## OR — Oregon
- Transparency/spending: oregon.gov/transparency / data.oregon.gov
- DOT (bid lettings/tabs): oregon.gov/odot
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## PA — Pennsylvania
- Transparency/spending: openrecords.pa.gov / data.pa.gov
- DOT (bid lettings/tabs): penndot.pa.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## RI — Rhode Island
- Transparency/spending: ri.gov/transparency / data.ri.gov
- DOT (bid lettings/tabs): dot.ri.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## SC — South Carolina
- Transparency/spending: procurement.sc.gov / data.sc.gov
- DOT (bid lettings/tabs): scdot.org
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## SD — South Dakota
- Transparency/spending: bfm.sd.gov transparency / data.sd.gov
- DOT (bid lettings/tabs): dot.sd.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## TN — Tennessee (DONE 2026-08-22)
- Transparency/spending: tn.gov/transparenttn.html (NOT data.tn.gov — Apache 403/404, no Socrata API). Salary search salary.app.tn.gov needs session → Playwright. tn.gov WAF resets plain urllib; use browser UA via curl.
- DOT (bid lettings/tabs): tn.gov/tdot/tdot-construction-division/bid-lettings/ — year index → per-letting pages with ApparentBidResults.pdf / SummaryOfBids.pdf / ContractAwards.pdf / BidAuth.xlsx. Collector: `tn_tdot_bids.py` (117 lettings indexed).
- Meeting platforms: Nashville = Legistar client `nashville` (verified webapi, 21 bodies). Clarksville hints CivicClerk; Memphis/Knoxville/Chattanooga/Murfreesboro have no Legistar client. Collector: `tn_city_platforms.py`. See data/TN/README.md.

## TX — Texas
- Transparency/spending: comptroller.texas.gov/transparency / data.texas.gov
- DOT (bid lettings/tabs): txdot.gov (Bid Tabulations Dashboard — 24 months, downloadable)
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## UT — Utah
- Transparency/spending: transparent.utah.gov / opendata.utah.gov
- DOT (bid lettings/tabs): udot.utah.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## VT — Vermont
- Transparency/spending: finance.vermont.gov / data.vermont.gov
- DOT (bid lettings/tabs): vtrans.vermont.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## VA — Virginia
- Transparency/spending: open.virginia.gov / data.virginia.gov
- DOT (bid lettings/tabs): vdot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## WA — Washington
- Transparency/spending: fiscal.wa.gov / data.wa.gov
- DOT (bid lettings/tabs): wsdot.wa.gov (bid tabulations public)
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## WV — West Virginia
- Transparency/spending: transportation.wv.gov transparency / data.wv.gov
- DOT (bid lettings/tabs): transportation.wv.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## WI — Wisconsin
- Transparency/spending: doa.wi.gov openbook / data.wi.gov
- DOT (bid lettings/tabs): wisconsindot.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## WY — Wyoming
- Transparency/spending: data.wy.gov / spendwyoming
- DOT (bid lettings/tabs): dot.state.wy.us
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)

## DC — District of Columbia
- Transparency/spending: clear.dc.gov / opendata.dc.gov
- DOT (bid lettings/tabs): ddot.dc.gov
- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, {slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)
