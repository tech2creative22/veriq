# Veriq MVP Test and Release Report

**Release candidate date:** 14 July 2026  
**Scope:** local production build with synthetic judge dataset

## Summary

| Verification | Result |
|---|---|
| Backend unit/control tests | Pass: 29/29 |
| AI evidence-control evaluation | Pass: 23/23 |
| TypeScript | Pass: 0 errors |
| ESLint | Pass: 0 warnings/errors |
| Next.js production build | Pass: 8 application routes, standalone assets prepared |
| Production dependency audit | Pass: 0 vulnerabilities |
| HTTP deployment smoke | Pass: 8/8 frontend/backend checks |
| Visible Playwright judge flow | Pass: 35/35 checks |
| Dataset validation | Pass: 20 learners, 4 classes, 834 records, expected scenario labels |

## Browser flow evidence

The browser test used the production standalone frontend at `http://localhost:3000` and FastAPI at `http://localhost:8000`. It verified:

- all six judge-facing routes return a rendered page with a main heading;
- no server error or Unicode replacement character appears;
- the analyse action is disabled until data use is acknowledged;
- all three CSV inputs accept the committed synthetic dataset;
- the import completes with 20 learners across 4 classes;
- the upload routes to School Pulse and imported coverage is visible;
- Beacon treats `hello` as a conversational greeting rather than repeating an evidence template;
- School Pulse has no horizontal overflow at a 390 px mobile viewport; and
- there are no failed browser requests, console errors or page errors.

Machine-readable results and four release screenshots are under `outputs/judge-readiness-zimbabwe/browser/`.

## Defects found and corrected during release testing

1. The standalone Node server originally served HTML but not copied JS/CSS assets. `scripts/prepare_standalone.mjs` is now part of `npm run build`, and the rerun rendered and hydrated every page.
2. An empty current-analysis Decision Brief returned HTTP 404, producing avoidable browser console noise. It now returns a successful `null` result until a brief is generated, while unknown explicit decision IDs still return 404.
3. The upload acknowledgement originally existed only in the UI. The API now independently rejects false or missing acknowledgement and returns the accepted state in import metadata.

## Reproduction commands

```powershell
npm ci
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev --audit-level=high --package-lock-only
Set-Location backend
python -m unittest discover -s tests -v
Set-Location ..
python scripts/run_ai_evaluation.py
python scripts/validate_judge_dataset.py
python scripts/smoke_test.py
```

The browser automation was run through the Playwright workflow against the visible production application. The final JSON result is the portable review artifact; the temporary automation script is not part of the application source.

## Remaining external release gates

- Run the documented 10-question live Gemini semantic protocol three times and record the 30-response rubric before final submission.
- Build and start the Docker/Compose package on a Docker-capable host or allocated CCE; Docker is not installed on this workstation.
- Provide a hosted demo URL or CCE route and rerun the smoke/browser flow against HTTPS.
- Add repository remote/commit evidence after the applicant provides real Git identity.
- Complete the proposal cover identity, final code licence and security contact.
