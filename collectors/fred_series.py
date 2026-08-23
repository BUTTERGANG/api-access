"""FRED collectors: mortgage rates, delinquencies, consumer credit, CPI.

Free API key: https://fred.stlouisfed.org/docs/api/api_key.html
Set FRED_API_KEY env var. Uses the fred/series/observations endpoint.

Series catalog (all public aggregates — no individual-level data):
  MORTGAGE30US  30-yr fixed mortgage weekly avg (Freddie Mac PMMS)
  MORTGAGE15US  15-yr fixed
  DRCCLACBS     Credit card charge-off rate, all banks (quarterly)
  DRCLACBS      Credit card delinquency rate, all banks
  DRALACBS      All loans delinquency rate
  CORCCACBS     Credit card charge-offs ($)
  REVOLSL       Revolving consumer credit outstanding ($B, monthly)
  GDP           Gross domestic product
  CPIAUCSL      CPI all urban consumers
  MEHOINUSA672N Median household income

Usage: FRED_API_KEY=xxx python3 fred_series.py
Output: data/economic/fred/<SERIES>.json + a combined CSV index
"""
import csv, json, os, subprocess, time

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "economic", "fred")
UA = "api-access-collector/0.1 (alex@buttergang.dev)"
KEY = os.environ.get("FRED_API_KEY", "")

SERIES = {
    "MORTGAGE30US": "30-Year Fixed Rate Mortgage Average (Freddie Mac PMMS, weekly)",
    "MORTGAGE15US": "15-Year Fixed Rate Mortgage Average",
    "DRCCLACBS":    "Credit Card Charge-Off Rate, All Banks (quarterly)",
    "DRCLACBS":     "Credit Card Delinquency Rate, All Banks",
    "DRALACBS":     "Delinquency Rate on All Loans, All Banks",
    "CORCCACBS":    "Credit Card Charge-Offs, All Banks ($)",
    "REVOLSL":      "Revolving Consumer Credit Outstanding ($B)",
    "GDP":          "Gross Domestic Product",
    "CPIAUCSL":     "CPI: All Urban Consumers",
    "MEHOINUSA672N": "Median Household Income (annual)",
}


def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, url],
                       capture_output=True, timeout=90)
    return r.stdout.decode("utf-8", errors="replace")


def main():
    if not KEY:
        sys_exit = "FRED_API_KEY not set. Get one free: https://fred.stlouisfed.org/docs/api/api_key.html"
        print(sys_exit)
        return 1
    os.makedirs(OUT, exist_ok=True)
    rows_all = []
    ok = fail = 0
    for sid, desc in SERIES.items():
        url = (f"https://api.stlouisfed.org/fred/series/observations"
               f"?series_id={sid}&api_key={KEY}&file_type=json")
        raw = curl(url)
        try:
            d = json.loads(raw)
            obs = d["observations"]
        except Exception as e:
            print(f"  {sid}: FAILED ({e}) {raw[:150]}")
            fail += 1
            continue
        with open(os.path.join(OUT, f"{sid}.json"), "w") as f:
            json.dump(d, f, indent=1)
        valid = [o for o in obs if o["value"] != "."]
        print(f"  {sid}: {len(obs)} obs ({len(valid)} valid) {desc}")
        for o in obs:
            rows_all.append([sid, o["date"], o["value"], desc])
        ok += 1
        time.sleep(0.5)
    with open(os.path.join(OUT, "ALL_SERIES.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series_id", "date", "value", "description"])
        w.writerows(rows_all)
    print(f"\nDone: {ok} ok, {fail} failed. Combined CSV at data/economic/fred/ALL_SERIES.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
