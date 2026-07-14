# VERIQ MVP MILESTONE EXECUTION PLAN

**Document ID:** VER-OS-005

**Version:** 1.0

**Status:** Active

**Owner:** Product & Engineering

**Applies To:** AI4Impact MVP

**Last Updated:** 11 July 2026

---

# Purpose

This document controls the implementation order of the Veriq AI4Impact MVP.

Unlike architecture documents, this document is operational.

It answers one question:

> **What should be built right now?**

This document is the single source of truth for implementation order.

It prevents:

- feature creep
- overengineering
- milestone skipping
- building future functionality too early

If another document conflicts with this execution plan, the active milestone always wins during the MVP.

---

# Current Objective

Build a believable AI-native Educational Decision Intelligence platform that demonstrates how schools can detect problems before they become results.

The MVP should convince AI4Impact judges that Veriq provides practical decision support rather than another analytics dashboard.

---

# MVP Journey

Every milestone should strengthen this user journey.

```text
School Pulse

↓

Upload School Data

↓

Educational Analysis

↓

Early Intervention

↓

Beacon

↓

Decision Brief
```

Nothing outside this journey should delay implementation.

---

# Engineering Workflow

Every milestone follows exactly the same lifecycle.

```text
Read Context

↓

Understand

↓

Plan

↓

Implement

↓

Self Review

↓

Verify

↓

Report

↓

Review

↓

Approve

↓

Next Milestone
```

Never skip a step.

---

# Runtime Documents

Every milestone begins by reading the following documents.

1. Operating-System/01_AGENTS.md

Purpose

Engineering behaviour.

---

2. Operating-System/02_48_HOUR_EXECUTION_PLAN.md

Purpose

Overall execution strategy.

---

3. Operating-System/03_VERIQ_DESIGN_SYSTEM.md

Purpose

Product philosophy.

---

4. Operating-System/04_CREATIVE_DIRECTION.md

Purpose

Creative and UI direction.

---

5. Operating-System/05_MILESTONE_EXECUTION_PLAN.md

Purpose

Current milestone.

---

# Milestone Rules

Only one milestone may be active.

Never implement future milestones.

Never combine milestones.

Leave the application in a working state after every milestone.

Every milestone must finish with:

- Successful build
- Successful lint
- Type checking
- Engineering report

Then stop.

Wait for review.

---

# Current Project Status

Overall Progress

```text
████████□□

80%
```

Current Phase

Intelligence Integration

Current Active Milestone

Milestone 8

Status

✅ COMPLETED

---

# Milestone 1

## Name

School Pulse Foundation

---

## Goal

Create the first experience users see when opening Veriq.

The School Pulse should immediately answer:

> "What deserves my attention today?"

---

## Read

- Operating-System/01_AGENTS.md
- Operating-System/02_48_HOUR_EXECUTION_PLAN.md
- Operating-System/03_VERIQ_DESIGN_SYSTEM.md
- Operating-System/04_CREATIVE_DIRECTION.md

Reference if required:

- 005-engineering/TECH_STACK.md
- 005-engineering/CODING_STANDARDS.md
- 005-engineering/REPOSITORY_STANDARDS.md

---

## Build

- Next.js application shell
- Sidebar navigation
- Top header
- School Pulse page
- Beacon Brief component
- Metric cards
- Priority cards
- Recent alerts
- Responsive layout
- Shared layout components
- Typed mock data

---

## Do NOT Build

- Backend
- Authentication
- CSV Upload
- Beacon chat
- Reports
- Settings
- Decision Brief
- Notifications
- Database
- APIs

---

## Acceptance Criteria

✓ Application starts successfully

✓ Sidebar renders

✓ Header renders

✓ School Pulse renders

✓ Beacon Brief is the visual hero

✓ Navigation works

✓ Responsive layout works

✓ Build passes

✓ Lint passes

✓ Type checking passes

---

## Deliverables

- Frontend shell
- School Pulse page
- Shared layout
- Shared components
- Typed demo data

---

## Status

✅ Completed

---

# Milestone 2

## Name

Early Intervention

Status

✅ Completed

---

## Goal

Show how Veriq identifies emerging educational risks before they become larger problems.

---

## Build

- Intervention Hero
- Risk summary
- Evidence cards
- Behaviour indicators
- Attendance indicators
- Confidence score
- Recommended actions

---

## Reference Documents

- 003-ai/EVIDENCE_ENGINE.md
- 003-ai/DECISION_ENGINE.md
- 000-reference/DOMAIN_MODEL.md

---

## Acceptance Criteria

A school leader immediately understands:

- What is wrong
- Why it is wrong
- What should happen next

---

# Milestone 3

## Name

Beacon Workspace

Status

✅ Completed

---

## Goal

Build the AI conversation experience.

---

## Build

- Conversation interface
- Suggested questions
- Thinking state
- Evidence references
- Recommendation cards
- Follow-up actions

---

## Reference Documents

- 003-ai/BEACON.md
- 003-ai/CONTEXT_ENGINE.md
- 003-ai/EVIDENCE_ENGINE.md
- 003-ai/DECISION_ENGINE.md

---

## Acceptance Criteria

Beacon explains educational evidence naturally and remains grounded in verified calculations.

---

# Milestone 4

## Name

CSV Upload

Status

✅ Completed

---

## Goal

Allow educational data to enter Veriq.

---

## Build

- Attendance upload
- Behaviour upload
- Assessment upload
- Validation
- Upload progress
- Processing results

---

## Reference Documents

- 004-architecture/DATA_PIPELINE.md
- 005-engineering/API_STANDARDS.md
- 005-engineering/TESTING_STRATEGY.md

---

# Milestone 5

## Name

Backend Analysis

Status

✅ Completed

---

## Goal

Generate deterministic educational evidence.

---

## Build

- Attendance calculations
- Behaviour calculations
- Assessment calculations
- Signal detection
- Confidence scoring
- Evidence packages

---

## Reference Documents

- 003-ai/EVIDENCE_ENGINE.md
- 003-ai/DECISION_ENGINE.md
- 000-reference/DOMAIN_MODEL.md

---

# Milestone 6

## Name

LLM Integration

Status

✅ Completed

---

## Goal

Allow Beacon to explain verified educational evidence.

---

## Build

- Prompt templates
- Grounded responses
- Structured outputs
- Decision explanations

---

## Reference Documents

- 003-ai/BEACON.md
- 003-ai/CONTEXT_ENGINE.md
- 005-engineering/API_STANDARDS.md

---

# Milestone 7

## Name

Decision Brief

Status

✅ Completed

---

## Goal

Convert understanding into accountable action.

---

## Build

- Decision Brief
- Owner
- Priority
- Success Metric
- Due Date
- Status

---

## Reference Documents

- 003-ai/DECISION_ENGINE.md
- 000-reference/DOMAIN_MODEL.md

---

# Milestone 8

## Name

Frontend + Backend Integration

Status

✅ Completed

---

## Goal

Connect the complete user journey.

---

## Build

- API integration
- Loading states
- Error handling
- Caching
- End-to-end workflow

---

# Milestone 9

## Name

Deployment

Status

⬜ Pending

---

## Goal

Deploy the MVP.

---

## Build

- Frontend deployment (Vercel)
- Backend deployment
- Environment variables
- Production verification

---

## Reference Documents

- 005-engineering/DEPLOYMENT.md
- 005-engineering/TECH_STACK.md

---

# Milestone 10

## Name

AI4Impact Submission

Status

⬜ Pending

---

## Goal

Prepare the competition submission.

---

## Checklist

- Deployment verified
- Demo rehearsed
- Screenshots captured
- Demo video recorded (if required)
- Submission package complete

---

# Engineering Report Template

Every completed milestone must end with:

## Summary

---

## Files Created

---

## Files Modified

---

## Verification

- Build
- Lint
- Type Check
- Tests

---

## Remaining Work

---

## Recommended Next Milestone

---

# Progress Tracker

| Milestone | Status |
|-----------|--------|
| School Pulse | ✅ |
| Early Intervention | ✅ |
| Beacon Workspace | ✅ |
| CSV Upload | ✅ |
| Backend Analysis | ✅ |
| LLM Integration | ✅ |
| Decision Brief | ✅ |
| Integration | ✅ |
| Deployment | ⬜ |
| Submission | ⬜ |

---

# Final Rule

Implement only the current active milestone.

When it has been completed:

- Verify the implementation.
- Update the progress tracker.
- Produce the engineering report.
- Stop.

Do not begin the next milestone until it has been reviewed and approved.

The objective is not to build the largest platform.

The objective is to build the most convincing AI4Impact MVP.

Build deliberately.

Build beautifully.

Build Veriq.
