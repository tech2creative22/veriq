# Veriq MVP Threat Model

## Scope and trust boundaries

The assessed path is browser -> Next.js frontend -> FastAPI API -> SQLite and, for Beacon explanations, FastAPI -> Gemini API. CSV files and their text fields are untrusted input. The browser, API, local database and external AI provider are separate trust zones.

## Protected assets

- Learner identifiers and attendance, behaviour and assessment records.
- Evidence Packages, Beacon conversations and Decision Briefs.
- Gemini API key and deployment configuration.
- School/workspace identity, audit information and availability.
- Integrity of calculated metrics, scopes and human decisions.

## Main threats and required controls

| Threat | Current MVP control | Production/pilot requirement |
|---|---|---|
| Malicious or malformed CSV | Extension, required-column, domain, date and score validation. | File-size/rate limits, content and malware scan, streaming parser, duplicate/conflict policy. |
| Broken access control | Local single-user demonstration. | Identity provider, MFA for administrators, RBAC, tenant-scoped queries and automated isolation tests. |
| Injection into prompts | Structured, scoped Evidence Package; deterministic grounding. | Delimit untrusted fields, restricted output schema, adversarial prompt suite and model-output policy check. |
| Secret disclosure | Environment files ignored; example files contain placeholders; safe provider errors. | Managed secrets, least privilege, rotation, egress controls, log redaction and repository secret scanning in CI. |
| Data disclosure in transit/storage | Local development boundary. | TLS everywhere, encrypted managed volumes/backups, key management and auditable access. |
| Tampering with evidence | Trace/analysis IDs and deterministic calculations. | Signed/versioned imports, immutable audit events, database integrity controls and reviewer attribution. |
| Replay/stale context | API rejects a mismatched analysis ID for Beacon. | Session controls, idempotency, freshness display and concurrency tests across all write operations. |
| Denial of service or cost abuse | Bounded input and short model workflow. | Authentication, quotas, request/body limits, timeouts, rate limits, budget alerts and circuit breaker. |
| Supply-chain compromise | Pinned manifests; production audit currently clean. | Dependabot-equivalent monitoring, CI audit/SBOM, signed builds and controlled updates. |
| Data loss | Local database persists between runs. | Encrypted backups, defined RPO/RTO, restore tests and monitored health checks. |

## Security acceptance boundary

The present controls support a synthetic-data demonstration only. Real-data deployment is rejected until authentication, authorisation, tenant isolation, encryption, audit, retention/deletion, backup/restore, incident response and security testing have been implemented and evidenced.
