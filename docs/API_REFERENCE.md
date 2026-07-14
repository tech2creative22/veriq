# Veriq MVP API Reference

**Base URL:** `http://localhost:8000`  
**Interactive OpenAPI:** `/docs`

Successful application responses use:

```json
{
  "success": true,
  "data": {},
  "metadata": {},
  "trace_id": "trace_..."
}
```

Errors use a stable code and safe message:

```json
{
  "success": false,
  "error": { "code": "VALIDATION_ERROR", "message": "...", "details": {} },
  "trace_id": "trace_..."
}
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness response. |
| GET | `/api/v1/workspace` | Current school and user display context. |
| PATCH | `/api/v1/workspace` | Update school name/location and user name/role. |
| GET | `/api/v1/intelligence/demo-evidence` | Prepared example Evidence Package. |
| GET | `/api/v1/intelligence/latest-evidence` | Current imported or prepared Evidence Package. |
| GET | `/api/v1/intelligence/scoped-evidence` | Evidence scoped to school, metric, class, learner or intervention. |
| POST | `/api/v1/imports/analyse` | Validate three CSV files, store records and create the active Evidence Package. |
| POST | `/api/v1/beacon/explain` | Explain current evidence using resolved question scope. |
| GET | `/api/v1/beacon/conversations` | List conversations for the active analysis. |
| GET | `/api/v1/beacon/conversations/{id}` | Open one active-analysis conversation. |
| POST | `/api/v1/decisions/generate` | Generate a Decision Brief from scoped evidence. |
| GET | `/api/v1/decisions/latest` | Fetch the newest Decision Brief for the active analysis. |
| PATCH | `/api/v1/decisions/{id}` | Update human-owned `owner` or `status`. |

## Import contract

`POST /api/v1/imports/analyse` is `multipart/form-data` with four required parts:

- `attendance`
- `behaviour`
- `assessments`
- `data_use_acknowledged=true`

All three files must be supplied and valid. The acknowledgement must be true; otherwise the API returns HTTP 422 without storing the import. It confirms authorised synthetic demonstration use only and is not a substitute for consent or a lawful basis. The response metadata contains the import ID, validated file count, stored record count and acknowledgement state.

## Evidence scope

`GET /api/v1/intelligence/scoped-evidence` accepts:

- `scope_type`: `school`, `metric`, `class`, `learner` or `intervention`.
- `scope_id`: the metric ID, class name, learner ID/name or intervention class identifier where applicable.

## Beacon request

```json
{
  "question": "Which Form 4 class needs attention before the next internal assessment?",
  "analysis_id": "analysis_...",
  "scope_type": "school",
  "scope_id": null,
  "conversation_id": null
}
```

`question` is 2-500 characters. The server resolves a more specific named learner or class from the question when supported by current evidence. If `analysis_id` no longer matches the active import, the request is rejected with HTTP 409.

Beacon may return `conversation`, `clarification` or `evidence_analysis`. Evidence analysis contains situation, why it matters, verified supporting evidence, recommendation, next step, confidence, missing evidence, scope and trace ID.

## Decision requests

Generate:

```json
{
  "scope_type": "intervention",
  "scope_id": "Form 4A"
}
```

Update human-owned fields:

```json
{
  "owner": "Deputy Head",
  "status": "in_progress"
}
```

Allowed statuses are `draft`, `open`, `assigned`, `in_progress` and `completed`.

## Important status codes

| Status | Meaning |
|---:|---|
| 201 | CSV import accepted and analysed. |
| 409 | Client analysis context is stale. |
| 422 | Request or CSV validation failed. |
| 502 | Provider response could not be safely grounded. |
| 503 | Gemini is not configured. |
