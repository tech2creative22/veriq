# Beacon Model Card

## Model and purpose

- Provider: Google Gemini Developer API.
- Configured model: `gemini-3.5-flash`.
- Application role: natural-language explanation and drafting over a precomputed school Evidence Package.
- Intended users: authorised school heads, deputy heads and heads of department in a controlled pilot.
- Decision role: advisory only; no automated disciplinary, exclusion, grading or high-stakes learner decision.

## Inputs

- The school leader's question, limited to 500 characters.
- Active scope: school, metric, class, learner, intervention or decision.
- Verified supporting evidence, signals, confidence, missing evidence, analysis ID and trace ID.
- An allowed recommendation-category list.

Raw CSV files, API keys and the SQLite database are not sent as prompt attachments.

## Outputs

- Situation.
- Why the evidence matters.
- Supporting evidence.
- Recommendation and suggested next step.
- Confidence explanation and missing evidence.
- Structured conversation or clarification where appropriate.

The application validates structure and presents verified Evidence Package facts alongside the generated language.

## Intended uses

- Explain connected attendance, behaviour and assessment changes.
- Answer evidence questions at a supported scope.
- Draft proportionate, reviewable next steps.
- Draft a Decision Brief for human ownership.

## Prohibited uses

- Predict or declare an official ZIMSEC result from internal scores.
- Diagnose a medical, psychological or safeguarding condition.
- Make an autonomous disciplinary or exclusion decision.
- Rank learners for punishment or deny an educational opportunity.
- Use unverified model claims as school records.
- Process real learner records in the current unauthenticated local MVP.

## Known risks

- Hallucinated or overconfident explanation.
- Scope confusion between school, class and learner.
- Automation bias by school staff.
- Prompt injection embedded in free-text data or questions.
- Provider outage, latency, quota or model-version change.
- Disparate impact if future real data reflects unequal reporting or access.

## Controls

- Deterministic source-of-truth calculations.
- Strict Evidence Package scope and trace IDs.
- Structured response schema and semantic grounding checks.
- Missing-evidence disclosure and safe clarification.
- No direct tools, database write access or autonomous action for the model.
- Human review and editable owner/status for Decision Briefs.
- Regression suite and planned repeated live-prompt evaluation.

## Evaluation status

The deterministic grounding/scope suite is recorded in `BEACON_TEST_RESULTS.json`. Dataset scenarios and hashes are recorded under `submission/dataset/`. Educator usability, live-model repetition, fairness on representative pilot data and production security testing remain pre-pilot gates.
