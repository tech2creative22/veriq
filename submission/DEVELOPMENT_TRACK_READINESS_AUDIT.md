# Veriq Development Track Submission Readiness Audit

**Source reviewed:** Terms of Reference: Track 3 (Development)  
**Audit date:** 14 July 2026  
**Product audited:** Veriq AI4Impact MVP

## Executive conclusion

Veriq belongs in the Development track. It is a functional AI-enabled educational decision-support MVP with a demonstrable workflow:

`CSV evidence -> deterministic validation and signals -> School Pulse -> learner monitoring -> grounded Beacon explanation -> Decision Brief`

The product is demonstrable, but the current submission package is not yet ready for the published scoring rubric. The strongest remaining work is submission evidence rather than additional UI.

## Current estimated rubric position

| Criterion | Weight | Current estimate | Main reason |
|---|---:|---:|---|
| C1 Technical Feasibility and Code Quality | 30 | 26-28 | Functional modular MVP, reproducible setup and as-built/API/environment documentation, pinned manifests, 29 backend tests, 35 browser checks, clean standalone production build, zero production dependency vulnerabilities and a CCE container/operations package; reduced by missing committed Git history and Docker-host/hosted deployment evidence. |
| C2 AI Justification and Fit-for-Purpose | 30 | 25-28 | Grounded Gemini workflow, rule-only baseline, AI/non-AI boundary, model trade-offs, model card, fallback behaviour and 23 passing control tests are documented. A timed educator study and repeated live semantic benchmark remain. |
| C3 Dataset Provenance and Synthetic Validation | 20 | 17-19 | The fictional dataset now has a deterministic generator, portable manifest with SHA-256 hashes, field dictionary, provenance/rights statement, limitations and a passing validation report executed through the production evidence engine. Final judge scoring may still expect validation on a larger representative pilot dataset. |
| C4 Business Model and Edge Feasibility | 20 | 13-15 | Customer/user, adoption path, pricing hypothesis, AI unit economics, 12-month cost envelope, scaling boundary and cloud/edge position are documented. Reduced because pricing has not been validated with schools, legal/security costs need quotations and there is no paid pilot evidence. |
| **Estimated total today** | **100** | **81-90** | Strong evidence package across technical delivery, AI, dataset, compliance, CCE and sustainability; Git history, Docker-host execution, customer validation, live semantic evaluation and the final proposal PDF/video remain incomplete. |

This is a conservative document-based estimate, not an official score.

## Minimum admissibility checklist

| Requirement | Status | Existing evidence | Required action |
|---|---|---|---|
| Clear Zimbabwe problem and intended users | Ready | AI4Impact overview and working school-leadership workflow | Condense into proposal Section 1 and identify headmasters, deputy heads and HODs explicitly. |
| Product description or working prototype | Ready | Production build and tested end-to-end MVP | Add demo URL, screenshots and a 3-5 minute demo script. |
| Technical architecture note | Ready | `docs/AS_BUILT_ARCHITECTURE.md` shows the implemented Next.js, FastAPI, SQLite, Gemini and CSV evidence flow. | Include it in the technical appendix and keep future architecture clearly labelled. |
| Dataset statement | Ready | Three CSVs, judge workbook, deterministic generator, portable manifest, schema/label dictionary, rights statement and machine-readable validation report | Include `submission/dataset/DATASET_PROVENANCE.md` and the validation report in the technical appendix. |
| User interaction plan | Ready | Upload, School Pulse, Early Intervention, Beacon and Decision Brief workflow | Add a one-page user journey to the proposal. |
| Material risk note | Ready for synthetic demo | Compliance/data-governance plan, demo notice, threat model and owned risk register cover privacy, model, security, data-quality and adoption risks. | Obtain legal and controller approval and close all listed pilot blockers before real learner data. |
| Business/sustainability note | Ready as hypothesis | Business/adoption model, pilot measures, proposed pricing, AI unit economics, 12-month cost envelope and commercial risks are documented. | Validate willingness to pay/support effort with schools and obtain legal/security/CCE quotations. |

## Technical delivery checklist

| Item | Status | Required evidence before submission |
|---|---|---|
| Build and demonstration documentation | Ready | Root README documents prerequisites, environment variables, install, build, run, test, upload and demo workflow. |
| Dependency stability | Ready/Partial | Frontend runtime dependencies are exactly pinned and `package-lock.json` is current; Python requirements are pinned. Add isolated Python environment setup evidence. |
| Unit and end-to-end testing | Ready | 29 backend tests and a 35-check visible production browser flow pass, including real synthetic upload, cross-workspace evidence, Beacon greeting, console/network checks and mobile overflow. See `submission/TEST_AND_RELEASE_REPORT.md`. |
| Security warning-free code | Ready | Next.js upgraded to 15.5.20, PostCSS locked to 8.5.10, `npm audit --omit=dev --audit-level=high --package-lock-only` reports zero vulnerabilities, and the production build plus 29 backend tests pass. See `submission/SECURITY_BASELINE.md`. |
| Git evidence | Partial/Blocked | A clean repository is initialised on `main`, ignore rules protect secrets/runtime data and the source package is staged. The honest initial commit awaits the applicant's real Git author name/email; a remote link is also required. No historical commits will be fabricated. |
| Environment template | Ready | Root and backend `.env.example` files contain safe variable names/placeholders only; configuration is documented in `docs/ENVIRONMENT_AND_CONFIGURATION.md`. |
| Deployment/CCE readiness | Partial | Non-root frontend/backend Dockerfiles, Compose topology, persistent volume, health checks, resource budget, operations runbook, smoke test and ZCHPC CCE roadmap are included. Docker is not installed on the current workstation, so image build/start must be verified on a Docker-capable host or CCE. |
| Live demo URL | Missing | Deploy the frontend and backend or provide an approved hosted demonstration route. |
| Asset and licence register | Partial | Project assets, direct libraries, Gemini/CCE terms and release blockers are registered. Applicant must confirm the legal owner and choose a project code licence before publication. |

## AI justification checklist

The proposal must clearly separate what ordinary software does from what Gemini does.

### Deterministic, non-AI responsibilities

- CSV schema validation and canonical storage.
- Attendance, behaviour and assessment calculations.
- Threshold-based signal severity.
- Evidence scoping and trace IDs.
- Persistence of analyses, conversations and decisions.
- Prevention of invented metrics by reattaching verified facts after model output.

### AI responsibilities that create additional value

- Natural-language questions across school, class, metric and learner scopes.
- Context-sensitive synthesis of several verified signals.
- Explanation of why a connected pattern matters to an educator.
- Selection of an allowed recommendation category.
- Conversational follow-up without requiring database or analytics expertise.
- Translation of evidence into a human-reviewable Decision Brief.

### AI evidence status

- Completed: rule-only alert/dashboard versus Beacon-assisted functional baseline.
- Completed: Gemini model rationale, alternatives, current pricing reference and structured-output fit.
- Completed: trade-offs and fallback behaviour when the model or internet is unavailable.
- Completed: explicit deterministic/AI boundary and model card.
- Completed: 23/23 evidence, scope, grounding and provider-boundary tests.
- Remaining final gate: repeated live semantic benchmark on the fixed judge dataset.
- Remaining pilot evidence: a timed educator task measuring interpretation time or comprehension.

## Dataset provenance checklist

The judge dataset is fictional and synthetic. It contains 20 first-name-only learners across Form 1A-Form 4A, 400 attendance records, 34 behaviour records and 400 internal continuous-assessment records. Provenance, generation and validation evidence is now recorded in `submission/dataset/`.

Completed evidence includes:

- Every CSV field, type and accepted value.
- A byte-reproducible deterministic scenario generator and SHA-256 manifest.
- Three connected high-attention cases, two watch cases and fifteen stable controls verified through the live evidence engine.
- Fictional identity, ownership and permitted-use statements.
- Explicit internal continuous-assessment and non-ZIMSEC-pass-rate limitations.
- Integrity checks by Form, period, subject, domain value and composite key.

## Compliance and risk checklist

Proposal Section 4 must cover at least:

- Zimbabwe Data Protection Act [Chapter 12:07] applicability.
- Lawful basis and school authority for processing learner records.
- Consent or acknowledgement checkbox implementation for demo uploads.
- Data minimisation and pseudonymous learner identifiers.
- Retention and deletion policy.
- Encryption in transit and at rest for a hosted pilot.
- Authentication, authorisation and school/tenant isolation planned for pilot use.
- API key and secret handling.
- Prompt injection, hallucination and over-reliance controls.
- Human review: Beacon recommends; school leadership decides.
- Incident response, audit logging and backup/recovery assumptions.
- Clear disclosure that the current local MVP is not yet production-authorised for real learner data.

Completed MVP evidence: `submission/compliance/COMPLIANCE_AND_DATA_GOVERNANCE.md`, `DEMO_DATA_NOTICE.md`, `RISK_REGISTER.md`, `docs/THREAT_MODEL.md`, `SECURITY.md`, and frontend/API enforcement of the synthetic-data acknowledgement. These controls support the demonstration boundary only; the documented legal, privacy and security gates remain mandatory before a real-data pilot.

## Required formal proposal

The submitted proposal must be PDF only, maximum 10 pages excluding cover and technical appendices, using Avenir or Arial 11 pt, 1.15 line spacing and 1-inch margins.

Required filename:

`[ProjectID]_AI4I_Proposal_Development.pdf`

Required structure:

1. Cover page: project, track, team, lead innovator and date.
2. Problem Definition and Strategic Alignment (1-2 pages).
3. Technical Design and Product Logic (2-3 pages).
4. Deliverables and CCE Implementation Roadmap (2 pages).
5. Compliance and Risk Mitigation (1-2 pages).
6. Sustainability and Future Adoption (1 page).

## Recommended submission package

- Formal proposal PDF with the exact required filename.
- Public or adjudicator-accessible Git repository link.
- Hosted demo URL.
- Short demo video as a reliability backup.
- Root README and reproducible build instructions.
- As-built architecture diagram.
- Dataset statement, schema and synthetic-validation report.
- Test report containing unit, build, lint, browser and security results.
- Asset/licence register.
- Risk and Data Protection compliance note.
- CCE deployment roadmap and compute requirements.
- Business model and cost projection.
- Judge dataset and backup screenshots.

## Recommended order of work

1. ~~Resolve the dependency security finding without breaking the production build.~~ Completed 14 July 2026.
2. Initialise Git, create the remote repository and make structured commits for all work from this point forward.
3. ~~Write the as-built README, architecture and `.env.example`.~~ Completed 14 July 2026.
4. ~~Produce the dataset provenance and synthetic-validation report.~~ Completed 14 July 2026.
5. ~~Write the AI necessity/baseline comparison and model trade-off note.~~ Completed 14 July 2026.
6. ~~Create compliance, consent and risk documentation; add the upload acknowledgement control.~~ Completed for the synthetic-data MVP on 14 July 2026; real-data pilot gates remain open.
7. ~~Create the CCE deployment plan and reproducible container/build configuration.~~ Completed as a reviewable package on 14 July 2026; container execution remains a final external-host gate.
8. ~~Create the business model, cost projection and licence register.~~ Completed as judge-review hypotheses on 14 July 2026; ownership/licence selection and market validation remain applicant gates.
9. Draft and render the formal 10-page proposal.
10. Deploy, record the demo, run the full test/audit suite and package final evidence.

## Information required from the applicant

- Project ID assigned by the challenge.
- Official team name.
- Lead innovator's full name.
- Team members and roles.
- Submission deadline.
- Available budget/currency assumptions.
- Preferred pilot school type and number of pilot schools.
- Repository hosting account/organisation.
- Intended demo hosting provider or CCE access details.
