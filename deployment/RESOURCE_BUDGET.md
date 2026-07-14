# Veriq Demonstration Resource Budget

## Initial allocation

| Component | CPU limit | Memory limit | Persistent storage | Notes |
|---|---:|---:|---:|---|
| Next.js frontend | 0.5 vCPU | 512 MB | None | Static/prerendered UI plus standalone server. |
| FastAPI backend | 1.0 vCPU | 768 MB | 2 GB initial volume | One Uvicorn worker and SQLite for a single-school demonstration. |
| Host/platform reserve | 0.5 vCPU | ~768 MB | 3-8 GB | Container runtime, logs, images and backup headroom. |
| **Recommended host** | **2 vCPU** | **4 GB** | **10 GB** | Deliberate headroom for image build, updates and judge testing. |

Compose enforces 0.5 vCPU/512 MB for the frontend and 1 vCPU/768 MB for the backend. Storage quota and log rotation must be configured at the CCE platform/host layer.

## Scaling boundary

The budget is for the fixed synthetic judge workload, not a production school district. SQLite serialises writes and the backend is intentionally one worker, so horizontal replicas are not supported by the current persistence design. Before a multi-school pilot:

1. measure records per school, import frequency, concurrent users, Beacon requests and retention period;
2. move to a managed transactional database with tenant isolation and encrypted backups;
3. load-test API, database and Gemini quotas;
4. set per-school request and spending limits; and
5. derive CPU, memory and storage from observed p95 latency and growth.

## Service objectives for the synthetic demonstration

- All health checks become healthy within 60 seconds after launch.
- Six key frontend routes and two backend endpoints return HTTP 200 in the smoke test.
- Restarting the backend does not remove the persisted SQLite volume.
- A Gemini outage produces a safe provider error while deterministic dashboards remain usable.

These are release acceptance targets, not contractual availability guarantees.
