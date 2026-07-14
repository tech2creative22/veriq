"use client";

import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "../../components/app-shell";
import { AppIcon } from "../../components/app-icons";
import {
  askBeacon, generateDecision, getBeaconConversation, getBeaconConversations, getLatestEvidence,
  type BeaconConversationSummary, type BeaconExplanation, type BeaconScope,
  type EvidencePackage, type EvidenceSignal,
} from "../../lib/veriq-api";
import "./beacon.css";
import "./beacon-workspace.css";

type ConversationTurn = { id: number | string; question: string; answer?: BeaconExplanation; error?: string };
type ActiveEvidenceView = {
  label: string; scope: BeaconScope; signals: EvidenceSignal[]; confidence: number;
  confidenceExplanation: string; missingEvidence: string[]; analysisPeriod: string;
  traceId: string; sourceLabel: string;
};

function defaultEvidenceView(evidence: EvidencePackage): ActiveEvidenceView {
  return {
    label: evidence.class_name,
    scope: { analysis_id: evidence.analysis_id, scope_type: "school" },
    signals: evidence.signals,
    confidence: evidence.confidence,
    confidenceExplanation: evidence.confidence_explanation,
    missingEvidence: evidence.missing_evidence,
    analysisPeriod: evidence.analysis_period,
    traceId: evidence.trace_id,
    sourceLabel: evidence.source === "csv_import" ? "Latest CSV upload" : "Prepared verified evidence",
  };
}

export default function BeaconPage() {
  const router = useRouter();
  const [evidence, setEvidence] = useState<EvidencePackage | null>(null);
  const [evidenceError, setEvidenceError] = useState<string | null>(null);
  const [turns, setTurns] = useState<ConversationTurn[]>([]);
  const [composer, setComposer] = useState("");
  const [composerError, setComposerError] = useState<string | null>(null);
  const [thinking, setThinking] = useState(false);
  const [activeQuestion, setActiveQuestion] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string>();
  const [conversations, setConversations] = useState<BeaconConversationSummary[]>([]);
  const [activeEvidenceView, setActiveEvidenceView] = useState<ActiveEvidenceView | null>(null);
  const [generatingDecision, setGeneratingDecision] = useState(false);
  const [decisionError, setDecisionError] = useState<string | null>(null);
  const thinkingRef = useRef(false);
  const requestControllerRef = useRef<AbortController | null>(null);
  const initialQuestionAsked = useRef(false);
  const scopeRef = useRef<BeaconScope>({ scope_type: "school" });
  const composerInputRef = useRef<HTMLInputElement>(null);

  const refreshConversations = useCallback(() => {
    getBeaconConversations().then(setConversations).catch(() => undefined);
  }, []);

  const applyAnswerContext = useCallback((answer: BeaconExplanation) => {
    if (answer.response_type !== "evidence_analysis" || !answer.active_scope) return;
    const scope: BeaconScope = {
      analysis_id: evidence?.analysis_id,
      scope_type: answer.active_scope.type,
      scope_id: answer.active_scope.id ?? undefined,
    };
    setActiveEvidenceView({
      label: answer.active_scope.name ?? answer.active_scope.id ?? "Current evidence",
      scope,
      signals: answer.signals,
      confidence: answer.confidence,
      confidenceExplanation: answer.confidence_explanation,
      missingEvidence: answer.missing_evidence,
      analysisPeriod: answer.analysis_period ?? evidence?.analysis_period ?? "Current reporting period",
      traceId: answer.trace_id,
      sourceLabel: answer.evidence_source === "csv_import" ? "Latest CSV upload" : "Verified evidence",
    });
    scopeRef.current = scope;
  }, [evidence]);

  const ask = useCallback(async (nextQuestion: string, scopeOverride?: BeaconScope) => {
    const trimmedQuestion = nextQuestion.trim();
    if (trimmedQuestion.length < 2) { setComposerError("Enter at least two characters."); return; }
    if (thinkingRef.current) return;
    thinkingRef.current = true;
    setThinking(true); setActiveQuestion(trimmedQuestion); setComposer(""); setComposerError(null);
    const turnId = Date.now();
    const controller = new AbortController();
    requestControllerRef.current = controller;
    try {
      const answer = await askBeacon(trimmedQuestion, scopeOverride ?? scopeRef.current, conversationId, controller.signal);
      setTurns((current) => [...current, { id: turnId, question: trimmedQuestion, answer }]);
      if (answer.conversation_id) setConversationId(answer.conversation_id);
      applyAnswerContext(answer);
      refreshConversations();
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : "Beacon could not answer right now.";
      setTurns((current) => [...current, { id: turnId, question: trimmedQuestion, error: message }]);
    } finally {
      thinkingRef.current = false; requestControllerRef.current = null;
      setThinking(false); setActiveQuestion(null);
    }
  }, [applyAnswerContext, conversationId, refreshConversations]);

  useEffect(() => {
    getLatestEvidence(true).then((currentEvidence) => {
      setEvidence(currentEvidence);
      setActiveEvidenceView(defaultEvidenceView(currentEvidence));
      refreshConversations();
      const params = new URLSearchParams(window.location.search);
      const scopeType = params.get("scope") as BeaconScope["scope_type"] | null;
      scopeRef.current = { analysis_id: params.get("analysisId") ?? currentEvidence.analysis_id, scope_type: scopeType ?? "school", scope_id: params.get("scopeId") ?? undefined };
      const initialQuestion = params.get("question");
      if (params.get("focus") === "1") window.setTimeout(() => composerInputRef.current?.focus(), 0);
      if (initialQuestion && !initialQuestionAsked.current) { initialQuestionAsked.current = true; void ask(initialQuestion, scopeRef.current); }
    }).catch((requestError) => setEvidenceError(requestError instanceof Error ? requestError.message : "Verified evidence could not be loaded."));
    // This bootstraps the current analysis and optional URL question once per page visit.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const submitQuestion = (event: FormEvent<HTMLFormElement>) => { event.preventDefault(); void ask(composer); };
  const clearSession = () => {
    setTurns([]); setConversationId(undefined); setComposer(""); setComposerError(null); setActiveQuestion(null);
    window.history.replaceState({}, "", "/beacon");
    scopeRef.current = { analysis_id: evidence?.analysis_id, scope_type: "school" };
    if (evidence) setActiveEvidenceView(defaultEvidenceView(evidence));
  };
  const openConversation = async (id: string) => {
    if (thinking) return;
    try {
      const conversation = await getBeaconConversation(id);
      setConversationId(conversation.id);
      setTurns(conversation.turns.map((turn) => ({ id: turn.id, question: turn.question, answer: turn.answer })));
      scopeRef.current = { analysis_id: evidence?.analysis_id, scope_type: conversation.scope_type as BeaconScope["scope_type"], scope_id: conversation.scope_id ?? undefined };
      const lastGrounded = [...conversation.turns].reverse().find((turn) => turn.answer.response_type === "evidence_analysis");
      if (lastGrounded) applyAnswerContext(lastGrounded.answer);
    } catch (requestError) {
      setComposerError(requestError instanceof Error ? requestError.message : "This conversation could not be opened.");
    }
  };

  const className = evidence?.class_name ?? "Grade 7A";
  const suggestedQuestions = [`Why does ${className} deserve attention now?`, "Show me the strongest evidence.", "What should leadership do first?", "What should leadership verify next?"] as const;
  const view = activeEvidenceView;
  const confidence = view?.confidence ?? evidence?.confidence ?? 87;
  const contextLabel = view?.label ?? className;
  const contextSignals = view?.signals ?? evidence?.signals ?? [];
  const contextMissingEvidence = view?.missingEvidence ?? evidence?.missing_evidence ?? [];
  const createDecisionBrief = async () => {
    if (generatingDecision) return;
    const scope = view?.scope ?? scopeRef.current;
    setGeneratingDecision(true);
    setDecisionError(null);
    try {
      await generateDecision(scope);
      router.push("/decision-brief");
    } catch (requestError) {
      setDecisionError(requestError instanceof Error ? requestError.message : "Beacon could not create the Decision Brief.");
      setGeneratingDecision(false);
    }
  };

  return <AppShell activeNavigation="Beacon"><main className="beacon-page beacon-advisor-page">
    <header className="beacon-advisor-header page-reveal">
      <div className="beacon-advisor-title"><span><AppIcon name="sparkles" size={24} /></span><div><p>BEACON</p><h1>Your evidence-grounded educational advisor.</h1><small>I review verified school signals, explain why they matter, and help leadership decide what to do next.</small></div></div>
      <div className="beacon-context-summary"><span>{contextLabel}</span><strong>{confidence}% confidence</strong><small>{view?.sourceLabel ?? "Verified evidence"}</small></div>
    </header>

    <div className="beacon-advisor-grid">
      <aside className="beacon-session-rail" aria-label="Beacon session navigation">
        <button className="beacon-new-conversation" type="button" onClick={clearSession} disabled={thinking}><AppIcon name="plus" size={17} />New conversation</button>
        <section className="beacon-session-section"><div className="beacon-session-heading"><p>RECENT CONVERSATIONS</p><span>{conversations.length}</span></div>{conversations.length ? <div className="beacon-history-list">{conversations.map((conversation) => <button className={conversation.id === conversationId ? "active" : ""} key={conversation.id} type="button" onClick={() => void openConversation(conversation.id)}><strong>{conversation.title}</strong><small>{conversation.turn_count} question{conversation.turn_count === 1 ? "" : "s"} · saved</small></button>)}</div> : <p className="beacon-session-empty">Your evidence conversations will be saved here for the current analysis.</p>}</section>
        <section className="beacon-session-section"><div className="beacon-session-heading"><p>THIS CONVERSATION</p><span>{turns.length}</span></div>{turns.length ? <ol className="beacon-session-list">{turns.map((turn, index) => <li key={turn.id}><span>{index + 1}</span><div><strong>{turn.question}</strong><small>{turn.answer?.response_type === "conversation" ? "Conversation" : turn.answer?.response_type === "clarification" ? "Needs clarification" : turn.answer ? "Evidence-grounded answer" : "Transparent error"}</small></div></li>)}</ol> : <p className="beacon-session-empty">Ask a question to begin a saved conversation.</p>}</section>
        <section className="beacon-session-section"><div className="beacon-session-heading"><p>SUGGESTED QUESTIONS</p></div><div className="beacon-rail-questions">{suggestedQuestions.map((question) => <button key={question} type="button" onClick={() => void ask(question)} disabled={thinking}>{question}<AppIcon name="arrow-right" size={14} /></button>)}</div></section>
      </aside>

      <section className="beacon-conversation" aria-live="polite">
        <article className="beacon-opening-message"><div className="beacon-message-identity"><span><AppIcon name="sparkles" size={17} /></span><div><strong>Beacon</strong><small>Evidence advisor</small></div></div><p>I’ve reviewed the current evidence for <strong>{contextLabel}</strong>. I can explain the connected pattern, show the strongest verified facts, or help turn the evidence into a practical next step.</p><div className="beacon-opening-evidence">{contextSignals.length ? contextSignals.map((signal) => <span key={signal.id}>{signal.fact}</span>) : <span>{evidenceError ?? "Loading the latest verified evidence…"}</span>}</div></article>

        {turns.map((turn) => <div className="beacon-conversation-turn" key={turn.id}><div className="beacon-user-question"><span>You</span><p>{turn.question}</p></div>
          {turn.answer?.response_type === "conversation" ? <article className="beacon-grounded-answer beacon-conversational-answer"><div className="beacon-message-identity"><span><AppIcon name="sparkles" size={17} /></span><div><strong>Beacon</strong><small>Educational advisor</small></div></div><p>{turn.answer.message}</p></article>
          : turn.answer?.response_type === "clarification" ? <article className="beacon-grounded-answer beacon-clarification-answer"><div className="beacon-message-identity"><span><AppIcon name="sparkles" size={17} /></span><div><strong>Beacon</strong><small>Clarification needed</small></div></div><p>{turn.answer.message}</p><div>{turn.answer.available_learners.map((learner) => <button type="button" key={learner} onClick={() => void ask(`Give me the performance for ${learner}`)}>{learner}</button>)}</div></article>
          : turn.answer ? <article className="beacon-grounded-answer"><div className="beacon-message-identity"><span><AppIcon name="sparkles" size={17} /></span><div><strong>Beacon</strong><small>Grounded in traceable evidence</small></div></div><div className="beacon-answer-story"><section><p>SITUATION</p><span>{turn.answer.situation}</span></section><section><p>WHY IT MATTERS</p><span>{turn.answer.why_it_matters}</span></section><section><p>BEACON RECOMMENDATION</p><span>{turn.answer.recommendation}</span></section></div><section className="beacon-cited-evidence"><p>STRONGEST EVIDENCE</p><ul>{turn.answer.supporting_evidence.map((fact) => <li key={fact}>{fact}</li>)}</ul></section><div className="beacon-answer-trust"><div><span>CONFIDENCE</span><strong>{turn.answer.confidence}%</strong></div><p>{turn.answer.confidence_explanation}<br />{turn.answer.missing_evidence[0] ?? "No evidence gap was reported for this scope."}</p></div><div className="beacon-next-step"><span>NEXT STEP</span><p>{turn.answer.suggested_next_step}</p></div><div className="beacon-trace-reference">Reporting period: {turn.answer.analysis_period ?? "current upload"} · Trace {turn.answer.trace_id.slice(-8)}</div></article>
          : <article className="beacon-grounded-answer beacon-transparent-error"><div className="beacon-message-identity"><span><AppIcon name="sparkles" size={17} /></span><div><strong>Beacon</strong><small>Transparent status</small></div></div><p>{turn.error}</p><small>I will not create an answer that cannot be grounded in verified evidence.</small><button type="button" onClick={() => void ask(turn.question)}>Try this question again</button></article>}
        </div>)}

        {thinking ? <article className="beacon-thinking-state"><span><AppIcon name="sparkles" size={17} /></span><p>Reviewing verified evidence for “{activeQuestion}”</p><i /><i /><i /><button type="button" onClick={() => requestControllerRef.current?.abort()}>Cancel</button></article> : null}
        <form className="beacon-composer" onSubmit={submitQuestion}><label htmlFor="beacon-question">Ask Beacon about the current school evidence</label><div><input ref={composerInputRef} id="beacon-question" value={composer} onChange={(event) => { setComposer(event.target.value); setComposerError(null); }} placeholder="Ask Beacon anything about this evidence…" maxLength={500} disabled={thinking} /><button type="submit" aria-label="Send question" disabled={thinking || composer.trim().length < 2}><AppIcon name="send" size={18} /></button></div><small>{composerError ?? `${composer.length}/500 · Evidence questions remain grounded in the current evidence package.`}</small></form>
      </section>

      <aside className="beacon-evidence-rail" aria-label="Current Beacon evidence and actions">
        <section><div className="beacon-evidence-heading"><span><AppIcon name="sparkles" size={16} /></span><div><p>CURRENT EVIDENCE</p><h2>{contextLabel}</h2></div></div><div className="beacon-signal-list">{contextSignals.length ? contextSignals.map((signal) => <article key={signal.id}><span className={`beacon-signal-dot ${signal.severity}`} /><div><strong>{signal.category}</strong><p>{signal.fact}</p></div></article>) : <p className="beacon-evidence-loading">{evidenceError ?? "Loading verified signals…"}</p>}</div><small className="beacon-source-reference">{view?.analysisPeriod ?? evidence?.analysis_period}<br />Trace {(view?.traceId ?? evidence?.trace_id ?? "").slice(-8)}</small></section>
        <section className="beacon-confidence-panel"><p>WHY THIS CONFIDENCE</p><strong>{confidence}%</strong><span>{view?.confidenceExplanation ?? evidence?.confidence_explanation ?? "Confidence will be explained when evidence is ready."}</span><small>{contextMissingEvidence.length ? `${contextMissingEvidence.length} visible evidence gap${contextMissingEvidence.length === 1 ? "" : "s"}` : "No missing evidence reported for this scope"}</small></section>
        <section className="beacon-decision-panel"><p>FROM EVIDENCE TO ACTION</p><h2>Formalise this response.</h2><span>Create a scoped Decision Brief for {contextLabel} with an owner, target and due date. Early Intervention remains your school-wide monitoring workspace.</span><button type="button" onClick={() => void createDecisionBrief()} disabled={generatingDecision || !evidence}><AppIcon name="clipboard" size={16} />{generatingDecision ? "Creating Decision Brief…" : "Create scoped Decision Brief"}</button>{decisionError ? <small className="beacon-decision-error" role="alert">{decisionError}</small> : null}<button className="beacon-return-action" type="button" onClick={() => router.push("/early-intervention")}>View all monitored cases<AppIcon name="arrow-right" size={15} /></button><button className="beacon-return-action" type="button" onClick={() => router.push("/")}>Return to School Pulse<AppIcon name="arrow-right" size={15} /></button></section>
      </aside>
    </div>
  </main></AppShell>;
}
