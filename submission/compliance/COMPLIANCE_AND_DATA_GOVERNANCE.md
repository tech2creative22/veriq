# Veriq MVP Compliance and Data Governance

**Version:** 1.0  
**Review date:** 14 July 2026  
**Scope:** Development-track demonstration MVP

> This is an engineering compliance plan, not legal advice. A Zimbabwe-qualified legal review and a determination by the relevant school authority are mandatory before any pilot involving real learner records.

## Current operating boundary

The current Veriq MVP is approved only for fictional or synthetic demonstration data. It is not production-authorised for real learner records. The upload interface and API require the operator to acknowledge that they are authorised to use the files and that demonstration uploads must be synthetic. This acknowledgement is an operational safeguard; it is **not** learner or guardian consent and does not itself establish a lawful basis.

Beacon is decision support. It may explain verified evidence and draft a proposed action, but it does not make disciplinary, admission, grading, progression, employment or other decisions. A designated school leader must review the underlying evidence and accept, change or reject every recommendation.

## Legal and regulatory context

The applicable framework must be confirmed for the deployment, including:

- Zimbabwe's Cyber and Data Protection Act [Chapter 12:07], which covers personal information including educational history and provides additional relevance for children.
- The Postal and Telecommunications Regulatory Authority of Zimbabwe (POTRAZ) as the Data Protection Authority.
- Cyber and Data Protection (Licensing of Data Controllers and Appointment of Data Protection Officers) Regulations, 2024 (SI 155 of 2024), including whether the school and/or Veriq must register or obtain a licence and appoint a Data Protection Officer.

Authoritative references:

- [Cyber and Data Protection Act [Chapter 12:07]](https://zimlii.org/akn/zw/act/2021/5/eng%402022-03-11)
- [POTRAZ copy of the Act](https://www.potraz.gov.zw/wp-content/uploads/2022/02/Data-Protection-Act-5-of-2021.pdf)
- [SI 155 of 2024](https://www.potraz.gov.zw/wp-content/uploads/2025/02/sI-155-of-2024-Cyber-and-Data-Protection-Normal_240913_1250178.pdf)

## Proposed accountability model for a pilot

This allocation is provisional and must be recorded in a signed Data Processing Agreement (DPA).

| Party | Proposed role | Main responsibility |
|---|---|---|
| Participating school or responsible authority | Data controller | Determines purpose and lawful basis; issues notices; handles rights requests; approves users and decisions. |
| Veriq operator | Data processor, unless it determines an independent purpose | Processes only documented instructions; secures the service; supports deletion, access, audit and incidents. |
| Google Gemini service | Sub-processor/provider, subject to contract and deployment configuration | Processes the minimum grounded context needed for an explanation; terms, retention and transfer location require review. |

## Data lifecycle and minimisation

| Stage | MVP behaviour | Required pilot control |
|---|---|---|
| Collect | Three CSVs: attendance, behaviour and internal assessments. | Publish purpose and field list; reject unnecessary fields; use stable pseudonymous learner IDs. |
| Validate | Deterministic schema/domain checks before analysis. | Add malware/content scanning, size limits and administrator-only imports. |
| Store | Raw CSVs and normalised records in local SQLite. | Encrypted managed storage, school/tenant isolation, backups, access logging and defined regional location. |
| Analyse | Python calculates metrics, thresholds and evidence. | Version rules; monitor data quality and bias; document change approval. |
| Explain | Gemini receives a bounded evidence package, not the raw CSV files. | Contract/provider review, transfer assessment, redaction and no-training/retention configuration where available. |
| Decide | Human reviews Beacon output and may create a Decision Brief. | Record reviewer, evidence version, rationale, outcome, appeal/correction path and review date. |
| Retain/delete | Local records persist until the local database is removed. | Adopt a documented schedule; delete raw imports after the minimum operational period; support verified erasure and backup expiry. |

The MVP does not yet claim a production retention period. A pilot schedule should be approved before collection, with different periods for raw imports, derived evidence, conversations, decisions, security logs and backups.

## Data-subject rights readiness

Before real data is used, the school must provide an understandable privacy notice and a route for learners or authorised representatives to request access, correction, objection or deletion where applicable. Veriq must be able to find records by pseudonymous identifier, export relevant records, correct source data through a controlled re-import, and propagate deletions through primary storage and backups according to the approved schedule.

## AI safeguards

- Metrics and severity are calculated deterministically; Gemini does not calculate the official values.
- Prompts receive a scoped, verified Evidence Package and are instructed not to invent facts.
- Responses expose trace and analysis context, verified evidence and confidence from the evidence engine.
- Unknown learners, stale analysis contexts and unverified numeric claims are rejected or corrected.
- Provider failure produces an explicit safe error; it does not silently substitute fabricated advice.
- No recommendation may be treated as a solely automated decision with legal or similarly significant effect.
- Educators must inspect source records and apply professional judgement before action.

## Pre-pilot approval gates

Real learner data must remain prohibited until all gates are evidenced:

1. Controller/processor roles, lawful basis and POTRAZ registration/licensing applicability confirmed in writing.
2. DPO/contact owner, privacy notice, DPA and data-subprocessor register approved.
3. Data Protection Impact Assessment completed, including children's data and Gemini/cross-border processing.
4. Authentication, role-based access, tenant isolation, encryption, audit logs and tested backup/restore deployed.
5. Retention, correction, export, deletion, incident response and breach-notification procedures tested.
6. Educator training, human-review workflow, appeal/escalation route and acceptable-use policy signed off.
7. Security and privacy testing completed with no unresolved high-severity finding.

## Evidence included in this repository

- Upload acknowledgement enforced in `app/upload/page.tsx` and `backend/app/main.py`.
- API acknowledgement test in `backend/tests/test_imports.py`.
- Synthetic dataset provenance and validation in `submission/dataset/`.
- AI model boundary, safeguards and evaluation in `submission/ai/`.
- Security baseline in `submission/SECURITY_BASELINE.md`.
- Threat model in `docs/THREAT_MODEL.md`.
- Risk ownership and mitigations in `submission/compliance/RISK_REGISTER.md`.
