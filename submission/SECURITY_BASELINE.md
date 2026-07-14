# Veriq MVP Security and Dependency Baseline

**Verification date:** 14 July 2026  
**Scope:** Development-track MVP frontend and backend

## Remediation completed

- Upgraded Next.js from 14.2.31 to the patched 15.5.20 release.
- Kept React and React DOM at the compatible, exactly pinned 18.3.1 release.
- Locked transitive PostCSS to patched version 8.5.10.
- Kept the npm lockfile as the reproducible frontend dependency source.
- Kept every backend package exactly pinned in `backend/requirements.txt`.
- Added explicit `dev`, `build`, `start`, `lint` and `typecheck` scripts.

The upgrade follows the maintained Next.js 15 line to minimise breaking changes while resolving the audit findings. A larger Next.js 16 and React 19 migration is intentionally deferred because it is unnecessary for the MVP security fix and would expand submission risk.

## Verification results

| Check | Result |
|---|---|
| `npm audit --omit=dev --audit-level=high --package-lock-only` | Passed: 0 vulnerabilities |
| `npm run typecheck` | Passed: 0 TypeScript errors |
| `npm run lint` | Passed: 0 ESLint warnings or errors |
| `npm run build` | Passed: optimized production build, 8 application routes |
| `python -m unittest discover -s tests -v` | Passed: 29 of 29 backend tests |
| Frontend production health | Passed: HTTP 200 on `http://127.0.0.1:3000/` |
| Backend health | Passed: `{\"status\":\"healthy\"}` on `http://127.0.0.1:8000/health` |
| Visible browser release flow | Passed: 35 of 35 checks; no failed requests, console/page errors, encoding defect or mobile overflow |

## Runtime baseline

- Node.js tested: 24.14.0
- npm tested: 11.9.0
- Next.js: 15.5.20
- React / React DOM: 18.3.1
- TypeScript: 5.7.2
- FastAPI: 0.115.6
- Gemini SDK (`google-genai`): 2.11.0

## Operational notes

- Secrets remain outside source control in `backend/.env`; only safe variable names and placeholders will be documented in the root environment template.
- The current local MVP must use fictional or synthetic learner data until production authentication, tenant isolation, encryption, retention and formal school data-processing controls are implemented.
- Production dependency auditing must be rerun before the final submission build and before each hosted release.
- `npm run build` copies Next.js static assets into standalone output, preventing an HTML-only deployment whose JavaScript and CSS return 404.

## Authoritative upgrade references

- Next.js version 15 upgrade guide: https://nextjs.org/docs/app/guides/upgrading/version-15
- Next.js security advisories: https://github.com/vercel/next.js/security/advisories
