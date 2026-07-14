export type SignalSeverity = "high" | "medium" | "healthy";
export type EvidenceSignal = { id: string; category: string; fact: string; previous_value: number; current_value: number; change: number; severity: SignalSeverity };
export type SchoolMetric = { id: string; category: string; label: string; previous_value: number; current_value: number; change: number; unit: string; tone: "positive" | "attention"; fact: string; display_value?: string };
export type ClassSummary = { class_name: string; risk_score: number; repeated_absences: number; signals: EvidenceSignal[] };
export type LearnerSummary = { student_id: string; learner_name: string; class_name: string; attendance_previous: number | null; attendance_current: number | null; behaviour_previous: number; behaviour_current: number; assessment_previous: number | null; assessment_current: number | null; risk_factors: string[] };
export type IntelligencePriority = { id: string; class_name: string; level: "High" | "Medium" | "Watch"; title: string; description: string; scope_id: string };
export type IntelligenceAlert = { id: string; category: string; title: string; detail: string; tone: "positive" | "attention" };
export type Intervention = { class_name: string; title: string; summary: string; priority: "High" | "Medium" | "Watch"; actions: string[] };
export type EvidencePackage = {
  analysis_id: string; school_name: string; class_name: string; analysis_period: string; generated_at: string;
  signals: EvidenceSignal[]; school_metrics: SchoolMetric[]; class_summaries: ClassSummary[];
  learner_summaries: LearnerSummary[]; subject_summaries: Array<{ class_name: string; subject: string; previous_value: number; current_value: number; change: number }>;
  priorities: IntelligencePriority[]; alerts: IntelligenceAlert[]; intervention: Intervention;
  supporting_evidence: string[]; missing_evidence: string[]; confidence: number; confidence_explanation: string;
  data_summary: { learners: number; classes: number; attendance_records: number; behaviour_records: number; assessment_records: number };
  trace_id: string; source?: "prepared_example" | "csv_import";
  active_scope?: BeaconActiveScope;
};
export type BeaconScope = { analysis_id?: string; scope_type?: "school" | "metric" | "class" | "learner" | "intervention" | "decision"; scope_id?: string };
export type BeaconActiveScope = { type: BeaconScope["scope_type"]; id?: string | null; name?: string | null };
type BeaconResponseContext = { conversation_id?: string; trace_id: string; analysis_period?: string; active_scope?: BeaconActiveScope };
export type BeaconExplanation =
  | (BeaconResponseContext & { response_type: "conversation"; message: string })
  | (BeaconResponseContext & { response_type: "clarification"; message: string; available_learners: string[] })
  | (BeaconResponseContext & { response_type: "evidence_analysis"; situation: string; why_it_matters: string; supporting_evidence: string[]; recommendation: string; suggested_next_step: string; confidence: number; confidence_explanation: string; missing_evidence: string[]; evidence_source?: string; signals: EvidenceSignal[] });
export type BeaconConversationSummary = { id: string; analysis_id: string; title: string; scope_type: string; scope_id?: string | null; created_at: string; updated_at: string; turn_count: number };
export type BeaconConversation = BeaconConversationSummary & { turns: Array<{ id: string; created_at: string; question: string; answer: BeaconExplanation }> };
export type DecisionBrief = {
  id: string; analysis_id: string; trace_id: string; class_name: string; title: string; situation: string; why_it_matters: string;
  recommendation: string; evidence_summary: string[]; confidence: number; missing_evidence: string[]; priority: string;
  owner: string; due_date: string; review_date: string; status: string; success_metric: string;
  expected_outcomes: Array<{ label: string; current: string; target: string; note: string }>; actions: string[];
  scope_type?: string; scope_id?: string | null; scope_label?: string;
};
export type WorkspaceContext = { school_name: string; school_location: string; user_name: string; user_role: string; updated_at: string };

const baseUrl = process.env.NEXT_PUBLIC_VERIQ_API_URL ?? "http://localhost:8000";
let evidenceCache: EvidencePackage | null = null;

export class VeriqApiError extends Error {
  constructor(message: string, public readonly code = "REQUEST_FAILED") { super(message); }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort("timeout"), 45000);
  const forwardAbort = () => controller.abort("cancelled");
  init?.signal?.addEventListener("abort", forwardAbort, { once: true });
  try { response = await fetch(`${baseUrl}${path}`, { ...init, signal: controller.signal, cache: "no-store" }); }
  catch (error) {
    if (controller.signal.aborted) throw new VeriqApiError("Beacon stopped waiting for this response. Try the question again.", "REQUEST_ABORTED");
    throw new VeriqApiError("Veriq intelligence service is unavailable. Start the backend and try again.", "SERVICE_UNAVAILABLE");
  } finally {
    window.clearTimeout(timeout);
    init?.signal?.removeEventListener("abort", forwardAbort);
  }
  let payload: { success?: boolean; data?: T; error?: { message?: string; code?: string } };
  try { payload = await response.json(); } catch { throw new VeriqApiError("Veriq returned an unreadable response. Please try again.", "INVALID_RESPONSE"); }
  if (!response.ok || !payload.success) throw new VeriqApiError(payload.error?.message ?? "Veriq could not complete this request.", payload.error?.code);
  return payload.data as T;
}

export async function getLatestEvidence(force = false): Promise<EvidencePackage> {
  if (evidenceCache && !force) return evidenceCache;
  evidenceCache = await request<EvidencePackage>("/api/v1/intelligence/latest-evidence");
  return evidenceCache;
}

export async function uploadAndAnalyse(
  files: Record<"attendance" | "behaviour" | "assessments", File>,
  dataUseAcknowledged: boolean,
): Promise<EvidencePackage> {
  const form = new FormData();
  form.append("attendance", files.attendance);
  form.append("behaviour", files.behaviour);
  form.append("assessments", files.assessments);
  form.append("data_use_acknowledged", String(dataUseAcknowledged));
  evidenceCache = await request<EvidencePackage>("/api/v1/imports/analyse", { method: "POST", body: form });
  return evidenceCache;
}

export async function askBeacon(question: string, scope: BeaconScope = {}, conversationId?: string, signal?: AbortSignal): Promise<BeaconExplanation> {
  return request<BeaconExplanation>("/api/v1/beacon/explain", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question, ...scope, conversation_id: conversationId }), signal });
}

export async function getScopedEvidence(scope: BeaconScope): Promise<EvidencePackage> {
  const params = new URLSearchParams({ scope_type: scope.scope_type ?? "school" });
  if (scope.scope_id) params.set("scope_id", scope.scope_id);
  return request<EvidencePackage>(`/api/v1/intelligence/scoped-evidence?${params.toString()}`);
}

export async function getBeaconConversations(): Promise<BeaconConversationSummary[]> {
  return request<BeaconConversationSummary[]>("/api/v1/beacon/conversations");
}

export async function getBeaconConversation(id: string): Promise<BeaconConversation> {
  return request<BeaconConversation>(`/api/v1/beacon/conversations/${id}`);
}

export async function generateDecision(scope: BeaconScope = {}): Promise<DecisionBrief> {
  return request<DecisionBrief>("/api/v1/decisions/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ scope_type: scope.scope_type ?? "intervention", scope_id: scope.scope_id }) });
}

export async function getLatestDecision(): Promise<DecisionBrief | null> {
  return request<DecisionBrief | null>("/api/v1/decisions/latest");
}

export async function updateDecision(id: string, updates: { owner?: string; status?: string }): Promise<DecisionBrief> {
  return request<DecisionBrief>(`/api/v1/decisions/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(updates) });
}

export async function getWorkspace(): Promise<WorkspaceContext> {
  return request<WorkspaceContext>("/api/v1/workspace");
}

export async function updateWorkspace(workspace: Omit<WorkspaceContext, "updated_at">): Promise<WorkspaceContext> {
  evidenceCache = null;
  return request<WorkspaceContext>("/api/v1/workspace", { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(workspace) });
}
