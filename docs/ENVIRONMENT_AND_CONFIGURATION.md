# Environment and Configuration

## Frontend

Create `.env.local` from the root `.env.example`.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `NEXT_PUBLIC_VERIQ_API_URL` | No | `http://localhost:8000` | Browser-visible FastAPI base URL. It must be reachable by the user's browser. |

Because the variable is prefixed with `NEXT_PUBLIC_`, it must never contain a secret.

## Backend

Create `backend/.env` from `backend/.env.example`.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `GEMINI_API_KEY` | For generative Beacon responses | None | Server-only Google Gemini credential. |
| `GEMINI_MODEL` | No | `gemini-3.5-flash` | Gemini model used for grounded explanation. |
| `VERIQ_DB_PATH` | No | `backend/data/veriq_mvp.db` | Absolute or process-relative SQLite database path. |
| `VERIQ_ALLOWED_ORIGINS` | No | Localhost ports shown below | Comma-separated exact frontend origins accepted by CORS. Do not use a wildcard for a real-data pilot. |

`backend/.env` and all `.env.*` files except examples are ignored by Git. The API key must be provided by the runtime secret manager in a hosted deployment.

## Local ports and origins

| Service | Port | URL |
|---|---:|---|
| Next.js | 3000 | `http://localhost:3000` |
| FastAPI | 8000 | `http://127.0.0.1:8000` |
| FastAPI health | 8000 | `http://127.0.0.1:8000/health` |
| OpenAPI UI | 8000 | `http://127.0.0.1:8000/docs` |

The default accepts browser API requests only from `http://localhost:3000` and `http://127.0.0.1:3000`. Set `VERIQ_ALLOWED_ORIGINS` to the exact HTTPS frontend origin or comma-separated origins for a hosted deployment.

`NEXT_PUBLIC_VERIQ_API_URL` is embedded into the browser bundle at frontend build time. Set the correct externally reachable HTTPS API URL before `npm run build` or the container image build.

## Data paths

- The default database is `backend/data/veriq_mvp.db`.
- Database files and runtime uploads are excluded from Git.
- The committed `demo-data/` and `sample-data/` files are fictional demonstration data.
- Set `VERIQ_DB_PATH` to a writable persistent volume for a container or CCE deployment.

## Container configuration

`docker-compose.yml` builds the locked Next.js standalone image and FastAPI image, persists `/data`, applies demonstration CPU/memory limits and defines service health checks. Use `deployment/cce.env.example` as the safe variable template. The Gemini key is a runtime backend secret; it is never passed into the frontend image build.

## Configuration validation

- Without `GEMINI_API_KEY`, deterministic evidence pages continue to work and generative requests return `GEMINI_NOT_CONFIGURED` with HTTP 503.
- If Gemini cannot provide a safely grounded response, the API returns `BEACON_RESPONSE_UNAVAILABLE` with HTTP 502.
- If the frontend holds an outdated analysis ID after a new import, the API returns `ANALYSIS_CONTEXT_CHANGED` with HTTP 409.
