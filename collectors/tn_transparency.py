"""Rewrite data/TN/transparency_probe.json from verified probes.

Findings (verified 2026-08-22):
- data.tn.gov is NOT a Socrata portal: Apache returns 403 on / and 404 on
  /api/catalog/v1 even with a browser User-Agent. No open SODA API.
  (City portals ARE Socrata: data.nashville.gov, data.memphistn.gov.)
- Transparent Tennessee lives at tn.gov/transparenttn.html with sections:
  checkbook, contracts, finances/interactive-budget, local, state taxes.
- State Employee Salary Search is salary.app.tn.gov/searchsalary — a
  server-rendered app; plain GET/POST returns a 404 page and needs session
  cookies/JS -> Playwright candidate.
"""
import json

OUT = "/home/alex/code/BUTTERGANG/api-access/data/TN"

probe = {
    "probed": "2026-08-22",
    "user_agent_note": (
        "Plain urllib gets connection-reset by the tn.gov WAF; browser-like "
        "User-Agent via curl works for HTML pages."),
    "data.tn.gov": {
        "verdict": "not-socrata",
        "checks": {
            "https://data.tn.gov/": "403 Forbidden (Apache)",
            "https://data.tn.gov/api/catalog/v1?q=&limit=5": "404 Not Found",
        },
        "note": ("No Socrata catalog/SODA API at this host. TN state GIS data "
                 "lives at tnmap / geodata.tn.gov (STS-GIS). City Socrata "
                 "portals: data.nashville.gov, data.memphistn.gov."),
    },
    "transparent_tennessee": {
        "home": "https://www.tn.gov/transparenttn.html",
        "sections": [
            "/transparenttn/finances/checkbook.html (payments checkbook; deep link fetch was WAF-reset — retry needed)",
            "/transparenttn/contracts.html",
            "/transparenttn/finances/interactive-budget0.html",
            "/transparenttn/local.html",
            "/transparenttn/statetaxes.html",
            "/transparenttn/accountablegovernment/performance-dashboard.html",
        ],
        "external_systems": [
            "PeopleSoft supplier/contract search: hub.edison.tn.gov ...TN_ACTIVE_SWC_CMP.GBL (active contracts)",
            "CPO all-contracts dashboard: tn.gov/generalservices/procurement/.../all-contracts-dashboard.html",
        ],
    },
    "salary_search": {
        "url": "https://salary.app.tn.gov/searchsalary",
        "verdict": "server-rendered app; GET/POST without session returns its 404 page",
        "status": "needs-playwright-or-session-cookies",
    },
}

with open(f"{OUT}/transparency_probe.json", "w") as f:
    json.dump(probe, f, indent=2)
print("wrote transparency_probe.json")
