"""USAspending collectors: federal spending by state (monthly obligations).

No key needed. Uses /api/v2/search/spending_over_time/ (verified working
2026-08; the v1 spending_by_category route 404s).

Usage:
  python3 usaspending_spending.py                    # IN, FY2025
  python3 usaspending_spending.py --state CA --year 2025
Output: data/economic/usaspending/<ST>_FY<year>.json + .csv
"""
import csv, json, os, subprocess, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "economic", "usaspending")
UA = "api-access-collector/0.1 (alex@buttergang.dev)"

# Federal fiscal year Oct 1 - Sep 30
FY_DATES = {
    2024: ("2023-10-01", "2024-09-30"),
    2025: ("2024-10-01", "2025-09-30"),
    2026: ("2025-10-01", "2026-09-30"),
}


def post(url, payload):
    r = subprocess.run(
        ["curl", "-sL", "-m", "90", "-A", UA,
         "-X", "POST", "-H", "Content-Type: application/json",
         "-d", json.dumps(payload), url],
        capture_output=True, timeout=120)
    return r.stdout.decode("utf-8", errors="replace")


def state_monthly(state_fips, fy):
    start, end = FY_DATES[fy]
    payload = {
        "group": "month",
        "filters": {
            "time_period": [{"start_date": start, "end_date": end}],
            "place_of_performance_locations": [{"country": "USA", "state": state_fips}],
        },
    }
    raw = post("https://api.usaspending.gov/api/v2/search/spending_over_time/", payload)
    try:
        d = json.loads(raw)
        return d["results"]
    except Exception as e:
        print(f"  {state_fips} FY{fy}: FAILED ({e}); {raw[:150]}")
        return None


def main():
    args = sys.argv[1:]
    states = [args[args.index("--state") + 1]] if "--state" in args else ["IN"]
    year = int(args[args.index("--year") + 1]) if "--year" in args else 2025
    if year not in FY_DATES:
        print(f"FY{year} not in date map; add it to FY_DATES.")
        return 1
    os.makedirs(OUT, exist_ok=True)
    for st in states:
        rows = state_monthly(st, year)
        if not rows:
            continue
        with open(os.path.join(OUT, f"{st}_FY{year}.json"), "w") as f:
            json.dump(rows, f, indent=1)
        with open(os.path.join(OUT, f"{st}_FY{year}.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["fy", "month", "total_obligations", "contracts",
                        "grants", "direct_payments", "loans", "other"])
            total = 0.0
            for r in rows:
                amt = r["aggregated_amount"]
                total += amt
                tp = r["time_period"]
                w.writerow([tp["fiscal_year"], tp["month"],
                            f"{amt:.2f}", r.get("Contract_Obligations"),
                            r.get("Grant_Obligations"), r.get("Direct_Obligations"),
                            r.get("Loan_Obligations"), r.get("Other_Obligations")])
        print(f"  {st} FY{year}: {len(rows)} months, ${total:,.0f} total -> {st}_FY{year}.csv")
    print("\nDone. Files in data/economic/usaspending/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
