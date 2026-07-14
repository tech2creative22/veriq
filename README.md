# Veriq AI4Impact MVP

# Veriq

**AI-Native Educational Decision Intelligence Platform**

Veriq helps school leaders detect educational problems before they become examination results.

Instead of waiting until the end of the term to discover declining pass rates,bad behavior Veriq continuously analyzes attendance, behaviour and perfomance data, it identifies emerging patterns, explains why they matter and recommends practical interventions through an AI assistant called **Beacon**.

Built for the **AI4Impact Zimbabwe Challenge 2026**.

---

# The Problem

Schools often discover problems too late.

By the time examination results are released, opportunities for intervention have already passed.

School leaders receive data.

They rarely receive intelligence.

Veriq changes that.

---

# Our Solution

Veriq transforms raw school data into actionable educational intelligence.

Using AI, Veriq:

- Detects emerging educational risks
- Connects evidence across multiple data sources
- Explains why patterns matter
- Recommends interventions
- Generates accountable Decision Briefs for school leadership

The goal is simple:

> Help schools act **before problems become outcomes**.

---

# Core Workflow

```text
Upload School Data
        ↓
Validate Data
        ↓
Generate Educational Evidence
        ↓
Identify Early Risks
        ↓
Beacon Explains Why
        ↓
Generate Decision Brief
        ↓
Leadership Takes Action
```

---

# Key Features

## School Pulse

An AI-generated overview of the school's current health, highlighting the most important priorities for the day.

---

## Data Upload

Import attendance, behaviour and assessment CSV files for analysis.

---

## Early Intervention

Detect emerging educational patterns before they become larger problems.

Evidence is transparent, confidence is explained and recommendations remain grounded in school data.

---

## Beacon

Beacon is Veriq's AI educational advisor.

It explains:

- Why a class was flagged
- Which evidence supports the conclusion
- What interventions should happen next
- What information is still missing

Beacon does not replace school leadership.

It supports better decision-making.

---

## Decision Briefs

Convert AI insights into structured leadership actions.

Each Decision Brief contains:

- verified evidence
- recommended action
- owner
- due date
- measurable success metric
- confidence score

---

# AI Philosophy

Veriq is designed around one principle:

> AI should explain before it recommends.

Every recommendation is supported by evidence.

School leaders remain responsible for final decisions.

Beacon provides intelligence.

Humans provide judgement.

This repository is the working **AI4I Development-track MVP**. It is suitable for demonstration with the included fictional dataset. It is not yet authorised for production processing of real learner records.

## Judge workflow

1. Confirm authorised synthetic demonstration use, then upload three Zimbabwe secondary-school CSV files: attendance, behaviour and assessments.
2. Review the whole-school summary in **School Pulse**.
3. Monitor class and learner patterns in **Early Intervention**.
4. Ask **Beacon** to explain the evidence or compare current internal assessment readiness.
5. Generate and review a **Decision Brief** with an owner, actions and review date.

The included judge dataset contains 20 fictional, first-name-only learners across Form 1A to Form 4A. Three learners have connected high-attention patterns, two have watch patterns and fifteen are stable controls.

## Technology

- Frontend: Next.js 15.5.20, React 18.3.1 and TypeScript 5.7.2.
- API: FastAPI 0.115.6 and Pydantic.
- Persistence: local SQLite for the MVP.
- AI provider: Google Gemini through `google-genai` 2.11.0.
- Evidence engine: deterministic Python validation, aggregation, signal and confidence logic.

See [As-built architecture](docs/AS_BUILT_ARCHITECTURE.md), [API reference](docs/API_REFERENCE.md) and [environment guide](docs/ENVIRONMENT_AND_CONFIGURATION.md).

For the reproducible Linux container topology and ZCHPC CCE roadmap, see [CCE deployment plan](deployment/CCE_DEPLOYMENT_PLAN.md). Docker is not required for local development.

## Prerequisites

- Node.js 20 or newer.
- npm 10 or newer.
- Python 3.11 or newer.
- A Gemini API key for live Beacon explanations and Decision Brief generation.

The dashboard, CSV import, evidence calculations and prepared example can run without Gemini. Questions that require model synthesis return a safe configuration error when no key is present.

## Local setup

### 1. Install the frontend

From the repository root:

```powershell
npm ci
Copy-Item .env.example .env.local
```

macOS or Linux:

```bash
npm ci
cp .env.example .env.local
```

### 2. Create the backend environment

PowerShell:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install --upgrade pip
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.txt
Copy-Item backend/.env.example backend/.env
```

macOS or Linux:

```bash
python -m venv backend/.venv
backend/.venv/bin/python -m pip install --upgrade pip
backend/.venv/bin/python -m pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
```

Open `backend/.env` and set `GEMINI_API_KEY`. Never commit that file.

### 3. Start the backend

PowerShell:

```powershell
backend/.venv/Scripts/python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

macOS or Linux:

```bash
backend/.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Verify `http://127.0.0.1:8000/health` returns `{"status":"healthy"}`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 4. Start the frontend

Development mode:

```powershell
npm run dev
```

Open `http://localhost:3000`.

For the production path used in verification:

```powershell
npm run build
$env:HOSTNAME = "127.0.0.1"
$env:PORT = "3000"
npm run start
```

## Load the judge dataset

Open `http://localhost:3000/upload` and select:

- `demo-data/zimbabwe-secondary-judge/attendance.csv`
- `demo-data/zimbabwe-secondary-judge/behaviour.csv`
- `demo-data/zimbabwe-secondary-judge/assessments.csv`

The backend validates all three files before replacing the active evidence snapshot. Invalid rows or missing required columns produce a structured validation response; partial imports are not accepted.

## Verification commands

Frontend:

```powershell
npm run typecheck
npm run lint
npm run build
npm audit --omit=dev --audit-level=high --package-lock-only
```

Backend:

```powershell
Set-Location backend
python -m unittest discover -s tests -v
```

The verified baseline on 14 July 2026 is: zero production npm vulnerabilities, zero TypeScript errors, zero ESLint errors, a successful optimized build, 29 passing backend tests and a 35-check visible browser flow. See [security baseline](submission/SECURITY_BASELINE.md).

## Repository structure

```text
app/                 Next.js pages and page-specific styles
components/          Shared frontend presentation components
lib/                 Typed browser-to-API client
backend/app/         FastAPI application and services
backend/tests/       Evidence, import and Beacon unit/integration tests
demo-data/           Primary fictional Zimbabwe judge dataset
sample-data/         Smaller import examples
docs/                As-built technical documentation
submission/          Competition readiness and verification evidence
```

## Evidence and AI safety boundary

Veriq does not ask Gemini to calculate attendance, incident counts, assessment averages, changes, risk thresholds or confidence. Python calculates and stores those facts first. Beacon receives a scoped Evidence Package, must use the supplied facts, and the application reattaches verified evidence to the response. A school leader remains responsible for any intervention or decision.

The assessment CSV represents internal continuous-assessment results. The MVP does not claim to calculate an official ZIMSEC pass rate or final examination outcome.

## Current MVP limitations

- Single-school local workspace; authentication and tenant isolation are not implemented.
- SQLite is appropriate for the demonstration, not a multi-school production deployment.
- CORS currently permits the local frontend origins only.
- Internet access and a configured Gemini key are required for generative explanations.
- Real learner data must not be used until production privacy, security, retention and school-authorisation controls are implemented.

## Licence and contribution status

Veriq is released under the repository's protected [Challenge Evaluation Licence](LICENSE): authorised challenge reviewers may inspect and run it for evaluation, but no general reuse, redistribution or commercialisation rights are granted. Third-party dependencies remain governed by their own licences. See the [licence and asset register](submission/business/LICENCE_AND_ASSET_REGISTER.md).
