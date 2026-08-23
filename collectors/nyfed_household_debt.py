"""NY Fed Household Debt & Credit: quarterly household debt/delinquency aggregates.

No API — downloads the public quarterly PDF report (the XLSX links on the
hhdc page are JS-rendered and the direct /xls/ paths 404 to HTML; the PDF
at HHDC_<year>Q<q> is stable and text-extractable via pymupdf).

Source: https://www.newyorkfed.org/microeconomics/hhdc.html
This is THE canonical aggregate source for credit card / mortgage / auto /
student-loan balances and delinquency rates (Equifax panel — aggregates only,
no individual data).

Usage: python3 nyfed_household_debt.py [--quarters 4]
Output: data/economic/nyfed/HHDC_<year>Q<q>.pdf + extracted text .txt
"""
import os, subprocess, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "data", "economic", "nyfed")
UA = "api-access-collector/0.1 (alex@buttergang.dev)"
BASE = ("https://www.newyorkfed.org/medialibrary/interactives/"
        "householdcredit/data/pdf/HHDC_{year}Q{q}")


def fetch(year, q):
    url = BASE.format(year=year, q=q)
    pdf_path = os.path.join(OUT, f"HHDC_{year}Q{q}.pdf")
    r = subprocess.run(["curl", "-sL", "-m", "180", "-A", UA, url, "-o", pdf_path],
                       capture_output=True, timeout=240)
    if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 50_000:
        print(f"  {year}Q{q}: not available ({os.path.getsize(pdf_path) if os.path.exists(pdf_path) else 0} bytes)")
        return False
    # extract text
    try:
        import pymupdf
        d = pymupdf.open(pdf_path)
        text = "\n".join(p.get_text() for p in d)
        txt_path = pdf_path.replace(".pdf", ".txt")
        with open(txt_path, "w") as f:
            f.write(text)
        first = d[0].get_text()[:120].replace("\n", " ")
        print(f"  HHDC_{year}Q{q}.pdf: {os.path.getsize(pdf_path):,} bytes, "
              f"{len(d)} pages -> text saved")
        print(f"    {first}")
        return True
    except ImportError:
        print(f"  HHDC_{year}Q{q}.pdf downloaded ({os.path.getsize(pdf_path):,} bytes); "
              "pip install pymupdf for text extraction")
        return True


def main():
    n_back = 4
    if "--quarters" in sys.argv:
        n_back = int(sys.argv[sys.argv.index("--quarters") + 1])
    os.makedirs(OUT, exist_ok=True)
    # latest quarter first: walk back until we find one
    found = 0
    year, q = 2026, 3  # future-proof start; fetch() skips 404s
    tried = 0
    while found < n_back and tried < 12:
        tried += 1
        if fetch(year, q):
            found += 1
        q -= 1
        if q == 0:
            q = 4
            year -= 1
    print(f"\nDone: {found} quarterly reports in data/economic/nyfed/")
    # Key tables for parsing later: 'Household debt balances' and
    # 'Delinquency transitions' — delinquency rates by loan type are in the
    # text near 'Percent of balance 90+ days delinquent'.


if __name__ == "__main__":
    main()
