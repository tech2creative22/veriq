# Veriq MVP Risk Register

**Scoring:** likelihood and impact are Low (L), Medium (M) or High (H). Residual ratings are targets after the listed mitigation. The product owner is accountable for closing all pilot gates.

| ID | Risk | Likelihood / impact | Current controls | Required mitigation and evidence | Owner | Residual target | Status |
|---|---|---|---|---|---|---|---|
| R1 | Real learner data is used without a confirmed lawful basis or authority. | M / H | Synthetic-only notice; UI and API acknowledgement. | Legal review, controller decision, privacy notice, DPA and documented lawful basis. | School controller + Product lead | L / H | Pilot blocker |
| R2 | Children's educational records are exposed. | M / H | Secrets excluded from Git; local-only demonstration. | Authentication, least-privilege RBAC, tenant isolation, TLS, encrypted storage, access logs and penetration test. | Security lead | L / H | Pilot blocker |
| R3 | Gemini or a cross-border provider receives excessive personal data. | M / H | Only bounded evidence is sent; raw CSV upload is not sent directly. | DPIA, provider/subprocessor review, transfer assessment, redaction, minimum fields and approved retention configuration. | DPO / Product lead | L / H | Pilot blocker |
| R4 | Beacon invents a metric or gives an unsupported explanation. | M / H | Deterministic metrics; scoped evidence; numeric grounding checks; 23 control tests. | Repeat live semantic benchmark, adversarial tests, monitoring and visible source-evidence links. | AI lead | L / M | In progress |
| R5 | Staff over-rely on AI and take harmful action. | M / H | Advisory wording; Decision Brief requires human workflow. | Training, review checklist, no automated significant decisions, escalation and appeal/correction route. | School head | L / H | Pilot blocker |
| R6 | Poor or incomplete uploads produce misleading patterns. | M / H | Required columns, domain checks and shared-class validation. | Completeness dashboard, duplicate/conflict handling, source-owner sign-off and quality thresholds. | Data steward | L / M | Partial |
| R7 | A learner is misidentified across source systems. | M / H | Stable learner IDs in judge data. | Authoritative ID mapping, collision tests, reconciliation report and correction workflow. | School data steward | L / H | Pilot blocker |
| R8 | API key or database contents leak through source control or logs. | M / H | `.env` and databases ignored; secret scan; safe error handling. | Managed secrets, rotation, log redaction, repository protection and incident runbook. | Security lead | L / H | Partial |
| R9 | One school can access another school's data. | M / H | Single-workspace local MVP avoids remote multi-tenancy. | Enforced tenant keys at every query, isolation tests and administrator audit. | Backend lead | L / H | Pilot blocker |
| R10 | Data cannot be corrected, exported or deleted promptly. | M / H | Local database can be manually removed. | Rights-request workflow, record lookup, export/correction/deletion tooling and backup expiry tests. | DPO + Backend lead | L / M | Pilot blocker |
| R11 | Service or Gemini outage interrupts school workflow. | M / M | Deterministic evidence remains available; provider errors are explicit. | Health checks, backups, retry/timeouts, offline evidence view, recovery objectives and tested restore. | Operations lead | L / M | Partial |
| R12 | Prompt injection in uploaded text manipulates Beacon. | M / H | Fixed schema and structured evidence context. | Treat all imported text as untrusted data, delimit content, restrict output schema, adversarial test and output policy validation. | AI + Security leads | L / M | In progress |
| R13 | Thresholds disadvantage a class or create stigma. | M / H | Signals combine domains and show evidence/confidence. | Subgroup/fairness review, educator feedback, periodic threshold validation and neutral language policy. | AI lead + School head | L / M | Pilot blocker |
| R14 | Unclear retention leads to excessive storage. | H / M | Synthetic-only MVP; local manual deletion. | Approved retention schedule, automated deletion, backup lifecycle and deletion evidence. | DPO / Operations | L / M | Pilot blocker |
| R15 | Licensing, registration or contractual obligations are missed. | M / H | Applicable instruments identified. | Zimbabwe legal review; POTRAZ determination; signed contracts and asset/licence register. | Product lead | L / H | Pilot blocker |

## Review cadence

- Reassess before every judge release and pilot deployment.
- Review high-impact risks after any architecture, model, dataset or provider change.
- Record the named person, due date and evidence link when real team roles are assigned.
- Stop processing real data if a pilot blocker is not closed or a high-severity incident occurs.
