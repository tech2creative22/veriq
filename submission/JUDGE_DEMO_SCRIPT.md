# Veriq Judge Demo Script

**Target duration:** 4 minutes 30 seconds  
**Dataset:** committed fictional Zimbabwe secondary-school judge CSVs only

## Before the demonstration

1. Start backend and production frontend; run `python scripts/smoke_test.py`.
2. Confirm the Gemini key without displaying it.
3. Open `/upload`; keep the three CSV paths ready.
4. Close terminals or files that could reveal secrets.
5. Keep the release screenshots and short backup recording available.

## 0:00-0:30 - Frame the problem

Say:

> School leaders already have attendance, behaviour and internal-assessment records, but those signals are reviewed separately. Veriq helps leadership see connected patterns early, understand the verified evidence and assign a human-owned response. Today I am using fictional data only.

## 0:30-1:05 - Prove the data boundary

- Show the three required CSV cards on **Upload data**.
- Point to the data-use acknowledgement and explain that the API also enforces it.
- Select attendance, behaviour and assessments, acknowledge synthetic use, then analyse.
- Point out `20 learners across 4 classes` and the new analysis identifier.

Judge message: this is one persistent evidence package, not independent mock values on each screen.

## 1:05-1:50 - Show the whole school

- Open **School Pulse**.
- Point to source, coverage, reporting period and analysis ID.
- Explain the whole-school attendance, behaviour, assessment and school-health indicators.
- Show every class and the monitored learner distribution.
- Use one **Ask Beacon** action to demonstrate that the selected metric/class becomes Beacon's scope.

Judge message: a head can move from school health to the class or learner behind it without losing evidence context.

## 1:50-2:30 - Show early monitoring

- Open **Early Intervention**.
- Identify the connected high-attention cases and a single-signal watch case.
- Open one learner/class case and point to the exact attendance, behaviour and assessment movements.
- Explain that the system monitors different patterns rather than giving every learner the same template.

Judge message: deterministic rules find and rank the signals before any LLM explanation.

## 2:30-3:35 - Show Beacon's AI value

- Open **Beacon** and first type `hello` to show a natural greeting.
- Ask: `Give me Chipo's current performance and tell me what should be verified before action.`
- Point to the resolved learner scope, traceable evidence, confidence and missing-evidence statement.
- Ask a different learner question if time permits and show that facts differ.
- State: Python calculates the values; Gemini explains a bounded Evidence Package. Beacon cannot invent an official pass rate or make the final decision.

Judge message: AI adds accessible synthesis and follow-up while verified metrics remain deterministic.

## 3:35-4:10 - Convert evidence into accountability

- Choose **Create scoped Decision Brief**.
- Show the recommendation, evidence, owner, due/review dates, success target and human-review statement.
- Assign the owner only after explaining that leadership can accept, modify or reject the recommendation.

Judge message: the workflow ends in accountable human action, not a chatbot answer.

## 4:10-4:30 - Close with deployment and sustainability

Say:

> The MVP has 29 backend tests, 23 AI-control checks and a 35-check browser flow. It is packaged for a two-container CCE deployment and costs about 0.75 US cents per planned Beacon interaction at the documented token assumption. The current release is synthetic-data-only; authentication, tenant isolation and the legal/privacy gates are explicit before a real-data pilot.

## Failure-safe demonstration

- If Gemini is unavailable, show School Pulse and Early Intervention, then explain the visible provider error and use the saved Beacon screenshot. Never claim the screenshot is a new live answer.
- If hosting is unavailable, run the local production build and use the backup video.
- If an import fails, read the validation message, correct the selected file and do not switch to hidden mock data.
