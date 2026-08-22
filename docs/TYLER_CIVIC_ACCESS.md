# Tyler Civic Access / EnerGov — prototype findings

## Architecture (verified by endpoint archaeology + Playwright)

```
SPA:      https://{tenant}-energovweb.tylerhost.net/apps/selfservice
Real API: https://{tenant}-energovapi.tylerhost.net/apps/selfservicewebapi/api
Auth:     Tyler Identity (Portico OIDC) — identity.tylerportico.com
Tenant:   resolved per-tenant; numeric TenantID from /api/Home/GetTenants
          (e.g. LawrenceKS = TenantID 1, TenantName "LawrenceKSProd")
Headers:  tenantId, tenantName, Tyler-TenantUrl, Tyler-Tenant-Culture
```

## Key API routes (extracted from the SPA's minified bundle)

The full route map lives in `/apps/selfservice/app/energov?v=...`:

- `/energov/permits/search/` — public permit search
  - `GET criteria` — returns the search-criteria model
  - `POST` — search with `{PageSize, PageNumber, SearchText, ModuleId,
    CaseTypeIds, StartDate, EndDate, SortField, ...}`
  - `GET setup/{id}` — secondary data
- `/energov/entity/permits/search/search` (+`bufferredsearch`,
  `extentsearch`) — authenticated deep search
- `/energov/entity/violations/search` — code cases
- `/energov/entity/inspections/search/unauth` — anonymous inspections
- `/energov/mypermits|mylicenses|myrequests/search` — account-bound
- `/Home/GetTenants` — unauthenticated; returns tenant registry

## The blocker (and why it exists)

Public search requires a **Tyler Identity bearer token**. Every tested
tenant (Lawrence KS, Clay County FL, Box Elder SD, Westminster CA) redirects
the search page through Portico OIDC sign-in — even for "public" search.
Anonymous browsing stops at the login wall.

Token flow: OIDC implicit/PKCE via identity.tylerportico.com with the
tenant's client_id → access_token in localStorage → Authorization: Bearer on
API calls. Account creation is free but requires email verification per
tenant.

## Prototype status

- ✅ Playwright loads the SPA, passes tenant-picker dialog, reaches login wall
- ✅ Confirmed real API host pattern (`{tenant}-energovapi.tylerhost.net`)
- ✅ Confirmed numeric TenantID discovery via GetTenants
- ✅ Full API route map extracted from bundles (works for any tenant)
- ❌ Anonymous token minting blocked by OIDC interactive flow

## Path forward (pick one)

1. **Register one free account** on a friendly tenant (e.g. Lawrence KS),
   capture the token once via Playwright, and test how long it lasts +
   whether one token works across tenants. Then replay API calls directly
   (fast, no browser).
2. **Playwright-with-account** automation: keep a session alive, scrape
   rendered results. Slower but robust to token expiry.
3. **FOIA the vendor**: Tyler publishes API docs for government partners;
   some tenants expose bulk extracts on request.

Cost/benefit: option 1 gives us every permit/code-case/license in ~thousands
of Tyler tenants nationwide with one manual signup. That's worth doing.
