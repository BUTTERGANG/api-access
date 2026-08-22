"""Wisconsin OpenBook transparency probe — PARTIAL.

openbook.wi.gov is an ASP.NET WebForms app whose search/export runs
through ASP.NET AJAX PageMethods (JSON POST to
  https://openbook.wi.gov/{Contracts,Expenditures,...}.aspx/{Method}).
Discovered methods: SetSearchType(searchType), ExportWebService(
UserControl, ExportType, FiscalYear, ComparisonYear, SearchType,
SearchString, CategoryCode, AgencyCode, ObjectCode, ProviderCode,
FundCode, ReferenceTransactionNumbers, TransactionNumber, SortField,
SortAscending, SuppressAmountColumns).
Direct POSTs currently return the app's own validation error ("Must
specify valid information for parsing in the string.") — the correct
enum values live inside Telerik ScriptResource bundles. TODO: trace via
Playwright and replay.

This script saves a probe report + sample HTML of the Contracts page.
data.wi.gov (state Socrata portal) no longer resolves (NXDOMAIN as of
2026-08) — recorded in probe_results.json.
"""
import urllib.request, json, os, datetime

UA = {"User-Agent": "api-access-collector/0.1 (alex@buttergang.dev)"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "WI")

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            return r.status, r.read()
    except Exception as e:
        return None, repr(e)[:200].encode()

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    probes = {}
    st, b = get("https://openbook.wi.gov/Contracts.aspx")
    probes["openbook_contracts_page"] = {"status": st, "bytes": len(b or b"")}
    if isinstance(b, bytes):
        with open(os.path.join(OUT, "openbook_contracts_sample.html"), "wb") as f:
            f.write(b)
        import re
        names = set(re.findall(r"PageMethods\.(\w+)\s*=", b.decode("utf-8", "replace")))
        names -= {"_staticInstance"}
        probes["openbook_pagemethods"] = sorted(
            m for m in names if not m.startswith(("get_", "set_")))
    for name, url in [
        ("data_wi_gov_socrata", "https://data.wi.gov/api/catalog/v1?q=&limit=3"),
        ("doa_openbook", "https://doa.wi.gov/openbook"),
        ("openbook_api", "https://openbook.wi.gov/api"),
    ]:
        st, b = get(url)
        probes[name] = {"status": st, "bytes": len(b or b""), "url": url}
    probes["probed_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(os.path.join(OUT, "probe_results.json"), "w") as f:
        json.dump(probes, f, indent=2)
    print(json.dumps(probes, indent=2))
