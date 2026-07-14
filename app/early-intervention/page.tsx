"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "../../components/app-shell";
import { AppIcon } from "../../components/app-icons";
import { getLatestEvidence, type EvidencePackage, type LearnerSummary } from "../../lib/veriq-api";
import "./early-intervention.css";

type CaseStatus = "attention" | "watch" | "stable";
type CaseFilter = "all" | CaseStatus;

function caseStatus(learner: LearnerSummary): CaseStatus {
  if (learner.risk_factors.length >= 2) return "attention";
  if (learner.risk_factors.length === 1) return "watch";
  return "stable";
}

function difference(previous: number | null, current: number | null) {
  if (previous === null || current === null) return null;
  return Number((current - previous).toFixed(1));
}

function movement(previous: number | null, current: number | null, unit = "%") {
  if (previous === null || current === null) return { range: "Not available", change: "Awaiting records", tone: "neutral" };
  const delta = difference(previous, current) ?? 0;
  return {
    range: `${previous}${unit} → ${current}${unit}`,
    change: `${delta > 0 ? "+" : ""}${delta}${unit === "%" ? "pp" : ""}`,
    tone: delta < 0 ? "decline" : delta > 0 ? "improve" : "neutral",
  };
}

function behaviourMovement(learner: LearnerSummary) {
  const delta = learner.behaviour_current - learner.behaviour_previous;
  return {
    range: `${learner.behaviour_previous} → ${learner.behaviour_current}`,
    change: `${delta > 0 ? "+" : ""}${delta} incident${Math.abs(delta) === 1 ? "" : "s"}`,
    tone: delta > 0 ? "decline" : delta < 0 ? "improve" : "neutral",
  };
}

function patternLabels(learner: LearnerSummary) {
  const labels: string[] = [];
  const attendance = difference(learner.attendance_previous, learner.attendance_current);
  const assessment = difference(learner.assessment_previous, learner.assessment_current);
  const behaviour = learner.behaviour_current - learner.behaviour_previous;
  if (attendance !== null && attendance < 0) labels.push("Attendance falling");
  if (behaviour > 0) labels.push("Incidents rising");
  if (assessment !== null && assessment < 0) labels.push("Assessment falling");
  if (attendance !== null && attendance > 0) labels.push("Attendance improving");
  if (behaviour < 0) labels.push("Behaviour improving");
  if (assessment !== null && assessment > 0) labels.push("Assessment improving");
  if (!labels.length) labels.push("Consistent across signals");
  return labels;
}

const filters: Array<{ id: CaseFilter; label: string }> = [
  { id: "all", label: "All cases" },
  { id: "attention", label: "Needs attention" },
  { id: "watch", label: "Watch" },
  { id: "stable", label: "Stable / improving" },
];

export default function EarlyInterventionPage() {
  const router = useRouter();
  const [evidence, setEvidence] = useState<EvidencePackage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<CaseFilter>("all");
  const [focusedLearnerId, setFocusedLearnerId] = useState<string>();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("scope") === "learner" && params.get("scopeId")) setFocusedLearnerId(params.get("scopeId") ?? undefined);
    getLatestEvidence(true).then(setEvidence).catch((requestError) => setError(requestError instanceof Error ? requestError.message : "Monitoring evidence could not be loaded."));
  }, []);

  const learners = useMemo(() => evidence?.learner_summaries ?? [], [evidence]);
  const counts = useMemo(() => ({
    total: learners.length,
    attention: learners.filter((learner) => caseStatus(learner) === "attention").length,
    watch: learners.filter((learner) => caseStatus(learner) === "watch").length,
    stable: learners.filter((learner) => caseStatus(learner) === "stable").length,
  }), [learners]);
  const visibleLearners = useMemo(() => learners.filter((learner) => filter === "all" || caseStatus(learner) === filter), [filter, learners]);

  const investigate = (learner: LearnerSummary) => {
    const params = new URLSearchParams({
      scope: "learner",
      scopeId: learner.student_id,
      question: `Give me a performance review for ${learner.learner_name} and explain the connected evidence pattern.`,
      focus: "1",
    });
    if (evidence) params.set("analysisId", evidence.analysis_id);
    router.push(`/beacon?${params.toString()}`);
  };

  return <AppShell activeNavigation="Early Intervention"><main className="monitoring-page">
    <header className="monitoring-header page-reveal">
      <div><p className="monitoring-eyebrow">CONTINUOUS EARLY SIGNALS</p><h1>Early Intervention</h1><p>Monitor emerging evidence patterns across every learner, including those who are stable or improving, before support becomes urgent.</p></div>
      <div className="monitoring-period"><span>Current evidence package</span><strong>{evidence?.analysis_period ?? "Loading reporting period…"}</strong><small>{evidence?.source === "csv_import" ? "Latest persisted upload" : "Verified school evidence"}</small></div>
    </header>

    {error ? <section className="monitoring-state monitoring-error" role="alert"><strong>Monitoring evidence is unavailable.</strong><p>{error}</p><button type="button" onClick={() => window.location.reload()}>Try again</button></section> : null}
    {!evidence && !error ? <section className="monitoring-state"><span className="monitoring-loader" /><strong>Building the learner monitoring view…</strong><p>Reviewing attendance, behaviour and assessment records.</p></section> : null}

    {evidence ? <>
      {focusedLearnerId ? <section className="monitoring-focus-note"><AppIcon name="sparkles" size={17} /><div><strong>Opened from a scoped workflow</strong><span>The selected learner is highlighted below, while this page continues to show the full school monitoring picture.</span></div><button type="button" onClick={() => { setFocusedLearnerId(undefined); window.history.replaceState({}, "", "/early-intervention"); }}>Clear highlight</button></section> : null}

      <section className="monitoring-summary" aria-label="Monitoring summary">
        <article><span>Total monitored</span><strong>{counts.total}</strong><small>learners with connected records</small></article>
        <article className="attention"><span>High attention</span><strong>{counts.attention}</strong><small>multiple concerning signals</small></article>
        <article className="watch"><span>Watch</span><strong>{counts.watch}</strong><small>one emerging signal</small></article>
        <article className="stable"><span>Stable / improving</span><strong>{counts.stable}</strong><small>continuous monitoring continues</small></article>
      </section>

      <section className="monitoring-workspace">
        <div className="monitoring-toolbar"><div><p className="monitoring-eyebrow">MONITORED CASES</p><h2>Connected learner patterns</h2><span>Compare how attendance, behaviour and assessment combine differently for each learner.</span></div><div className="monitoring-filters" role="group" aria-label="Filter monitored cases">{filters.map((item) => <button className={filter === item.id ? "active" : ""} key={item.id} type="button" aria-pressed={filter === item.id} onClick={() => setFilter(item.id)}>{item.label}<span>{item.id === "all" ? counts.total : counts[item.id]}</span></button>)}</div></div>

        {visibleLearners.length ? <div className="monitoring-case-list">{visibleLearners.map((learner) => {
          const status = caseStatus(learner);
          const attendance = movement(learner.attendance_previous, learner.attendance_current);
          const behaviour = behaviourMovement(learner);
          const assessment = movement(learner.assessment_previous, learner.assessment_current);
          return <article className={`monitoring-case ${focusedLearnerId === learner.student_id ? "focused" : ""}`} key={learner.student_id}>
            <div className="case-identity"><span className={`case-status-marker ${status}`} /><div><div className="case-title-line"><h3>{learner.learner_name}</h3><span className={`case-status ${status}`}>{status === "attention" ? "High attention" : status === "watch" ? "Watch" : "Stable / improving"}</span></div><p>{learner.class_name} <i /> Learner ID {learner.student_id}</p><div className="case-pattern-labels">{patternLabels(learner).map((label) => <span key={label}>{label}</span>)}</div></div></div>
            <div className="pattern-signature" aria-label={`${learner.learner_name} evidence pattern`}>
              <div className={attendance.tone}><span>A</span><p>Attendance</p><strong>{attendance.range}</strong><small>{attendance.change}</small></div>
              <div className={behaviour.tone}><span>B</span><p>Behaviour</p><strong>{behaviour.range}</strong><small>{behaviour.change}</small></div>
              <div className={assessment.tone}><span>P</span><p>Assessment</p><strong>{assessment.range}</strong><small>{assessment.change}</small></div>
            </div>
            <button className="investigate-action" type="button" onClick={() => investigate(learner)}><AppIcon name="sparkles" size={16} /><span>Investigate with Beacon<small>Open this learner’s verified evidence</small></span><AppIcon name="arrow-right" size={15} /></button>
          </article>;
        })}</div> : <section className="monitoring-empty"><strong>No cases match this filter.</strong><p>The learners remain monitored. Choose another status to see their current patterns.</p><button type="button" onClick={() => setFilter("all")}>View all cases</button></section>}
      </section>

      <footer className="monitoring-workflow-note"><div><AppIcon name="sparkles" size={18} /><span><strong>Investigate with Beacon</strong> to understand one learner’s connected pattern.</span></div><div><AppIcon name="clipboard" size={18} /><span><strong>Create a Decision Brief</strong> in Beacon when leadership is ready to formalise action.</span></div></footer>
    </> : null}
  </main></AppShell>;
}
