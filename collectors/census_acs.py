"""Census API collectors: ACS demographics, income, housing, poverty.

Free API key (recommended, higher limits): https://api.census.gov/data/key_signup.html
Set CENSUS_API_KEY env var (works without key at low volume).

Key datasets:
  ACS 1-year (large geographies) and 5-year (down to block group)
  Useful tables: B19013 (median household income), B25077 (median home value),
  B25064 (median rent), B17001 (poverty status), B25003 (tenure/owners vs renters)

Docs: https://www.census.gov/data/developers/data-sets.html
Usage:
  python3 census_acs.py                    # state-level pull
  python3 census_acs.py --county 06,48     # counties in CA,TX
Output: data/economic/census/*.json (one file per year/geography)
"""
import json, os, subprocess, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "economic", "census")
UA = "api-access-collector/0.1 (alex@buttergang.dev)"
KEY = os.environ.get("CENSUS_API_KEY", "")

# ACS 5-year variables: (variable, human label)
VARS = {
    "B19013_001E": "median_household_income",
    "B25077_001E": "median_home_value",
    "B25064_001E": "median_rent",
    "B17001_002E": "poverty_count",
    "B25003_002E": "owner_occupied",
    "B25003_003E": "renter_occupied",
    "B01003_001E": "total_population",
}


def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "--compressed", url],
                       capture_output=True, timeout=90)
    return r.stdout.decode("utf-8", errors="replace")


def pull(year, geo, geo_label):
    var_list = ",".join(VARS)
    url = (f"https://api.census.gov/data/{year}/acs/acs5"
           f"?get=NAME,{var_list}&for={geo}&key={KEY}" if KEY else
           f"https://api.census.gov/data/{year}/acs/acs5"
           f"?get=NAME,{var_list}&for={geo}")
    raw = curl(url)
    try:
        d = json.loads(raw)
    except Exception as e:
        print(f"  {year}/{geo_label}: FAILED ({e}); {raw[:150]}")
        return False
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"acs5_{year}_{geo_label}.json")
    with open(path, "w") as f:
        json.dump(d, f, indent=1)
    print(f"  {year}/{geo_label}: {len(d)-1} rows -> {path}")
    return True


def main():
    years = [2023, 2022]  # ACS 5-year releases (2024 lands late 2026)
    geos = [("state:*", "states")]
    if "--county" in sys.argv:
        i = sys.argv.index("--county")
        states = sys.argv[i + 1].split(",") if len(sys.argv) > i + 1 else ["06"]
        geos.append((f"county:*&in=state:{','.join(states)}", "counties"))
    for y in years:
        for geo, label in geos:
            pull(y, geo, label)
    print("\nDone. Files in data/economic/census/")


if __name__ == "__main__":
    main()
