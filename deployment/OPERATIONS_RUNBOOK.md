# Veriq MVP Operations Runbook

## Start and verify

```bash
docker compose up -d
docker compose ps
python scripts/smoke_test.py
```

Expected result: both services are healthy, the backend health and active-evidence endpoints respond, and all six judge-facing routes return HTTP 200.

## Inspect without exposing secrets

```bash
docker compose ps
docker compose logs --tail=200 frontend
docker compose logs --tail=200 backend
```

Do not print `.env`, request bodies or learner records into tickets or public logs.

## Restart

```bash
docker compose restart backend
docker compose restart frontend
python scripts/smoke_test.py
```

## Back up the demonstration database

Stop the backend, copy the named volume through the CCE-approved backup mechanism, then restart and smoke-test. Record timestamp, image digest, database checksum, operator and restore-test result. Never move a live SQLite file with an uncontrolled file copy.

## Provider failure

1. Confirm backend health and outbound HTTPS connectivity.
2. Confirm the secret exists without printing its value.
3. Check Gemini quota/provider status and the configured model name.
4. Keep deterministic School Pulse and Early Intervention views available.
5. Do not present cached or fabricated AI output as a new live answer.

## Suspected data or key exposure

1. Stop affected processing and restrict access.
2. Rotate the Gemini key and any affected credentials.
3. Preserve relevant logs without copying personal data into public channels.
4. Notify the appointed incident and data-protection owners.
5. Assess applicable notification duties and document containment, correction and lessons learned.

## Release checklist

- Unit, AI-control, type, lint, production-build, dependency and secret checks pass.
- Container images are rebuilt from the lockfiles and scanned.
- Exact frontend/API origins and TLS are verified.
- Synthetic dataset only; upload acknowledgement is enforced.
- Database backup and rollback image are available.
- Smoke test and judge workflow pass.
- Known limitations are disclosed to reviewers.
