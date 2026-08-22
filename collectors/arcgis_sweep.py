"""ArcGIS Hub sweep: check all 50 states + DC for ArcGIS Open Data portals.
ArcGIS Hub exposes an OGC-style search API:
  https://{host}/api/search/v1/collections/dataset?q=<q>&limit=1
Returns JSON with numberMatched. Test candidate hosts per state.
"""
import subprocess, json, os, time

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
ROOT = os.path.join(os.path.dirname(__file__), "..")

def curl(url, timeout=15):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA,
                        "--compressed", url],
                       capture_output=True, timeout=timeout + 10)
    return r.stdout.decode("utf-8", errors="replace")

def hub_count(host):
    """numberMatched lives on /items; q=* returns 0 — need a real term.
    Use a broad common term and also try empty-q items list."""
    for url in [f"https://{host}/api/search/v1/collections/dataset/items?limit=1",
                f"https://{host}/api/search/v1/collections/dataset/items?q=road&limit=1"]:
        body = curl(url)
        try:
            n = int(json.loads(body).get("numberMatched") or 0)
            if n:
                return n
        except Exception:
            pass
    return 0

# Candidate ArcGIS hosts per state (common naming patterns)
CANDIDATES = {
    "AL": ["alabama.maps.arcgis.com","gis.alabama.gov", "opendata.alabama.gov"],
    "AK": ["gis.data.alaska.gov", "akdata.soest.hawaii.edu"],
    "AZ": ["azgeo.opendata.arcgis.com","azgeo.az.gov", "opendata.az.gov", "land.az.gov"],
    "AR": ["gis.arkansas.gov", "geostor.aransas.gov", "geostor.ar.gov"],
    "CA": ["gis-ca.opendata.arcgis.com","gis.data.ca.gov", "map.dfg.ca.gov"],
    "CO": ["colorado.maps.arcgis.com","data.colorado.gov", "gis.colorado.gov"],
    "CT": ["cteco-uconn.opendata.arcgis.com","cteco.uconn.edu", "gis.ct.gov"],
    "DE": ["opendata.firstmap.delaware.gov", "firstmap.delaware.gov"],
    "DC": ["opendata.dc.gov"],
    "FL": ["floridadep-gis.opendata.arcgis.com", "fgdl.org","gis.myflorida.com", "floridadisaster.org", "labins.org"],
    "GA": ["data.georgiainfo.galileo.usg.edu", "gis.state.ga.us"],
    "HI": ["hawaii-state-gis.opendata.arcgis.com","geoportal.hawaii.gov", "planning.hawaii.gov"],
    "IA": ["iowa-dnr.opendata.arcgis.com","programs.iowadnr.gov", "gis.iowa.gov"],
    "ID": ["gis.idaho.gov", "maps.idaho.gov"],
    "IL": ["illinois-dnr-gis.opendata.arcgis.com","clearinghouse.isgs.illinois.edu", "data.illinois.gov"],
    "IN": ["indiana-map-opendata-indiana.hub.arcgis.com","maps.indiana.edu", "gis.in.gov"],
    "KS": ["kansas-data-access-and-support-center-dasc-kansas.hub.arcgis.com","kansasgis.org", "gisdasc.ku.edu"],
    "KY": ["kentucky-division-of-gis.opendata.arcgis.com","kygisserver.ky.gov", "kygeo.ky.gov"],
    "LA": ["louisiana-maps-opendata.arcgis.com","lagic.brc.lsu.edu", "sonris.com"],
    "MA": ["arcgisserver.digital.mass.gov", "massgis.mass.gov"],
    "MD": ["maryland-imap.opendata.arcgis.com","imap.maryland.gov", "data.imap.maryland.gov"],
    "ME": ["maine-office-of-gis-opendata-maine.hub.arcgis.com","megis.maine.gov", "maine.map.arcgis.com"],
    "MI": ["michigan-open-data-portal-1-michigan.hub.arcgis.com","gis-michigan.opendata.arcgis.com", "migis.org"],
    "MN": ["minnesota-geospatial-commons-opendata-mngeo.hub.arcgis.com", "gisdata.mn.gov","gisdata.mn.gov", "mnmap.delaware.gov"],
    "MO": ["msdis-missouri.opendata.arcgis.com","msdis.missouri.edu", "data.mo.gov"],
    "MS": ["maris.ms.gov", "gis.ms.gov"],
    "MT": ["montana-state-library-opendata-montana.hub.arcgis.com","montana.maps.arcgis.com", "geoinfo.msl.mt.gov"],
    "NC": ["nc-onemap-opendata-nconemap.hub.arcgis.com","nconemap.gov", "xmaps.industry.nc.gov"],
    "ND": ["north-dakota-gishub-opendata-ndgishub.hub.arcgis.com","ndgishub.nd.gov", "ndgishub.nd.gov/arcgis"],
    "NE": ["nebraska-map-opendata-nemap.hub.arcgis.com","dnr.nebraska.gov", "nebraskamap.nebraska.gov"],
    "NH": ["nh.granit.unh.edu", "granitweb.sr.unh.edu"],
    "NJ": ["new-jersey-office-of-gis-njgin-opendata-njogis.hub.arcgis.com","njgin.nj.gov", "njogis-newjersey.opendata.arcgis.com"],
    "NM": ["rgis-university-of-new-mexico-opendata-rgis.hub.arcgis.com","rgis.unm.edu", "data-nm.opendata.arcgis.com"],
    "NV": ["nbgis.nv.gov", "map.nv.gov"],
    "NY": ["nys-civil-service-data-ny.opendata.arcgis.com", "gis-ny-opendata-nygis.hub.arcgis.com","gis.ny.gov", "data.gis.ny.gov"],
    "OH": ["ohio-geographically-referenced-information-program-ogrip-opendata-ohiodnr.hub.arcgis.com","ogrip.oit.ohio.gov", "gis1.oit.ohio.gov"],
    "OK": ["oklahoma-base-map-okmaps-opendata-okmaps.hub.arcgis.com","okmaps.onenet.net", "gis.ok.gov"],
    "OR": ["oregon-imap-opendata-orimap.hub.arcgis.com","spatialdata.oregonexplorer.info", "imap.state.or.us"],
    "PA": ["pennsylvania-spatial-data-access-pasda-pasda.hub.arcgis.com","pasda.psu.edu", "www.pasda.psu.edu"],
    "RI": ["rhode-island-gis-rigis-opendata-rigis.hub.arcgis.com","rinhs-ri-gis-data-ri.hub.arcgis.com", "edc.rigis.org"],
    "SC": ["south-carolina-disaster-recovery-opendata-scdot.hub.arcgis.com","sc-drc.opendata.arcgis.com", "gis.sc.gov"],
    "SD": ["south-dakota-bureau-of-information-telecom-opendata-bhub.hub.arcgis.com","bhub.gis.sd.gov", "arcgis.sd.gov"],
    "TN": ["tennessee-department-of-transportation-opendata-tdot-gis.hub.arcgis.com", "tnmap-tndagisportal.opendata.arcgis.com","tnmap.tn.gov", "tnmap.maps.arcgis.com"],
    "TX": ["texas-natural-resources-information-system-tnris-opendata-tnris.hub.arcgis.com","txgi.tnris.org", "data.tnris.org"],
    "UT": ["utah-agrc-opendata-agrc.hub.arcgis.com", "opendata.gis.utah.gov","gis.utah.gov", "opendata.gis.utah.gov"],
    "VA": ["virginia-commonwealth-university-enterprise-marketing-and-communications-virginia-commonwealth-university.hub.arcgis.com", "virginia-it-institution-viti-opendata-vita-vdot.hub.arcgis.com","vgin.maps.arcgis.com", "gismaps.vgin.virginia.gov"],
    "VT": ["vcgi.vermont.gov", "vtmapcenter.vermont.gov"],
    "WA": ["washington-state-geospatial-open-data-portal-wageo-opendata-wageo.hub.arcgis.com", "wa-geospatial-opendata-wageo.hub.arcgis.com","gis.wa.gov", "wageo.wa.gov"],
    "WV": ["west-virginia-gis-clearinghouse-opendata-wvgis.hub.arcgis.com","wvgis.wvu.edu", "mapwv.gov"],
    "WI": ["wisconsin-state-cartographer-opendata-wisconsinview.hub.arcgis.com","wi-sco.opendata.arcgis.com", "sco.wisc.edu"],
    "WY": ["wygl.wygisc.org", "view.geoportal.io"],
}

results = {}
for st, hosts in sorted(CANDIDATES.items()):
    found = []
    for host in hosts:
        n = hub_count(host)
        if n is not None and n > 0:
            found.append({"host": host, "datasets": n})
            print(f"{st}: {host} -> {n} datasets")
        time.sleep(0.3)
    if not found:
        print(f"{st}: no live ArcGIS Hub among candidates")
    results[st] = found or None

with open(os.path.join(ROOT, "data", "ARCGIS_HUB_INDEX.json"), "w") as f:
    json.dump(results, f, indent=2)
live = {k: v for k, v in results.items() if v}
print(f"\n{len(live)} states with live ArcGIS Hub portals; total datasets:",
      sum(h["datasets"] for v in live.values() for h in v))
