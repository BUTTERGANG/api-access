"""BLS collectors: CPI metro/regional series (cost of living).

No key needed for v1 API (25 req/day/IP); free key raises to 500/day:
https://data.bls.gov/registrationEngine/
Set BLS_API_KEY env var (optional).

Series IDs of interest:
  CUUR0000SA0  CPI-U all items, US, not seasonally adjusted
  CUURA311SA0  CPI-U all items, NYC metro
  CUURA322SA0  CPI-U all items, LA metro
  CUURA411SA0  CPI-U all items, Chicago metro
  CUURS49ASA0  CPI-U all items, SF metro
  CUUR0000SAH1 CPI shelter index (housing cost proxy)

Docs: https://www.bls.gov/developers/api_signature_v1.htm
Usage: python3 bls_cpi.py   (optionally BLS_API_KEY=xxx)
Output: data/economic/bls/*.json
"""
import json, os, subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "economic", "bls")
UA = "api-access-collector/0.1 (alex@buttergang.dev)"
KEY = os.environ.get("BLS_API_KEY", "")

SERIES = [
    "CUUR0000SA0",   # US all items
    "CUURS35ASA0",  # San Francisco (S-size class series; A311/A322/A411 are discontinued)
    "CUURS12ASA0",  # Seattle
    "CUUR0000SAH1",  # Shelter
    "CUUR0000SEHF01",# Energy commodities
    "CUUR0000SETB01",# Gasoline
]


def main():
    os.makedirs(OUT, exist_ok=True)
    payload = {"seriesid": SERIES, "startyear": "2015", "endyear": "2026"}
    if KEY:
        payload["registrationkey"] = KEY
    body = json.dumps(payload)
    r = subprocess.run(
        ["curl", "-sL", "-m", "60", "-A", UA,
         "-X", "POST", "-H", "Content-Type: application/json",
         "-d", body, "https://api.bls.gov/publicAPI/v1/timeseries/data/"],
        capture_output=True, timeout=90)
    d = json.loads(r.stdout.decode())
    status = d.get("status")
    print(f"BLS API status: {status}")
    for s in d.get("Results", {}).get("series", []):
        sid = s["seriesID"]
        data = s.get("data", [])
        with open(os.path.join(OUT, f"{sid}.json"), "w") as f:
            json.dump(s, f, indent=1)
        latest = data[0] if data else {}
        print(f"  {sid}: {len(data)} obs, latest {latest.get('year','?')}-"
              f"{latest.get('period','?')} value={latest.get('value','?')}")
    if d.get("message"):
        print("Messages:", d["message"])


if __name__ == "__main__":
    main()
