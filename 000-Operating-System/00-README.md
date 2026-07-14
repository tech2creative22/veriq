# VERIQ OPERATING SYSTEM

**Document ID:** VER-OS-000

**Version:** 1.0

**Status:** Active

**Owner:** Veriq Engineering

**Applies To:** Entire Repository

**Last Updated:** 11 July 2026

---

# Welcome

This document is the entry point for every engineering session.

Whether the implementation is performed by Codex, another AI coding agent or a human engineer, work must always begin here.

Do not begin implementation by browsing the repository.

Do not assume project status.

Do not begin coding until the runtime documents have been read.

This document defines:

- the current project phase
- implementation priorities
- reading order
- runtime documents
- reference documents
- milestone workflow
- engineering expectations

---

# Current Project

Project

Veriq

Product

AI-Native Educational Decision Intelligence Platform

Current Phase

AI4Impact MVP

Current Goal

Deliver a believable demonstration that proves Veriq can:

• Understand today's educational situation

• Detect emerging educational problems before they become worse

• Explain why they were detected

• Recommend practical interventions

• Generate accountable Decision Briefs

---

# Current MVP Journey

Every engineering decision should strengthen this workflow.

```
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

Nothing outside this workflow should delay implementation.

---

# Runtime Documents

The following documents form the Veriq Operating System.

These documents are always read before implementation.

They define how the MVP is built.

---

## Step 1

Read

```
Operating-System/01_AGENTS.md
```

Purpose

Defines engineering behaviour.

Defines implementation philosophy.

Defines coding rules.

Defines AI rules.

Defines repository standards.

---

## Step 2

Read

```
Operating-System/02_48_HOUR_EXECUTION_PLAN.md
```

Purpose

Defines execution strategy.

Defines implementation order.

Defines frontend and backend objectives.

Defines MVP boundaries.

---

## Step 3

Read

```
Operating-System/03_VERIQ_DESIGN_SYSTEM.md
```

Purpose

Defines product philosophy.

Defines UX principles.

Defines interaction principles.

Defines Beacon-first thinking.

---

## Step 4

Read

```
Operating-System/04_CREATIVE_DIRECTION.md
```

Purpose

Defines visual direction.

Defines screen composition.

Defines UI quality.

Defines implementation aesthetics.

---

## Step 5

Read

```
Operating-System/05_MILESTONE_EXECUTION_PLAN.md
```

Purpose

Defines the active milestone.

Defines today's implementation.

Defines acceptance criteria.

Defines stopping point.

Always implement ONLY the current milestone.

---

# Reading Rules

Always read the Runtime Documents in order.

Never skip documents.

Never replace runtime documents with architecture documents.

Never begin implementation until all runtime documents have been reviewed.

---

# Repository Structure

The repository is divided into three knowledge layers.

```
Operating-System

↓

Engineering Knowledge

↓

Reference Knowledge
```

---

# Layer One

Operating-System

Purpose

Controls implementation.

Contains only active project documents.

Always read these first.

---

# Layer Two

Engineering Knowledge

Purpose

Provides implementation guidance.

Read only when the active milestone requires it.

Folders

```
002-product/

003-ai/

004-architecture/

005-engineering/

009-decisions/

010-execution/
```

---

# Layer Three

Reference Knowledge

Purpose

Long-term project knowledge.

Do not read unless specifically required.

Folders

```
000-foundation/

000-reference/

001-company/

005-governance/

006-design/

007-business/

008-research/

011-ai4impact/
```

These folders contain future documentation and supporting material.

They are not part of the runtime implementation context.

---

# Reference Document Rules

Reference documents are consulted only when required by the active milestone.

Never explore documentation without purpose.

Read only the minimum documentation necessary.

---

# Frontend Development

Read ONLY when:

- building layouts
- creating components
- creating pages
- implementing navigation
- implementing responsive behaviour

Reference

```
005-engineering/

TECH_STACK.md

CODING_STANDARDS.md

REPOSITORY_STANDARDS.md
```

---

# Backend Development

Read ONLY when:

- building FastAPI
- creating services
- dependency injection
- API implementation

Reference

```
005-engineering/

TECH_STACK.md

API_STANDARDS.md

CODING_STANDARDS.md

TESTING_STRATEGY.md
```

---

# CSV Upload

Read ONLY when:

- file upload
- validation
- parsing
- processing

Reference

```
004-architecture/

DATA_PIPELINE.md

005-engineering/

API_STANDARDS.md

TESTING_STRATEGY.md
```

---

# Educational Analysis

Read ONLY when:

- metrics
- educational calculations
- signal detection
- evidence generation

Reference

```
003-ai/

EVIDENCE_ENGINE.md

DECISION_ENGINE.md

000-reference/

DOMAIN_MODEL.md

005-engineering/

TESTING_STRATEGY.md
```

---

# Beacon

Read ONLY when:

- AI conversation
- prompt engineering
- explanation
- grounded reasoning

Reference

```
003-ai/

BEACON.md

CONTEXT_ENGINE.md

EVIDENCE_ENGINE.md

DECISION_ENGINE.md

000-reference/

DOMAIN_MODEL.md

005-engineering/

API_STANDARDS.md
```

---

# Decision Brief

Read ONLY when:

- decision generation
- decision workflow
- decision objects

Reference

```
003-ai/

DECISION_ENGINE.md

000-reference/

DOMAIN_MODEL.md

005-engineering/

API_STANDARDS.md
```

---

# Database

Read ONLY when:

- schema
- persistence
- Supabase
- migrations

Reference

```
004-architecture/

DATABASE_SCHEMA.md

MULTI_TENANCY.md

005-engineering/

REPOSITORY_STANDARDS.md
```

---

# Deployment

Read ONLY when:

- production deployment
- environment variables
- Vercel
- backend hosting

Reference

```
005-engineering/

DEPLOYMENT.md

TECH_STACK.md
```

---

# Testing

Read ONLY when:

- writing tests
- improving quality
- fixing verification failures

Reference

```
005-engineering/

TESTING_STRATEGY.md

CODING_STANDARDS.md
```

---

# Engineering Rules

Implementation is milestone-driven.

Only one milestone may be active.

Complete the current milestone.

Verify it.

Report it.

Stop.

Wait for approval.

Do not begin the next milestone automatically.

---

# Runtime Principles

Prefer:

small milestones

working software

simple architecture

reusable components

grounded AI

verified calculations

predictable APIs

Avoid:

feature creep

premature optimization

overengineering

future platform development

large rewrites

unverified AI behaviour

---

# Definition of Success

Every implementation should improve the current MVP journey.

If the implementation does not improve:

```
School Pulse

↓

Upload

↓

Analysis

↓

Early Intervention

↓

Beacon

↓

Decision Brief
```

then it probably does not belong in the current sprint.

---

# Startup Philosophy

The objective is not to build the entire Veriq platform.

The objective is to build one exceptional demonstration.

A focused MVP is more valuable than an unfinished enterprise platform.

---

# Session Start Checklist

Before every implementation session confirm:

✓ Runtime documents reviewed

✓ Current milestone identified

✓ Acceptance criteria understood

✓ Scope understood

✓ Required reference documents identified

Only then should implementation begin.

---

# Final Rule

When uncertain:

Do not guess.

Do not redesign.

Do not assume.

Stop.

Explain the uncertainty.

Recommend options.

Wait for approval.

Veriq is built one verified milestone at a time.