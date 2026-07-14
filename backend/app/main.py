import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import File, FastAPI, Form, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from app.services.analysis import build_demo_evidence
from app.services.beacon import (
    BeaconConfigurationError,
    BeaconGroundingError,
    BeaconProviderError,
    explain_with_gemini,
    get_conversational_reply,
    get_scope_clarification,
    get_model_name,
    resolve_question_scope,
    scope_evidence,
)
from app.services.database import (
    get_workspace,
    get_beacon_conversation,
    list_beacon_conversations,
    latest_decision,
    save_import,
    save_beacon_turn,
    update_decision,
    update_latest_snapshot_school,
    update_workspace,
)
from app.services.decisions import create_decision
from app.services.evidence_store import get_latest_evidence, set_latest_evidence
from app.services.imports import ImportValidationError, process_imports

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

app = FastAPI(title="Veriq MVP Intelligence API", version="0.1.0")
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "VERIQ_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)


class BeaconQuestionRequest(BaseModel):
    """A bounded question sent by a school leader to Beacon."""

    question: str = Field(min_length=2, max_length=500)
    analysis_id: str | None = Field(default=None, max_length=100)
    scope_type: str = Field(default="school", pattern="^(school|metric|class|learner|intervention|decision)$")
    scope_id: str | None = Field(default=None, max_length=120)
    conversation_id: str | None = Field(default=None, max_length=100)

    @field_validator("question")
    @classmethod
    def strip_question(cls, value: str) -> str:
        stripped_value = value.strip()
        if len(stripped_value) < 2:
            raise ValueError("Question must contain at least two characters.")
        return stripped_value


class DecisionUpdateRequest(BaseModel):
    owner: str | None = Field(default=None, min_length=2, max_length=100)
    status: str | None = Field(default=None, pattern="^(draft|open|assigned|in_progress|completed)$")


class DecisionGenerateRequest(BaseModel):
    scope_type: str = Field(default="intervention", pattern="^(school|metric|class|learner|intervention)$")
    scope_id: str | None = Field(default=None, max_length=120)


class WorkspaceUpdateRequest(BaseModel):
    school_name: str = Field(min_length=2, max_length=120)
    school_location: str = Field(min_length=2, max_length=160)
    user_name: str = Field(min_length=2, max_length=100)
    user_role: str = Field(min_length=2, max_length=100)

    @field_validator("school_name", "school_location", "user_name", "user_role")
    @classmethod
    def strip_workspace_value(cls, value: str) -> str:
        return value.strip()


def error_response(status_code: int, code: str, message: str) -> JSONResponse:
    evidence, _source = get_latest_evidence()
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {"code": code, "message": message, "details": {}},
            "trace_id": evidence["trace_id"],
        },
    )


@app.exception_handler(ImportValidationError)
async def import_validation_error(
    _request: object, error: ImportValidationError
) -> JSONResponse:
    evidence, _source = get_latest_evidence()
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(error),
                "details": error.details,
            },
            "trace_id": evidence["trace_id"],
        },
    )


@app.exception_handler(BeaconConfigurationError)
async def beacon_configuration_error(
    _request: object, _error: BeaconConfigurationError
) -> JSONResponse:
    return error_response(
        503,
        "GEMINI_NOT_CONFIGURED",
        "Beacon needs a Gemini API key before it can generate a response.",
    )


@app.exception_handler(BeaconProviderError)
@app.exception_handler(BeaconGroundingError)
async def beacon_provider_error(
    _request: object, _error: BeaconProviderError | BeaconGroundingError
) -> JSONResponse:
    return error_response(
        502,
        "BEACON_RESPONSE_UNAVAILABLE",
        "Beacon could not safely prepare a response. Please try again.",
    )


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}


@app.get("/api/v1/workspace", summary="Get the active MVP school and user context")
def workspace_context() -> dict:
    workspace = get_workspace()
    evidence, _source = get_latest_evidence()
    return {"success": True, "data": workspace, "metadata": {"analysis_id": evidence["analysis_id"]}, "trace_id": evidence["trace_id"]}


@app.patch("/api/v1/workspace", summary="Update the active MVP school and user context")
def patch_workspace(request: WorkspaceUpdateRequest) -> dict:
    workspace = update_workspace(request.model_dump())
    update_latest_snapshot_school(workspace["school_name"])
    evidence, _source = get_latest_evidence()
    return {"success": True, "data": workspace, "metadata": {"analysis_id": evidence["analysis_id"]}, "trace_id": evidence["trace_id"]}


@app.get("/api/v1/intelligence/demo-evidence")
def demo_evidence() -> dict:
    evidence = build_demo_evidence()
    return {"success": True, "data": evidence, "trace_id": evidence["trace_id"]}


@app.get("/api/v1/intelligence/latest-evidence")
def latest_evidence() -> dict:
    """Returns the current imported Evidence Package or the prepared MVP demo."""
    evidence, source = get_latest_evidence()
    return {
        "success": True,
        "data": {**evidence, "source": source},
        "metadata": {"source": source},
        "trace_id": evidence["trace_id"],
    }


@app.get("/api/v1/intelligence/scoped-evidence")
def scoped_evidence(
    scope_type: str = Query(default="school", pattern="^(school|metric|class|learner|intervention)$"),
    scope_id: str | None = Query(default=None, max_length=120),
) -> dict:
    evidence, source = get_latest_evidence()
    evidence["source"] = source
    scoped = scope_evidence(evidence, scope_type, scope_id)
    return {"success": True, "data": scoped, "metadata": {"source": source}, "trace_id": scoped["trace_id"]}


@app.post("/api/v1/imports/analyse", status_code=201)
async def analyse_import(
    attendance: UploadFile = File(...),
    behaviour: UploadFile = File(...),
    assessments: UploadFile = File(...),
    data_use_acknowledged: bool = Form(default=False),
) -> dict:
    """Validates the three documented CSV files and creates a new Evidence Package."""
    if not data_use_acknowledged:
        raise ImportValidationError(
            "Confirm that you are authorised to use these files before analysis."
        )
    for file in (attendance, behaviour, assessments):
        if not file.filename or not file.filename.lower().endswith(".csv"):
            raise ImportValidationError("Each uploaded file must be a CSV.")
    files = {
        "attendance": await attendance.read(),
        "behaviour": await behaviour.read(),
        "assessments": await assessments.read(),
    }
    workspace = get_workspace()
    evidence, records, import_id = process_imports(files["attendance"], files["behaviour"], files["assessments"], workspace["school_name"])
    save_import(import_id, evidence["school_name"], files, records)
    set_latest_evidence(evidence, "csv_import", import_id)
    return {
        "success": True,
        "data": {**evidence, "source": "csv_import"},
        "metadata": {
            "source": "csv_import",
            "files_validated": 3,
            "records_stored": len(records),
            "import_id": import_id,
            "data_use_acknowledged": True,
        },
        "trace_id": evidence["trace_id"],
    }


@app.post(
    "/api/v1/beacon/explain",
    summary="Explain verified school evidence with Gemini",
)
def explain_beacon(request: BeaconQuestionRequest) -> dict:
    """Generates a bounded Beacon explanation from the current Evidence Package."""
    evidence, source = get_latest_evidence()
    evidence["source"] = source
    if request.analysis_id and request.analysis_id != evidence["analysis_id"]:
        return error_response(409, "ANALYSIS_CONTEXT_CHANGED", "The selected analysis is no longer current. Refresh the page and ask again.")
    clarification = get_scope_clarification(request.question, evidence)
    scope_type, scope_id = resolve_question_scope(
        request.question, evidence, request.scope_type, request.scope_id
    )
    evidence = scope_evidence(evidence, scope_type, scope_id)
    response = clarification or get_conversational_reply(request.question, evidence)
    if response is not None:
        conversation_id = save_beacon_turn(
            evidence["analysis_id"], request.question, response, scope_type, scope_id, request.conversation_id
        )
        response["conversation_id"] = conversation_id
        return {
            "success": True,
            "data": response,
            "metadata": {"provider": "veriq", "intent": "conversation"},
            "trace_id": evidence["trace_id"],
        }

    response = explain_with_gemini(request.question, evidence)
    conversation_id = save_beacon_turn(
        evidence["analysis_id"], request.question, response, scope_type, scope_id, request.conversation_id
    )
    response["conversation_id"] = conversation_id
    return {
        "success": True,
        "data": response,
        "metadata": {"model": get_model_name(), "provider": "gemini"},
        "trace_id": evidence["trace_id"],
    }


@app.get("/api/v1/beacon/conversations", summary="List persisted Beacon conversations")
def beacon_conversations() -> dict:
    evidence, _source = get_latest_evidence()
    conversations = list_beacon_conversations(evidence["analysis_id"])
    return {"success": True, "data": conversations, "metadata": {}, "trace_id": evidence["trace_id"]}


@app.get("/api/v1/beacon/conversations/{conversation_id}", summary="Open a persisted Beacon conversation")
def beacon_conversation(conversation_id: str) -> dict:
    evidence, _source = get_latest_evidence()
    conversation = get_beacon_conversation(conversation_id, evidence["analysis_id"])
    if conversation is None:
        return error_response(404, "CONVERSATION_NOT_FOUND", "This Beacon conversation could not be found for the current analysis.")
    return {"success": True, "data": conversation, "metadata": {}, "trace_id": evidence["trace_id"]}


@app.post("/api/v1/decisions/generate", summary="Generate a Decision Brief from current evidence")
def generate_decision(request: DecisionGenerateRequest | None = None) -> dict:
    evidence, _source = get_latest_evidence()
    workspace = get_workspace()
    requested = request or DecisionGenerateRequest()
    scope_id = requested.scope_id or (evidence["class_name"] if requested.scope_type == "intervention" else None)
    evidence = scope_evidence(evidence, requested.scope_type, scope_id)
    explanation = explain_with_gemini(
        "Create the clearest proportionate recommendation for a school leader to review and action from this intervention evidence.",
        evidence,
    )
    decision = create_decision(evidence, explanation, workspace["user_role"])
    return {"success": True, "data": decision, "metadata": {"provider": "gemini", "model": get_model_name()}, "trace_id": evidence["trace_id"]}


@app.get("/api/v1/decisions/latest", summary="Get the current analysis Decision Brief")
def get_latest_decision() -> dict:
    evidence, _source = get_latest_evidence()
    decision = latest_decision(evidence["analysis_id"])
    return {"success": True, "data": decision, "metadata": {}, "trace_id": evidence["trace_id"]}


@app.patch("/api/v1/decisions/{decision_id}", summary="Update human-owned Decision Brief fields")
def patch_decision(decision_id: str, request: DecisionUpdateRequest) -> dict:
    updates = request.model_dump(exclude_none=True)
    decision = update_decision(decision_id, updates)
    if decision is None:
        return error_response(404, "DECISION_NOT_FOUND", "The Decision Brief could not be found.")
    return {"success": True, "data": decision, "metadata": {}, "trace_id": decision["trace_id"]}
