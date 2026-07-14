# VERIQ 48-HOUR EXECUTION PLAN

**Document ID:** VER-AI4I-013  
**Version:** 1.0  
**Status:** Active  
**Owner:** Founders  
**Start Date:** 11 July 2026  
**Internal Completion Deadline:** 12 July 2026  
**Submission Deadline:** 14 July 2026  
**Classification:** Internal  

---

# Purpose

This document defines the frontend and backend execution plan for completing the Veriq AI4Impact MVP within the available time.

It is the active implementation contract for the competition build.

The frontend defines the experience judges will see.

The backend provides the real data analysis, grounded AI and Decision Intelligence behind that experience.

Both must converge into one complete vertical slice.

---

# Mission

Deliver a beautiful, reliable and understandable Veriq demonstration that proves:

1. Veriq understands what is happening in a school today.
2. Veriq identifies emerging problems before they become worse.
3. Veriq recommends practical interventions using real AI.

---

# Primary Demo Journey

The complete MVP must support this journey:

```text
Open Veriq

↓

View School Pulse

↓

Upload School Data

↓

Validate Attendance, Behaviour and Assessment Files

↓

Calculate Verified Metrics

↓

Detect Combined Educational Signals

↓

Generate Grounded AI Analysis

↓

Display Early Intervention

↓

Ask Beacon Follow-Up Questions

↓

Generate a Decision Brief
```

Anything that does not strengthen this journey is deferred.

---

# Execution Principle

The implementation follows a frontend-first vertical-slice approach.

```text
Frontend Experience

↓

Mock Data Contract

↓

Backend Implementation

↓

Real AI Connection

↓

End-to-End Testing

↓

Demo Recording
```

Frontend-first does not mean completing the entire frontend before starting the backend.

It means defining the visible experience first, then immediately connecting the required backend capabilities.

---

# MVP Screen Scope

The working MVP contains four essential experiences.

## 1. School Pulse

Answers:

> What deserves my attention today?

---

## 2. Early Intervention

Answers:

> What is beginning to go wrong before it becomes worse?

---

## 3. Beacon

Answers:

> Why was this identified, and what should we do?

---

## 4. Decision Brief

Answers:

> What action should now be owned, measured and followed up?

---

# Deferred Screens

The following screens may remain visually complete but do not require full backend functionality before submission:

- Reports
- Settings
- Full Decisions Management
- User Management
- Notifications
- School Configuration
- Historical Analytics

They must not delay the core AI journey.

---

# Technology Scope

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Lucide icons

## Backend

- FastAPI
- Python
- Pydantic
- pandas
- Gemini model connector

## Data

- Prepared CSV files
- In-memory analysis or lightweight Supabase persistence
- Supabase only where it directly supports the demo

## Deployment

- Vercel for the Next.js frontend
- Lightweight FastAPI deployment where practical
- Local or alternative hosted backend if deployment time becomes a risk

---

# Part One — Frontend Execution Plan

# Frontend Objective

Create a polished AI-native experience that makes the judges understand Veriq immediately.

The frontend should feel like an intelligent workspace rather than a traditional analytics dashboard.

Beacon must be present throughout the experience.

---

# Frontend Rule

Every primary screen must contain:

```text
Page Question

↓

Beacon Brief

↓

Important Evidence

↓

Recommended Action

↓

Supporting Metrics
```

Metrics support intelligence.

They do not replace intelligence.

---

# Frontend Folder Structure

```text
frontend/

├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   │
│   ├── school-pulse/
│   │   └── page.tsx
│   │
│   ├── early-intervention/
│   │   └── page.tsx
│   │
│   ├── beacon/
│   │   └── page.tsx
│   │
│   ├── decisions/
│   │   └── page.tsx
│   │
│   └── upload/
│       └── page.tsx
│
├── components/
│   ├── layout/
│   │   ├── app-sidebar.tsx
│   │   ├── app-header.tsx
│   │   └── page-container.tsx
│   │
│   ├── beacon/
│   │   ├── beacon-brief.tsx
│   │   ├── beacon-panel.tsx
│   │   ├── beacon-message.tsx
│   │   ├── beacon-thinking.tsx
│   │   └── suggested-questions.tsx
│   │
│   ├── school-pulse/
│   │   ├── pulse-metric.tsx
│   │   ├── daily-priority.tsx
│   │   └── pulse-summary.tsx
│   │
│   ├── intervention/
│   │   ├── intervention-hero.tsx
│   │   ├── signal-item.tsx
│   │   ├── evidence-list.tsx
│   │   ├── intervention-action.tsx
│   │   └── confidence-indicator.tsx
│   │
│   ├── decisions/
│   │   ├── decision-brief.tsx
│   │   ├── decision-status.tsx
│   │   └── decision-owner.tsx
│   │
│   ├── upload/
│   │   ├── file-upload-card.tsx
│   │   ├── import-status.tsx
│   │   └── validation-result.tsx
│   │
│   └── ui/
│
├── lib/
│   ├── api.ts
│   ├── demo-data.ts
│   ├── formatters.ts
│   └── types.ts
│
├── styles/
│   └── globals.css
│
└── public/
```

---

# Frontend Phase F1 — Foundation

## Objective

Build the visual shell shared by all screens.

## Deliverables

- Global layout
- Dark navigation sidebar
- Header
- Page container
- Design tokens
- Typography
- Shared spacing
- Shared buttons
- Shared card surfaces
- Responsive layout foundation

## Visual Tokens

```text
Midnight Navigation:
#08111F

Workspace:
#F6F8FB

Card:
#FFFFFF

Primary Text:
#101828

Secondary Text:
#667085

Border:
#E8ECF3

Platform Blue:
#2F6BFF

Beacon Purple:
#6D4AFF

Healthy Green:
#18A673

Opportunity Amber:
#F59E0B

Critical Red:
#E5484D
```

## Success Criteria

- All routes share one consistent visual language.
- The product feels polished before backend integration.
- Beacon purple is reserved for intelligence.
- The interface does not resemble a generic KPI dashboard.

---

# Frontend Phase F2 — School Pulse

## Objective

Build the opening experience shown to judges.

## Screen Question

> What deserves my attention today?

## Required Content

### Greeting

```text
Good morning, James.

I've reviewed today's school activity.
Three things deserve your attention.
```

### Beacon Brief

Beacon must be visually more important than the metrics.

Example:

```text
One pattern deserves your attention.

Grade 7A attendance has declined over four weeks while
Mathematics performance and homework completion have also fallen.

There is still a strong opportunity to intervene.
```

### Supporting Metrics

- Attendance
- Behaviour
- Assessment status
- Learners requiring attention

### Primary Action

```text
View Early Intervention
```

### Data Upload Entry Point

A visible but secondary action:

```text
Upload latest school data
```

## Success Criteria

- Judges understand the school situation within 30 seconds.
- Beacon appears immediately.
- The main insight is larger than all metrics.
- One click opens the Early Intervention experience.

---

# Frontend Phase F3 — Upload Experience

## Objective

Allow prepared CSV files to be submitted for real analysis.

## Required Inputs

- Attendance CSV
- Behaviour CSV
- Assessments CSV

## Required States

### Empty

```text
Upload school data to generate today's intelligence.
```

### Uploading

```text
Uploading attendance...
Uploading behaviour...
Uploading assessments...
```

### Validating

```text
Validating file structure...
Checking required fields...
Reviewing data quality...
```

### Analysing

```text
Beacon is understanding your school...

✓ Attendance reviewed
✓ Behaviour reviewed
✓ Assessments reviewed
✓ Educational signals connected
✓ Decision Intelligence prepared
```

### Success

```text
Analysis complete.

One early intervention opportunity was identified.
```

### Failure

Explain:

- Which file failed
- Why it failed
- What must be corrected

## Success Criteria

- Three files can be selected.
- The user understands every processing step.
- No generic loading spinner is used.
- Successful analysis routes to Early Intervention.

---

# Frontend Phase F4 — Early Intervention

## Objective

Show how Veriq detects an emerging problem before it becomes worse.

## Screen Question

> What is beginning to go wrong?

## Hero Insight

```text
Grade 7A

High Intervention Opportunity

The next one to two weeks present a strong opportunity
to improve attendance and academic performance.

Confidence: 87%
```

## Required Signals

- Attendance declined from 92% to 84%.
- Behaviour incidents increased from 2 to 9.
- Mathematics average declined by 7 percentage points.
- Homework completion declined by 12%.
- Eight learners have repeated absences.

## Required Sections

### Beacon Interpretation

A calm natural-language explanation.

### Key Evidence

Verified facts only.

### Why It Matters

Explain the combined pattern.

### Recommended Actions

- Meet the class teacher.
- Review repeated absentees.
- Contact parents.
- Provide targeted Mathematics support.

### Primary Action

```text
Create Decision Brief
```

### Secondary Actions

```text
Ask Beacon
Show detailed evidence
```

## Success Criteria

- The screen clearly demonstrates early intelligence.
- The evidence and recommendation are linked.
- No unsupported prediction is shown.
- The user can move directly into Beacon or create a Decision Brief.

---

# Frontend Phase F5 — Beacon

## Objective

Demonstrate a real AI conversation grounded in verified evidence.

## Screen Question

> Why has Veriq made this recommendation?

## Required Experience

Beacon must feel like an educational advisor, not a generic chatbot.

## Supported Demo Questions

```text
Why is Grade 7A being flagged?

What evidence supports this?

What should we do this week?

Which learners contribute most to the pattern?

Create a Decision Brief.
```

## Response Structure

Every important response follows:

```text
Situation

↓

Why It Matters

↓

Evidence

↓

Recommendation

↓

Confidence

↓

Next Step
```

## Required UI Elements

- Current intervention context
- Conversation history
- Evidence references
- Suggested follow-up questions
- Input field
- Thinking state
- Create Decision Brief action

## Success Criteria

- Responses are generated by a live LLM.
- Responses only use provided evidence.
- Beacon never invents numbers.
- Beacon admits when evidence is insufficient.
- Follow-up questions preserve the current analysis context.

---

# Frontend Phase F6 — Decision Brief

## Objective

Convert intelligence into a structured, actionable Decision.

## Required Fields

```text
Decision Title

Situation

Evidence Summary

Recommendation

Priority

Confidence

Owner

Due Date

Success Metric

Review Date

Status
```

## Example

```text
Decision:
Grade 7A Attendance and Mathematics Intervention

Priority:
High

Owner:
Deputy Head

Recommendation:
Meet the Grade 7A teacher and contact parents of the
eight learners with repeated absences.

Success Metric:
Attendance returns to 90% or above before the next assessment.

Confidence:
87%
```

## Required Actions

```text
Accept Decision

Edit Owner

Mark In Progress
```

For the MVP, these actions may update local state without requiring a complex workflow backend.

## Success Criteria

- Judges see intelligence become accountability.
- Every recommendation has an owner and measurable outcome.
- The Decision Brief can be created from Beacon or Early Intervention.

---

# Frontend Types

The frontend should use one shared contract.

```typescript
export interface SchoolPulse {
  attendanceRate: number;
  behaviourIncidentCount: number;
  assessmentSubmissionRate: number;
  repeatedAbsenteeCount: number;
  primaryInsight: string;
}

export interface Signal {
  id: string;
  category: "attendance" | "behaviour" | "assessment" | "homework";
  title: string;
  currentValue: number;
  previousValue: number;
  change: number;
  severity: "low" | "medium" | "high";
  evidenceText: string;
}

export interface EarlyIntervention {
  id: string;
  className: string;
  title: string;
  summary: string;
  riskLevel: "low" | "medium" | "high";
  interventionOpportunity: "low" | "medium" | "high";
  confidence: number;
  signals: Signal[];
  recommendedActions: string[];
}

export interface DecisionBrief {
  id: string;
  title: string;
  situation: string;
  evidenceSummary: string[];
  recommendation: string;
  priority: "low" | "medium" | "high" | "critical";
  confidence: number;
  owner: string;
  successMetric: string;
  dueDate: string;
  status: "draft" | "open" | "in_progress" | "completed";
}
```

---

# Frontend API Contract

## Analyse Files

```text
POST /api/v1/intelligence/analyze
```

Input:

```text
multipart/form-data

attendance_file

behaviour_file

assessments_file
```

Response:

```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis_demo_001",
    "school_pulse": {},
    "interventions": [],
    "primary_intervention": {},
    "beacon_brief": ""
  },
  "trace_id": "trace_001"
}
```

---

## Ask Beacon

```text
POST /api/v1/beacon/query
```

Request:

```json
{
  "analysis_id": "analysis_demo_001",
  "question": "Why is Grade 7A being flagged?"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "answer": "",
    "evidence_ids": [],
    "confidence": 0.87,
    "suggested_questions": []
  },
  "trace_id": "trace_002"
}
```

---

## Generate Decision Brief

```text
POST /api/v1/decisions/generate
```

Request:

```json
{
  "analysis_id": "analysis_demo_001",
  "intervention_id": "intervention_grade_7a"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "decision": {}
  },
  "trace_id": "trace_003"
}
```

---

# Part Two — Backend Execution Plan

# Backend Objective

Provide a small but real intelligence pipeline that processes educational data, calculates verified metrics and grounds live LLM responses.

The backend should be simple, deterministic where possible and narrowly focused on the demo.

---

# Backend Rule

The LLM interprets verified evidence.

The LLM does not calculate school metrics.

```text
CSV Data

↓

Python Calculations

↓

Structured Evidence

↓

LLM Interpretation

↓

Decision Intelligence
```

---

# Backend Folder Structure

```text
backend/

├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── intelligence.py
│   │       ├── beacon.py
│   │       └── decisions.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── logging.py
│   │
│   ├── schemas/
│   │   ├── analysis.py
│   │   ├── beacon.py
│   │   ├── decision.py
│   │   └── responses.py
│   │
│   ├── services/
│   │   ├── csv_validation_service.py
│   │   ├── metrics_service.py
│   │   ├── signal_detection_service.py
│   │   ├── evidence_service.py
│   │   ├── llm_service.py
│   │   ├── beacon_service.py
│   │   └── decision_service.py
│   │
│   ├── prompts/
│   │   ├── beacon_system_prompt.md
│   │   └── decision_prompt.md
│   │
│   ├── demo/
│   │   ├── cache.py
│   │   └── prepared_results.json
│   │
│   └── tests/
│       ├── test_metrics.py
│       ├── test_signal_detection.py
│       ├── test_analysis_api.py
│       └── test_beacon_api.py
│
├── requirements.txt
├── Dockerfile
└── .env.example
```

---

# Backend Phase B1 — FastAPI Foundation

## Objective

Create a running API service.

## Deliverables

- FastAPI application
- CORS configuration
- Environment variables
- Health endpoint
- Standard response models
- Trace ID generation
- Basic error handling

## Endpoint

```text
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

## Success Criteria

- Backend starts locally.
- Frontend can call it.
- Errors return predictable responses.
- OpenAPI documentation loads.

---

# Backend Phase B2 — CSV Validation

## Objective

Support three prepared data schemas.

## Attendance Schema

```csv
student_id,class_name,date,status
```

Allowed status values:

```text
present
absent
late
excused
```

---

## Behaviour Schema

```csv
student_id,class_name,date,incident_type,severity
```

Allowed severity values:

```text
low
medium
high
```

---

## Assessment Schema

```csv
student_id,class_name,subject,date,score
```

Score range:

```text
0–100
```

---

## Validation Requirements

Validate:

- File is present.
- Required columns exist.
- Dates are valid.
- Scores are valid.
- Status values are supported.
- Class names exist.
- Files contain records.

## Success Criteria

- Correct demo files pass.
- Incorrect files produce understandable errors.
- Validation never silently removes invalid rows.

---

# Backend Phase B3 — Deterministic Metrics

## Objective

Calculate all numerical facts without using the LLM.

## Required Metrics

### Attendance

- Current attendance rate
- Previous attendance rate
- Four-week trend
- Repeated absentee count
- Class-level attendance changes

### Behaviour

- Current incident count
- Previous incident count
- Incident change
- Severity distribution
- Class-level incident concentration

### Assessments

- Current subject average
- Previous subject average
- Average change
- Class and subject-level trends

## Expected Demo Result

```json
{
  "class_name": "Grade 7A",
  "attendance": {
    "previous_rate": 92,
    "current_rate": 84,
    "change": -8
  },
  "behaviour": {
    "previous_incidents": 2,
    "current_incidents": 9,
    "change": 7
  },
  "mathematics": {
    "previous_average": 68,
    "current_average": 61,
    "change": -7
  },
  "repeated_absentees": 8
}
```

## Success Criteria

- Metrics match expected demo values.
- Results are reproducible.
- Unit tests verify calculations.
- No LLM is used for arithmetic.

---

# Backend Phase B4 — Signal Detection

## Objective

Convert metrics into structured signals.

## Initial Rules

### Attendance Signal

```text
If attendance change <= -5 percentage points:
    medium signal

If attendance change <= -8 percentage points:
    high signal
```

### Behaviour Signal

```text
If incidents increase by 3 or more:
    medium signal

If incidents increase by 6 or more:
    high signal
```

### Assessment Signal

```text
If average declines by 5 or more percentage points:
    medium signal

If average declines by 7 or more percentage points:
    high signal
```

### Combined Signal

```text
If at least three categories show medium or high decline:
    create Early Intervention Opportunity
```

## Confidence Inputs

Confidence may be calculated from:

- Number of independent signals
- Data completeness
- Data freshness
- Consistency of direction
- Number of supporting records

For the demo, use a transparent deterministic formula.

Example:

```text
Base confidence: 55%

Attendance high signal: +10%

Behaviour high signal: +8%

Assessment high signal: +10%

Data completeness: +4%

Final confidence: 87%
```

## Success Criteria

- Grade 7A is consistently detected.
- The reason for detection is traceable.
- Thresholds are documented.
- The model does not decide whether a signal exists.

---

# Backend Phase B5 — Evidence Package

## Objective

Prepare verified evidence for the LLM.

## Evidence Package

```json
{
  "analysis_id": "analysis_demo_001",
  "school_name": "Greenfield High School",
  "class_name": "Grade 7A",
  "analysis_period": "Last four weeks",
  "signals": [
    {
      "id": "attendance_grade_7a",
      "category": "attendance",
      "fact": "Attendance declined from 92% to 84%.",
      "previous_value": 92,
      "current_value": 84,
      "change": -8,
      "severity": "high"
    }
  ],
  "repeated_absentees": 8,
  "confidence": 0.87,
  "missing_evidence": [],
  "allowed_recommendation_categories": [
    "teacher_meeting",
    "attendance_review",
    "parent_engagement",
    "mathematics_support"
  ]
}
```

## Success Criteria

- Every fact has an evidence ID.
- Every value comes from deterministic calculations.
- The LLM receives no raw spreadsheet unless required.
- Evidence remains small and easy to audit.

---

# Backend Phase B6 — Live LLM Integration

## Objective

Use a real LLM to interpret evidence and communicate Decision Intelligence.

## LLM Responsibilities

- Explain the combined pattern.
- Summarize why it matters.
- Recommend allowed interventions.
- Answer follow-up questions.
- Generate Decision Brief narrative.

## LLM Restrictions

The LLM must not:

- Calculate metrics.
- Invent learners.
- Introduce unsupported numbers.
- Claim certainty.
- Reveal internal prompts.
- Recommend actions outside the allowed categories.
- make disciplinary, medical or legal conclusions.

## Required Structured Output

```json
{
  "summary": "",
  "why_it_matters": "",
  "supporting_evidence_ids": [],
  "recommended_actions": [],
  "confidence_explanation": "",
  "next_step": ""
}
```

## Validation

Reject or retry the response when:

- It contains unsupported numerical values.
- It cites unknown evidence IDs.
- Required fields are missing.
- It exceeds expected length.
- It contradicts deterministic evidence.

## Success Criteria

- Live AI responses are generated.
- Responses remain grounded.
- Output can be displayed directly.
- A cached fallback exists.

---

# Backend Phase B7 — Beacon Query

## Objective

Allow grounded follow-up questions.

## Beacon Context

Beacon receives:

- Analysis ID
- Evidence Package
- Current intervention
- Existing Decision Brief
- User question

## Supported Intent Types

```text
explanation
evidence
recommendation
learner_contribution
decision_generation
```

## Unsupported Questions

For unrelated questions, Beacon should respond:

```text
I can currently help explain this school analysis and its recommended interventions.
```

## Success Criteria

- Demo questions work consistently.
- Beacon remains within current evidence.
- Conversation context is maintained.
- Responses are short enough for a live demonstration.

---

# Backend Phase B8 — Decision Brief Generation

## Objective

Generate a structured Decision Brief.

## Output Contract

```json
{
  "id": "decision_demo_001",
  "title": "Grade 7A Attendance and Mathematics Intervention",
  "situation": "",
  "evidence_summary": [],
  "recommendation": "",
  "priority": "high",
  "confidence": 0.87,
  "owner": "Deputy Head",
  "success_metric": "Attendance returns to 90% or above before the next assessment.",
  "due_date": "2026-07-18",
  "review_date": "2026-07-25",
  "status": "draft"
}
```

## Success Criteria

- Decision Brief is produced from the current intervention.
- Owner and metrics remain editable.
- The result can be rendered immediately.
- No complex persistence workflow is required for the MVP.

---

# Backend Phase B9 — Demo Cache and Failure Safety

## Objective

Prevent network or model failure from destroying the presentation.

## Required Modes

### Live Mode

Uses real LLM responses.

### Cached Mode

Returns the last valid result for the prepared evidence package.

### Recorded Backup

A local screen recording shows the complete workflow.

## Cache Requirements

Store:

- Last successful Beacon brief
- Last successful intervention explanation
- Last successful Decision Brief
- Suggested follow-up answers

## Success Criteria

- The demo remains usable if the LLM times out.
- Cached output is generated from the same evidence.
- Failover is silent and fast.
- The presenter always has a recorded backup.

---

# Frontend and Backend Integration Order

Integration must happen in this order:

```text
1. School Pulse displays mock data.

2. Early Intervention displays mock data.

3. Beacon displays mock answers.

4. Frontend types are locked.

5. Backend returns the same contract.

6. Mock School Pulse is replaced.

7. Mock Early Intervention is replaced.

8. Mock Beacon answers are replaced.

9. Decision Brief is connected.

10. Full workflow is tested.
```

---

# 48-Hour Work Schedule

# Day One — Frontend Experience and Backend Core

## Block 1 — Frontend Foundation

- Initialize Next.js.
- Add Tailwind CSS.
- Add shadcn/ui.
- Build sidebar.
- Build header.
- Add global tokens.
- Create routes.

## Block 2 — Core Screens

- Build School Pulse.
- Build Early Intervention.
- Build Beacon.
- Build Decision Brief.
- Use typed mock data.

## Block 3 — Backend Foundation

- Initialize FastAPI.
- Add health endpoint.
- Add CORS.
- Add CSV schemas.
- Add file validation.

## Block 4 — Deterministic Analysis

- Calculate attendance metrics.
- Calculate behaviour metrics.
- Calculate assessment metrics.
- Detect Grade 7A signals.
- Produce Evidence Package.

## End-of-Day Goal

```text
Beautiful frontend works with mock data.

Backend processes prepared CSV files and returns verified evidence.
```

---

# Day Two — Real AI, Integration and Submission

## Block 5 — LLM Integration

- Create system prompt.
- Add structured output.
- Add grounding validation.
- Generate Beacon explanation.
- Generate Decision Brief.

## Block 6 — Connect Frontend and Backend

- Connect upload.
- Connect analysis.
- Connect Early Intervention.
- Connect Beacon.
- Connect Decision Brief.

## Block 7 — Reliability

- Add cached results.
- Add error states.
- Add retry states.
- Test demo questions.
- Test full flow repeatedly.

## Block 8 — Submission Preparation

- Deploy frontend.
- Deploy backend.
- Verify production environment.
- Record backup demonstration.
- Capture screenshots.
- Prepare pitch.
- Submit before the deadline.

## End-of-Day Goal

```text
The full School Pulse → Early Intervention → Beacon → Decision Brief journey works.
```

---

# Priority Order

If time becomes limited, preserve work in this order:

```text
1. School Pulse

2. Early Intervention

3. Real Beacon explanation

4. Decision Brief

5. CSV upload

6. Visual polish

7. Secondary screens
```

The real AI explanation and Early Intervention journey must not be removed.

---

# Definition of Done

The MVP is complete when:

- School Pulse loads.
- The three CSV files upload.
- Data validation completes.
- Verified metrics are calculated.
- Grade 7A is flagged.
- Early Intervention displays evidence.
- Beacon answers using a live LLM.
- A Decision Brief is generated.
- The complete journey works in production.
- Cached backup responses exist.
- A backup video has been recorded.

---

# Non-Negotiable Rules

1. Do not add features outside this plan.
2. Do not build the full long-term architecture now.
3. Do not allow the LLM to invent metrics.
4. Do not sacrifice the real AI demonstration.
5. Do not delay deployment until everything feels perfect.
6. Do not depend entirely on live internet during the presentation.
7. Every hour must improve the demo, the AI or its reliability.

---

# Final Acceptance Test

A person unfamiliar with Veriq should be able to complete this journey without explanation:

```text
Open School Pulse

↓

Understand today's situation

↓

Upload data

↓

Watch Beacon analyse it

↓

Open the Grade 7A intervention

↓

Understand why it was flagged

↓

Ask Beacon what to do

↓

Generate a Decision Brief
```

After completing this journey, the person should understand:

> Veriq helps school leaders act before problems become results.

---

# Revision History

| Version | Date | Author | Notes |
|---|---|---|---|
| 1.0 | 11 July 2026 | Founders | Initial frontend and backend 48-hour execution plan |