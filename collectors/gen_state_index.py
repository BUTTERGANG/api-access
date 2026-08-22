"""Generate states/SOURCES.md — a per-state source index.

For each state: transparency/portal, DOT bid tabs, data portal, and known
meeting-platform anchors (verified where we probed, else TODO). Indiana gets
the fully researched entry; others get the standard skeleton with the
universal patterns (every state has DOT bid tabs; most have a transparency
portal) plus known anchors.
"""
import os

STATES = {
    "AL": ("Alabama", "open.alabama.gov", "dot.state.al.us"),
    "AK": ("Alaska", "data.alaska.gov", "dot.alaska.gov"),
    "AZ": ("Arizona", "openbooks.az.gov", "azdot.gov"),
    "AR": ("Arkansas", "transparency.arkansas.gov", "ardot.gov"),
    "CA": ("California", "openbook.ca.gov / data.ca.gov", "dot.ca.gov"),
    "CO": ("Colorado", "colorado.gov/transparency / data.colorado.gov", "codot.gov"),
    "CT": ("Connecticut", "portal.ct.gov (OpenCheck)", "portal.ct.gov/DOT"),
    "DE": ("Delaware", "openstates / data.delaware.gov", "deldot.gov"),
    "FL": ("Florida", "floridahasright.com / data.floridapfo.org", "fdot.gov"),
    "GA": ("Georgia", "open.georgia.gov", "dot.ga.gov"),
    "HI": ("Hawaii", "data.hawaii.gov", "hidot.hawaii.gov"),
    "ID": ("Idaho", "transparency.idaho.gov", "itd.idaho.gov"),
    "IL": ("Illinois", "illinoiscomptroller.gov / data.illinois.gov", "idot.illinois.gov"),
    "IN": ("Indiana", "gateway.ifionline.org (BEST-IN-CLASS)", "erms12c.indot.in.gov/INDOTBidViewer"),
    "IA": ("Iowa", "dom.iowa.gov (transparency)", "iowadot.gov"),
    "KS": ("Kansas", "admin.ks.gov (KanView)", "ksdot.org"),
    "KY": ("Kentucky", "opendoor.ky.gov", "transportation.ky.gov"),
    "LA": ("Louisiana", "laopenbooks.com / data.la.gov", "dotd.la.gov"),
    "ME": ("Maine", "maine.gov/transparency", "maine.gov/mdot"),
    "MD": ("Maryland", "openmaryland / data.maryland.gov", "roads.maryland.gov"),
    "MA": ("Massachusetts", "mass.gov /cthru", "mass.gov/orgs/massdot"),
    "MI": ("Michigan", "michigan.gov/transparency / data.michigan.gov", "michigan.gov/mdot"),
    "MN": ("Minnesota", "mn.gov (Open Checkbook) / data.web.health.mn", "dot.state.mn.us"),
    "MS": ("Mississippi", "transparency.ms.gov", "mdot.ms.gov"),
    "MO": ("Missouri", "openbooks.mo.gov / data.mo.gov", "modot.org"),
    "MT": ("Montana", "transparency.mt.gov / data.mt.gov", "mdt.mt.gov"),
    "NE": ("Nebraska", "openspending.nebraska.gov", "dot.nebraska.gov"),
    "NV": ("Nevada", "openbook.nv.gov / data.nv.gov", "dot.nv.gov"),
    "NH": ("New Hampshire", "das.nh.gov transparency / data.nh.gov", "dot.nh.gov"),
    "NJ": ("New Jersey", "yourmoney.nj.gov / data.nj.gov", "state.nj.us/transportation"),
    "NM": ("New Mexico", "transparent.nm.gov / data.cabq / data.nm.gov", "dot.nm.gov"),
    "NY": ("New York", "openbook.newyorkstate.us / data.ny.gov", "dot.ny.gov (bid tabs: dot.ny.gov/doing-business/opportunities/const-tabulations)"),
    "NC": ("North Carolina", "ncopenbook.gov / data.nc.gov", "ncdot.gov"),
    "ND": ("North Dakota", "nd.gov/openspending / data.nd.gov", "dot.nd.gov"),
    "OH": ("Ohio", "ohiocheckbook.com / data.ohio.gov", "dot.state.oh.us"),
    "OK": ("Oklahoma", "openbooks.ok.gov / data.ok.gov", "odot.org"),
    "OR": ("Oregon", "oregon.gov/transparency / data.oregon.gov", "oregon.gov/odot"),
    "PA": ("Pennsylvania", "openrecords.pa.gov / data.pa.gov", "penndot.pa.gov"),
    "RI": ("Rhode Island", "ri.gov/transparency / data.ri.gov", "dot.ri.gov"),
    "SC": ("South Carolina", "procurement.sc.gov / data.sc.gov", "scdot.org"),
    "SD": ("South Dakota", "bfm.sd.gov transparency / data.sd.gov", "dot.sd.gov"),
    "TN": ("Tennessee", "tn.gov/transparency / data.tn.gov", "tn.gov/tdot"),
    "TX": ("Texas", "comptroller.texas.gov/transparency / data.texas.gov", "txdot.gov (Bid Tabulations Dashboard — 24 months, downloadable)"),
    "UT": ("Utah", "transparent.utah.gov / opendata.utah.gov", "udot.utah.gov"),
    "VT": ("Vermont", "finance.vermont.gov / data.vermont.gov", "vtrans.vermont.gov"),
    "VA": ("Virginia", "open.virginia.gov / data.virginia.gov", "vdot.gov"),
    "WA": ("Washington", "fiscal.wa.gov / data.wa.gov", "wsdot.wa.gov (bid tabulations public)"),
    "WV": ("West Virginia", "transportation.wv.gov transparency / data.wv.gov", "transportation.wv.gov"),
    "WI": ("Wisconsin", "doa.wi.gov openbook / data.wi.gov", "wisconsindot.gov"),
    "WY": ("Wyoming", "data.wy.gov / spendwyoming", "dot.state.wy.us"),
    "DC": ("District of Columbia", "clear.dc.gov / opendata.dc.gov", "ddot.dc.gov"),
}

IN_MEETINGS = """### Meeting platforms (VERIFIED by probing, 2026-08)
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
"""

lines = ["# State source index", "",
         "Per-state entry points for transparency/spending portals, DOT bid",
         "tabulations, open data portals, and meeting platforms. Indiana is the",
         "fully-researched template. Every state entry needs the same three",
         "collectors: (1) spending/transparency bulk, (2) DOT bid tabs,", "(3) meeting-platform registry.", ""]
for abbr, (name, portal, dot) in STATES.items():
    lines.append(f"## {abbr} — {name}")
    lines.append(f"- Transparency/spending: {portal}")
    lines.append(f"- DOT (bid lettings/tabs): {dot}")
    if abbr == "IN":
        lines.append(IN_MEETINGS)
    else:
        lines.append("- Meeting platforms: TODO (probe {slug}.legistar.com, {slug}.granicus.com, "
                     "{slug}.api.civicclerk.com, /AgendaCenter, municodemeetings.com)")
    lines.append("")

os.makedirs("states", exist_ok=True)
with open("states/SOURCES.md", "w") as f:
    f.write("\n".join(lines))
print(f"states/SOURCES.md written ({len(STATES)} entries)")
