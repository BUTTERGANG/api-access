"""EIA collectors: gas prices, electricity rates, natural gas.

Free API key: register at https://www.eia.gov/opendata/register.php
Set EIA_API_KEY env var. Without a key, some series still work via the
v2 API's rate-limited anonymous access — verify before relying on it.

Docs: https://www.eia.gov/opendata/v2.php
Usage:
  EIA_API_KEY=xxx python3 eia_prices.py            # full pull
  python3 eia_prices.py --no-key                   # try anonymous
Output: data/economic/eia/*.json (raw API responses, never hand-edited)
"""
import json, os, subprocess, sys, time

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "economic", "eia")
UA = "api-access-collector/0.1 (alex@buttergang.dev)"
KEY = os.environ.get("EIA_API_KEY", "")

# Series catalog: name -> v2 route (route + facet params)
SERIES = {
    # Weekly retail gasoline & diesel, U.S. + regions (Petroleum Marketing Monthly)
    "gasoline_weekly_us": {
        "route": "petroleum/pri/gnd/data",
        "params": "frequency=weekly&data[0]=value&facets[product][]=EPMRR&facets[duoarea][]=NUS&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    },
    "diesel_weekly_us": {
        "route": "petroleum/pri/gnd/data",
        "params": "frequency=weekly&data[0]=value&facets[product][]=EPD2DXL0&facets[duoarea][]=NUS&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    },
    # State gasoline grades monthly (all areas)
    "gasoline_monthly_states": {
        "route": "petroleum/pri/gnd/data",
        "params": "frequency=monthly&data[0]=value&facets[product][]=EPMRR&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    },
    # Average retail electricity price by state & sector, monthly
    "electricity_price_states_monthly": {
        "route": "electricity/retail-sales/data",
        "params": "frequency=monthly&data[0]=price&facets[sectorid][]=RES&facets[sectorid][]=COM&facets[sectorid][]=IND&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    },
    # Residential natural gas price by state, monthly
    "natgas_residential_price_states": {
        "route": "natural-gas/pri/sum/data",
        "params": "frequency=monthly&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000",
    },
}


def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "--compressed", url],
                       capture_output=True, timeout=90)
    return r.stdout.decode("utf-8", errors="replace")


def fetch(name, spec):
    url = f"https://api.eia.gov/v2/{spec['route']}/?api_key={KEY}&{spec['params']}"
    raw = curl(url)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{name}.json")
    with open(path, "w") as f:
        f.write(raw)
    try:
        d = json.loads(raw)
        n = len(d.get("response", {}).get("data", []))
        total = d.get("response", {}).get("total")
        print(f"  {name}: {n} rows (total={total}) -> {path}")
        return True
    except Exception as e:
        print(f"  {name}: FAILED to parse ({e}); first 200 chars: {raw[:200]}")
        return False


def main():
    only_keyless = "--no-key" in sys.argv
    if not KEY and not only_keyless:
        print("WARNING: EIA_API_KEY not set — attempting anonymous calls anyway.\n"
              "Register free key at https://www.eia.gov/opendata/register.php")
    ok = fail = 0
    for name, spec in SERIES.items():
        if fetch(name, spec):
            ok += 1
        else:
            fail += 1
        time.sleep(1)  # be polite; EIA allows ~5k req/hr with key
    print(f"\nDone: {ok} ok, {fail} failed. Raw files in data/economic/eia/")


if __name__ == "__main__":
    main()
