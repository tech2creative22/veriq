# VERIQ ENGINEERING CONSTITUTION

**Document:** AGENTS.md

**Version:** 1.0

**Status:** Active

**Owner:** Veriq Engineering

**Applies To:** Entire Repository

**Last Updated:** 11 July 2026

---

# Purpose

This document defines how AI coding agents and engineers contribute to Veriq.

It is the primary engineering operating manual for this repository.

Every implementation task begins by following the principles defined in this document.

The objective is not simply to write working software.

The objective is to build Veriq consistently, predictably and intentionally.

Whenever there is uncertainty, this document provides the default behaviour.

---

# Current Mission

## Intent

Ensure every engineering decision supports the successful delivery of the AI4Impact MVP.

This mission overrides long-term roadmap considerations until the MVP has been completed and submitted.

---

## Mission Statement

Build the smallest believable demonstration of Educational Decision Intelligence.

The demonstration must convince judges that Veriq can help school leaders understand what is happening today, identify emerging problems before they become worse and recommend practical actions using real AI.

The MVP is not intended to demonstrate every planned capability of Veriq.

It exists to demonstrate the core value proposition.

---

## Success Criteria

A school leader should be able to:

1. Open Veriq.

2. Understand today's situation in less than two minutes.

3. Upload school data.

4. Watch Beacon analyse the evidence.

5. Understand why a class has been flagged.

6. Receive a practical recommendation.

7. Generate a Decision Brief.

If these seven outcomes are achieved, the MVP has succeeded.

---

# Current Phase

## Intent

Prevent implementation from drifting into long-term platform development.

The current phase determines which work is allowed.

---

## Phase

AI4Impact MVP

---

## Internal Deadline

12 July 2026

---

## Submission Deadline

14 July 2026

---

## Current Objective

Deliver one complete vertical slice.

The vertical slice begins with School Pulse and ends with a generated Decision Brief.

Everything outside this journey is secondary.

---

## Current Vertical Slice

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

---

All engineering effort should improve this workflow.

---

# Authority Hierarchy

## Intent

Resolve conflicts between documents.

If two documents disagree, the higher document always takes precedence.

---

Highest Authority

1. User Instructions

2. AGENTS.md

3. Current Mission

4. Current Phase

5. 48 Hour Execution Plan

6. MVP Scope

7. Veriq Design System

8. Engineering Standards

9. Architecture Documents

10. Future Roadmaps

Lowest Authority

---

## Rule

Never implement functionality from a lower-priority document if it conflicts with a higher-priority document.

Example:

If the long-term architecture describes a Learning Engine but the MVP Scope excludes it, the Learning Engine must not be implemented.

---

# Required Reading

## Intent

Reduce unnecessary context while ensuring every task has sufficient information.

---

Every major task begins by reading the following documents.

### Required

docs/010-ai4impact/

- 00_AI4IMPACT_OVERVIEW.md
- 01_DEMO_VISION.md
- 02_MVP_SCOPE.md
- 03_DEMO_SCRIPT.md
- 13_48_HOUR_EXECUTION_PLAN.md

---

Engineering

- TECH_STACK.md
- REPOSITORY_STANDARDS.md
- CODING_STANDARDS.md
- TESTING_STRATEGY.md

---

Reference

- DOMAIN_MODEL.md

---

Design

- 00_VERIQ_DESIGN_SYSTEM.md

---

Task-specific documents should only be read when required.

Do not read unrelated architecture documents before every task.

---

# Product Identity

## Intent

Ensure every engineering decision reinforces Veriq's identity.

---

## Veriq is NOT

Veriq is not:

- a school management system
- an ERP
- a reporting dashboard
- business intelligence software
- a generic chatbot
- analytics software
- another SaaS dashboard

---

## Veriq IS

Veriq is:

- an AI-native Educational Decision Intelligence platform
- an AI Operating System for schools
- an intelligent workspace
- a trusted colleague for school leaders
- an evidence-driven decision platform

---

## Beacon

Beacon is the intelligence layer of Veriq.

Beacon is not another feature.

Beacon is not simply a chatbot.

Beacon exists throughout the product.

Every important workflow should include Beacon.

Beacon explains.

Beacon recommends.

Beacon guides.

Beacon never replaces verified evidence.

---

## Design Philosophy

Veriq reduces cognitive load.

It does not increase information density.

The interface should help users understand what matters rather than exposing every available metric.

Information must flow naturally from:

Understanding

↓

Evidence

↓

Action

Metrics support understanding.

They never dominate the experience.

---

## Engineering Philosophy

Engineering decisions should favour:

clarity

simplicity

maintainability

reliability

predictability

beauty

Avoid complexity unless complexity creates measurable value.

Prefer small, composable modules over large frameworks.

Prefer readable code over clever code.

Build only what improves the current mission.

---

## The One Question Rule

Every primary screen must answer exactly one question.

School Pulse

"What deserves my attention today?"

Early Intervention

"What is beginning to go wrong?"

Beacon

"Why has Veriq reached this conclusion?"

Decision Brief

"What action should now be taken?"

If a screen answers multiple unrelated questions, simplify it.

---

## Engineering Mindset

Before implementing any feature, ask:

Does this improve tomorrow's demonstration?

If the answer is no, it probably does not belong in the current MVP.

PART 2

# MVP Boundaries

## Intent

Protect the AI4Impact MVP from feature creep.

The objective is to deliver one exceptional demonstration rather than an incomplete enterprise platform.

Whenever there is uncertainty, choose the smallest implementation that convincingly demonstrates Educational Decision Intelligence.

---

## The Golden Rule

The MVP exists to demonstrate capability.

It does not exist to implement every planned feature of Veriq.

Every implementation decision should increase the quality of the demonstration.

If a feature does not improve the demonstration, it should not be implemented before submission.

---

# Core User Journey

The MVP supports one complete workflow.

```
School Pulse

↓

Upload School Data

↓

Educational Analysis

↓

Early Intervention

↓

Beacon Conversation

↓

Decision Brief
```

This workflow defines the product.

Every completed feature should strengthen this journey.

---

# MVP Features

The following features are mandatory.

## School Pulse

Purpose

Provide an immediate understanding of the school's current situation.

Required

- Greeting
- Beacon Brief
- Attendance summary
- Behaviour summary
- Assessment summary
- Primary Insight
- Navigation to Early Intervention

---

## CSV Upload

Purpose

Allow prepared datasets to enter the platform.

Required

- Attendance upload
- Behaviour upload
- Assessment upload
- Validation
- Processing status
- Success state
- Failure state

---

## Educational Analysis

Purpose

Transform uploaded data into verified educational evidence.

Required

- Attendance calculations
- Behaviour calculations
- Assessment calculations
- Signal detection
- Confidence calculation
- Evidence package generation

---

## Early Intervention

Purpose

Explain emerging educational risk before outcomes become worse.

Required

- Intervention hero
- Beacon explanation
- Verified evidence
- Recommended actions
- Confidence
- Create Decision Brief

---

## Beacon

Purpose

Provide grounded educational reasoning.

Required

- Context-aware conversation
- Explanation
- Evidence
- Recommendation
- Suggested questions
- Decision generation

Beacon must always remain grounded in verified evidence.

---

## Decision Brief

Purpose

Transform educational understanding into accountable action.

Required

- Situation
- Evidence
- Recommendation
- Priority
- Owner
- Success Metric
- Due Date
- Status

---

# Deferred Features

The following capabilities belong to future versions of Veriq.

Do not implement them during the MVP unless explicitly instructed.

## Platform

- Multi-school management
- District intelligence
- Ministry dashboards
- Billing
- Subscription management
- Marketplace
- Notifications
- Audit history
- Role administration

---

## AI

- Institutional Memory
- Learning Engine
- Prediction Engine
- Autonomous Planning
- Cross-school intelligence
- Long-term recommendations
- Automated scheduling
- Continuous monitoring

---

## Analytics

- Advanced dashboards
- Historical reporting
- Forecasting
- Benchmarking
- District comparisons
- National comparisons

---

## Integrations

- WhatsApp
- SMS
- Email automation
- Google Classroom
- Microsoft Teams
- Moodle
- SIS synchronization

---

## Rule

When in doubt,

leave it out.

---

# Design Commandments

## Intent

Maintain one visual identity throughout Veriq.

Every engineer should produce interfaces that feel like one product regardless of who implemented them.

---

## Commandment One

Beacon is always present.

Beacon is the intelligence layer of Veriq.

Beacon should appear naturally throughout the experience.

Do not isolate Beacon as a separate feature unless explicitly required.

---

## Commandment Two

Understanding comes before metrics.

Every page begins by helping the user understand what matters.

Only then should supporting evidence and metrics appear.

---

## Commandment Three

Every page answers one question.

Never allow a page to become a collection of unrelated information.

---

## Commandment Four

Whitespace is a feature.

Do not fill empty space simply because it exists.

Calm interfaces communicate confidence.

---

## Commandment Five

Evidence precedes recommendations.

Every recommendation must be supported by visible evidence.

---

## Commandment Six

Charts support stories.

Charts are supporting evidence.

Charts are never the hero of the page.

---

## Commandment Seven

One dominant insight.

Every screen should contain one visually dominant insight that immediately attracts attention.

---

## Commandment Eight

Beauty improves trust.

Attention to spacing, typography and hierarchy is part of functionality.

Poor visual quality reduces perceived intelligence.

---

# Engineering Commandments

## Intent

Maintain consistent implementation quality.

---

## Rule One

Small components.

Large pages.

Complex behaviour should be composed from reusable components.

---

## Rule Two

Strong typing everywhere.

Avoid untyped objects.

Prefer explicit interfaces.

---

## Rule Three

Business logic belongs in services.

Do not place calculation logic inside React components.

---

## Rule Four

LLMs never calculate.

Python calculates.

LLMs explain.

---

## Rule Five

Never duplicate business rules.

Business rules should exist in one location.

---

## Rule Six

Prefer composition over inheritance.

---

## Rule Seven

Readable code is better than clever code.

Future engineers should understand every implementation quickly.

---

## Rule Eight

Keep APIs predictable.

Every endpoint should follow the established response contract.

---

## Rule Nine

Errors must be understandable.

Every failure should tell the user what happened and what they can do next.

---

## Rule Ten

Optimize for reliability before optimization.

Correct software is more valuable than fast software.

---

# AI Commandments

## Intent

Ensure every AI response remains trustworthy.

---

## Principle One

AI explains evidence.

AI does not invent evidence.

---

## Principle Two

AI recommendations must remain grounded.

Every recommendation should be traceable to verified educational signals.

---

## Principle Three

Never hallucinate.

If evidence is insufficient,

Beacon should clearly state that additional information is required.

---

## Principle Four

Confidence should be transparent.

Do not imply certainty where uncertainty exists.

---

## Principle Five

Educational evidence always wins.

If an LLM response conflicts with verified calculations,

the verified calculations are correct.

---

## Principle Six

Every important response should follow this structure.

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

---

## Principle Seven

Protect user trust.

Never fabricate:

- learners
- teachers
- attendance figures
- assessment scores
- behaviour incidents

Every numerical statement must originate from verified calculations.

---

## AI Success Test

After every Beacon response ask:

Can this answer be explained using the available evidence?

If not,

the response should be regenerated or rejected.

PART 3

# Working Method

## Intent

Ensure every implementation task follows a consistent engineering workflow.

Every contribution should improve the product while maintaining reliability, readability and architectural consistency.

Never skip planning, verification or self-review.

---

# Engineering Workflow

Every task follows the same execution loop.

```
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

Improve

↓

Report
```

---

## Step One — Understand

Before writing code:

- Read AGENTS.md.
- Read the required MVP documents.
- Read any task-specific documents.
- Inspect the existing implementation.
- Understand how the requested feature fits into the current vertical slice.

Do not begin implementation until the objective is clear.

---

## Step Two — Plan

Before modifying code:

Describe a short implementation plan.

The plan should identify:

- affected files
- components
- APIs
- services
- expected output
- possible risks

Keep the plan concise.

---

## Step Three — Implement

Write the smallest implementation that satisfies the current milestone.

Prefer incremental improvements over large rewrites.

Avoid introducing unnecessary abstractions.

Do not build future features.

---

## Step Four — Self Review

Before testing, review the implementation.

Verify:

- naming consistency
- architecture consistency
- readability
- unnecessary complexity
- duplicated logic
- dead code

Refactor immediately if a simple improvement exists.

---

## Step Five — Verify

Every completed task must be verified.

Where supported by the repository:

Frontend

- lint
- type check
- production build

Backend

- unit tests
- endpoint verification
- schema validation

Never claim completion without verification.

---

## Step Six — Improve

If small improvements naturally fit within the current milestone:

- simplify code
- improve naming
- reduce duplication
- improve comments
- improve accessibility

Do not begin unrelated refactoring.

---

## Step Seven — Report

Every completed task must include a structured engineering report.

---

# Task Completion Report

Every completed implementation should finish with the following summary.

## Completed

Brief description of the completed milestone.

---

## Files Created

List every newly created file.

---

## Files Modified

List every modified file.

---

## Architecture Decisions

Explain any important implementation decisions.

---

## Commands Executed

Example:

```bash
npm run lint
npm run build
pytest
```

---

## Verification Status

Lint

PASS / FAIL

Type Check

PASS / FAIL

Build

PASS / FAIL

Tests

PASS / FAIL

---

## Remaining Limitations

Document any known limitations.

Never hide unfinished work.

---

## Recommended Next Task

Recommend the logical next milestone.

---

# Repository Standards

## Folder Structure

Respect the approved repository structure.

Do not create new top-level folders without clear justification.

Keep related functionality together.

---

## Components

Prefer small reusable components.

Large pages should be assembled from reusable building blocks.

Avoid deeply nested component trees where possible.

---

## Naming

Names should be descriptive.

Avoid abbreviations unless they are domain terminology.

Use Veriq terminology consistently.

---

## Comments

Write comments only when they explain intent.

Do not comment obvious code.

Prefer expressive code over excessive comments.

---

## Dependencies

Do not introduce new dependencies unless they provide clear value.

Prefer existing project libraries.

Explain why a new dependency is required.

---

# Code Quality Principles

Engineering quality is measured by:

- readability
- maintainability
- predictability
- consistency
- simplicity

Avoid clever solutions.

Future engineers should understand every implementation quickly.

---

# Performance Principles

Optimize only where necessary.

Correctness is more important than micro-optimizations.

Prefer understandable code over premature optimization.

---

# Accessibility Principles

Every UI should support:

- keyboard navigation
- readable typography
- sufficient colour contrast
- clear focus states
- meaningful labels

Accessibility is part of quality.

---

# Error Handling

Errors should always:

- explain what happened
- explain why
- explain what the user can do next

Avoid technical language where possible.

Never expose internal implementation details.

---

# Escalation Rules

If implementation becomes uncertain:

Stop.

Explain the issue.

Provide available options.

Recommend one approach.

Wait before making major architectural decisions.

Never silently redesign the platform.

---

# Definition of Done

A task is complete only when:

- requirements are implemented
- implementation follows repository standards
- design follows the Veriq Design System
- code is readable
- lint passes
- build passes
- tests pass where applicable
- no critical console errors exist
- documentation is updated if required

If any requirement is missing,

the task is not complete.

---

# Before Every Commit

Review the implementation.

Confirm:

✓ Requirements satisfied

✓ Naming consistent

✓ No duplicated logic

✓ No obvious bugs

✓ Lint passes

✓ Build passes

✓ Tests pass

✓ No temporary debug code

✓ No commented-out code

✓ No unused imports

Only then should work be considered ready.

---

# Forbidden Actions

Do not:

- redesign the architecture
- introduce new platform features outside the MVP
- rename established Veriq concepts
- bypass the Design System
- bypass Engineering Standards
- calculate educational metrics using an LLM
- fabricate evidence
- fabricate confidence values
- silently change API contracts
- silently change database schemas
- remove existing functionality without justification
- claim work is complete without verification

---

# Engineering Philosophy

Leave the repository better than you found it.

If a simple improvement can be made without delaying the milestone,

make it.

If the improvement becomes a separate project,

record it and continue.

---

# Success Test

Before finishing any task, answer the following questions.

Did this improve tomorrow's demonstration?

Does the implementation strengthen the School Pulse → Early Intervention → Beacon → Decision Brief workflow?

Does it make Veriq feel more intelligent?

Does it make Veriq easier to understand?

Does it maintain trust?

If the answer is no,

reconsider the implementation.

---

# Final Principle

Veriq is built to help educational leaders make better decisions before problems become results.

Every line of code should support that mission.

Build with clarity.

Build with purpose.

Build with discipline.

Build Veriq.