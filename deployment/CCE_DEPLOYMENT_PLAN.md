# Veriq CCE Deployment Plan

**Target:** ZCHPC Cloud Computing Environment (CCE), subject to the infrastructure allocation and platform guidance issued by the challenge.  
**Packaging status:** Linux container definitions and local Compose topology prepared; Docker execution remains to be verified on a Docker-capable host because Docker is not installed on the development workstation.

## Deployment unit

Veriq is packaged as two non-root Linux containers:

1. `frontend`: Next.js standalone Node.js service on port 3000.
2. `backend`: FastAPI/Uvicorn service on port 8000 with a persistent `/data` volume for SQLite.

Gemini remains an external HTTPS service. The backend is the only component that holds the Gemini key. Browser clients never receive the key. The public frontend API address is embedded at frontend image build time through `NEXT_PUBLIC_VERIQ_API_URL`.

## Requested CCE baseline

- Linux x86_64 virtual machine or container host.
- Docker Engine 24+ with Docker Compose v2, or an equivalent CCE container service.
- Recommended allocation: 2 vCPU, 4 GB RAM and 10 GB persistent disk.
- Minimum demonstration allocation: 2 vCPU, 2 GB RAM and 5 GB persistent disk.
- Outbound TCP 443 access to the configured Gemini endpoint and package/container registries during image build.
- Inbound HTTPS through the CCE ingress/reverse proxy; ports 3000 and 8000 should not both be exposed directly to the public internet.
- DNS name and TLS certificate supplied through the CCE ingress process.

These are engineering estimates for the 20-learner demonstration dataset, not measured production capacity claims. Load and storage sizing must be repeated with the agreed pilot population.

## Configuration

Create a host `.env` from `deployment/cce.env.example` and keep it outside source control. Set:

- `GEMINI_API_KEY`: managed secret, never a build argument.
- `GEMINI_MODEL`: approved model identifier.
- `NEXT_PUBLIC_VERIQ_API_URL`: externally reachable HTTPS API URL used by browsers.
- `VERIQ_ALLOWED_ORIGINS`: exact externally reachable HTTPS frontend origin. Do not use `*` for a real-data pilot.

For example, if the allocated names are `https://veriq.example.cce.zw` and `https://api.veriq.example.cce.zw`, use those exact origins. A CCE ingress may alternatively route `/api` to the backend, but that requires a future same-origin frontend/proxy change and should be tested before use.

## Build and launch

On the CCE host or approved CI runner:

```bash
cp deployment/cce.env.example .env
# Set real values using the CCE secret mechanism; do not commit .env.
docker compose build --pull
docker compose up -d
docker compose ps
```

Verify:

```bash
VERIQ_FRONTEND_URL=https://veriq.example.cce.zw \
VERIQ_BACKEND_URL=https://api.veriq.example.cce.zw \
python scripts/smoke_test.py
```

Then upload only the included synthetic judge CSV files and complete the judge workflow. Do not upload real learner records.

## CCE implementation roadmap

| Phase | Work | Acceptance evidence |
|---|---|---|
| 1. Access and discovery | Confirm CCE account, quotas, DNS, ingress, registry, outbound policy and secret mechanism. | Signed environment checklist and named technical contact. |
| 2. Image verification | Build pinned frontend/backend images; scan dependencies and images. | Image digests, zero unresolved high/critical findings, SBOM or package inventory. |
| 3. Synthetic deployment | Configure exact origins, TLS, volume and Gemini secret; deploy judge data only. | Healthy containers, HTTPS, smoke-test output and screenshots. |
| 4. Resilience test | Restart services, verify persistent evidence, back up and restore the volume, simulate Gemini failure. | Recovery log and evidence that deterministic views remain available. |
| 5. Performance check | Exercise the agreed concurrent demonstration load and record latency/memory/CPU. | Measured test report; resource request adjusted from evidence. |
| 6. Judge release | Pin image digests, freeze configuration, rerun audit/tests and rehearse demo. | Release record, rollback image and backup demo video. |
| 7. Real-data pilot gate | Complete legal/privacy/security controls listed in the compliance plan. | Written go/no-go approval; no real data before approval. |

## Rollback and recovery

- Tag and retain the last known-good frontend and backend image digests.
- Back up the persistent SQLite volume before application or schema changes.
- Roll back both application images together if an API contract change is involved.
- Restore a copied database only after stopping the backend to avoid an inconsistent SQLite file.
- If Gemini is unavailable, retain deterministic evidence views and show the explicit provider error; do not replace it with an ungrounded answer.

## Known constraints

- SQLite and a single Uvicorn worker suit the demonstration but are not a multi-instance production database architecture.
- Authentication, RBAC and tenant isolation are not implemented; therefore this package remains synthetic-data-only.
- Frontend public API URL is a build-time variable, so each target environment requires a correctly configured frontend image build.
- Docker/Compose could not be executed on the current workstation. The normal build, unit, type, lint, audit and HTTP smoke paths are verified locally; container execution is an explicit final deployment gate.
