# Security Policy

## Supported status

Veriq is currently a Development-track MVP intended for synthetic demonstration data. It is not approved for real learner records or production operation.

## Reporting a vulnerability

Do not include personal data, API keys or exploit details in a public issue. Report the affected component, version, reproduction steps and impact privately to `praisegodchaps@gmail.com`.

## Response targets

| Severity | Initial acknowledgement target | Action |
|---|---:|---|
| Critical | 24 hours | Stop affected processing, rotate exposed secrets, preserve logs and begin containment. |
| High | 2 business days | Triage, mitigate exposure and prepare a tested patch. |
| Medium/Low | 5 business days | Record, prioritise and include in a planned update. |

These are team targets, not a contractual service-level agreement.

## Safe handling

- Never commit `.env` files, API keys, databases or uploaded CSVs containing real people.
- Use the included synthetic judge dataset for testing.
- Rotate a key immediately if it may have been exposed.
- Re-run dependency, secret, test and production-build checks before every release.
- Follow `submission/compliance/COMPLIANCE_AND_DATA_GOVERNANCE.md` before considering a real-data pilot.
