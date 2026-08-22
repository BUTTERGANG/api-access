"""AL final round: ALDOT real letting portal found (alletting.dot.state.al.us).
Pull the Bid Tabs index + one letting file listing; save structured data.
"""
import subprocess, re, json, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"
OUT = "/home/alex/code/BUTTERGANG/api-access/data/AL"

def curl(url):
    r = subprocess.run(["curl", "-sL", "-m", "30", "-A", UA, "--compressed",
                        "-w", "\n__S__%{http_code}", url],
                       capture_output=True, text=True, timeout=35)
    m = re.search(r"\n__S__(\d+)$", r.stdout)
    return (int(m.group(1)) if m else 0), (r.stdout[:m.start()] if m else r.stdout)

results = {}

# Bid tabs index
s, b = curl("https://alletting.dot.state.al.us/DW_Pages/Bid_Tabs/Bidtabs.html")
print("bidtabs page:", s, len(b))
tab_links = sorted(set(re.findall(r'href="([^"]+)"', b)))
aldot_links = [l for l in tab_links if "Bid" in l or "bid" in l or ".pdf" in l or ".xls" in l]
print("candidate tab links:", aldot_links[:15])
results["bidtabs_index_links"] = aldot_links[:40]

# A recent letting files page
s2, b2 = curl("https://alletting.dot.state.al.us/DW_Pages/Letting_Files/2026/LettingFiles_082826.html")
print("letting 082826:", s2, len(b2))
files = sorted(set(re.findall(r'href="([^"]+\.(?:pdf|xlsx?|docx?))"', b2, re.I)))
print("letting files:", files[:12])
results["letting_082826_files"] = files

# grab one bid tab PDF if present
os.makedirs(os.path.join(OUT, "aldot"), exist_ok=True)
if files:
    sample = files[0]
    url = sample if sample.startswith("http") else f"https://alletting.dot.state.al.us/{sample.lstrip('./')}"
    r = subprocess.run(["curl", "-sL", "-m", "60", "-A", UA, "-o",
                        os.path.join(OUT, "aldot", os.path.basename(sample)), url],
                       capture_output=True, text=True, timeout=70)
    p = os.path.join(OUT, "aldot", os.path.basename(sample))
    if os.path.exists(p):
        with open(p, "rb") as fh:
            print("downloaded:", os.path.basename(sample), os.path.getsize(p), fh.read(4))

with open(os.path.join(OUT, "aldot_letting_data.json"), "w") as f:
    json.dump(results, f, indent=2)
print("saved aldot_letting_data.json")
