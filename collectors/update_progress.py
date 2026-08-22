"""Update PROGRESS.json for a state — called at the end of each state run.
Usage: python3 collectors/update_progress.py ST status 'json_notes'
"""
import json, sys, os

ROOT = os.path.join(os.path.dirname(__file__), "..")

def main(st, status, notes_json):
    p = json.load(open(os.path.join(ROOT, "PROGRESS.json")))
    notes = json.loads(notes_json)
    entry = p["states"].get(st, {"name": notes.get("name", st)})
    entry.update(notes)
    entry["status"] = status
    p["states"][st] = entry
    with open(os.path.join(ROOT, "PROGRESS.json"), "w") as f:
        json.dump(p, f, indent=2)
    # regenerate the summary counts in PROGRESS.md
    from collections import Counter
    c = Counter(s["status"] for s in p["states"].values())
    done = [k for k, v in p["states"].items() if v["status"] == "done"]
    partial = [k for k, v in p["states"].items() if v["status"] == "partial"]
    todo_n = c.get("todo", 0)
    md = f"""# Progress Tracker

Machine-readable version: `PROGRESS.json` (update both).

**Next up (alphabetical):** first `todo` state after {st}.

## Summary

| Status | Count | States |
|---|---|---|
| done | {len(done)} | {', '.join(sorted(done)) or '-'} |
| partial | {len(partial)} | {', '.join(sorted(partial)) or '-'} |
| todo | {todo_n} | — |

## Playbook per state

1. Transparency/spending portal — find API or bulk export; save sample to `data/<ST>/`
2. DOT bid lettings/tabs — index + first batch
3. City platform registry — top 5-6 cities, Legistar via webapi only
4. `data/<ST>/README.md` + update `PROGRESS.json` + this file

## Gotchas (see PROGRESS.json lessons)

- Legistar wildcard DNS — verify via webapi only
- 403 WAF sites → Playwright, don't fight
- Several states gzip-break plain urllib → use `curl --compressed` (see collectors/state_sweep.py)
- BidX (bidx.com/<state>/lettings) hosts DOT tabs for most states; needs free account or Playwright
"""
    with open(os.path.join(ROOT, "PROGRESS.md"), "w") as f:
        f.write(md)
    print(f"PROGRESS updated: {st} -> {status}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
