"""Tyler Civic Access (EnerGov) permit-search prototype.

Architecture discovered via endpoint archaeology on Lawrence, KS:
  1. Portal SPA: https://{tenant}-energovweb.tylerhost.net/apps/selfservice
  2. Real API:   https://{tenant}-energovapi.tylerhost.net/apps/selfservicewebapi/api
  3. Auth:       Portico OIDC (identity.tylerportico.com) — anonymous users get
                 a bearer token minted in-browser; API rejects calls without it
                 ("Authorization has been denied").
  4. Tenant headers: tenantId + Tyler-TenantUrl + Tyler-Tenant-Culture

Strategy: Playwright loads the SPA (minting the anonymous token), intercepts
the token from local storage / network, then either replays fast API calls or
scrapes rendered search results directly.
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "TYLER")

TENANTS = {
    "lawrenceks": {
        "name": "Lawrence, KS",
        "spa": "https://lawrenceks-energovweb.tylerhost.net/apps/selfservice",
    },
}

def capture_token_and_search(tenant_key, search_text="2024"):
    cfg = TENANTS[tenant_key]
    tokens = []
    api_calls = []
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0")
        page = ctx.new_page()

        # Capture any JSON API responses (search results) and auth traffic
        def on_response(resp):
            url = resp.url
            if "selfservicewebapi" in url or "/api/" in url:
                try:
                    body = resp.json()
                except Exception:
                    body = None
                entry = {"url": url, "status": resp.status}
                # capture authorization header from the request
                req = resp.request
                auth = req.header_value("authorization")
                if auth:
                    entry["auth"] = auth[:40] + "..."
                    tokens.append(auth)
                hdrs = {k: req.header_value(k) for k in ["tenantId", "Tyler-TenantUrl"] if req.header_value(k)}
                if hdrs:
                    entry["req_headers"] = hdrs
                if body is not None:
                    entry["body_preview"] = str(body)[:500]
                api_calls.append(entry)

        page.on("response", on_response)

        print(f"[{tenant_key}] loading SPA...")
        page.goto(cfg["spa"] + "#/search/results?searchMode=publicSearch",
                  wait_until="networkidle", timeout=60000)
        time.sleep(5)

        # Try to drive the public search UI: fill search box and submit
        try:
            # The public search page has inputs; dump what's there
            inputs = page.eval_on_selector_all(
                "input", "els => els.map(e => ({id: e.id, name: e.name, ph: e.placeholder, type: e.type}))")
            print("inputs:", json.dumps(inputs)[:400])
            buttons = page.eval_on_selector_all(
                "button", "els => els.map(e => e.textContent.trim()).slice(0, 15)")
            print("buttons:", buttons)
        except Exception as e:
            print("selector err:", str(e)[:100])

        # Dump localStorage keys (token lives here)
        storage = page.evaluate("() => JSON.stringify(Object.fromEntries(Object.entries(localStorage)))")
        ls = json.loads(storage)
        token_keys = [k for k in ls if "token" in k.lower() or "auth" in k.lower()]
        for k in token_keys:
            v = ls[k]
            if len(v) > 50:
                tokens.append(("localStorage:" + k, v))
        print("localStorage keys:", list(ls.keys())[:15])

        time.sleep(3)
        browser.close()

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{tenant_key}_probe.json"), "w") as f:
        json.dump({"tokens_found": len(tokens),
                   "api_calls": api_calls[:30]}, f, indent=2)
    print(f"\ncaptured {len(api_calls)} API calls, {len(tokens)} token refs -> data/TYLER/{tenant_key}_probe.json")
    return api_calls

if __name__ == "__main__":
    tenant = sys.argv[1] if len(sys.argv) > 1 else "lawrenceks"
    collect_api_calls = capture_token_and_search(tenant)
    for c in collect_api_calls[:10]:
        print(c["url"][:120], c["status"])
