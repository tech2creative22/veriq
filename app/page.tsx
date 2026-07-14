"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "../components/app-shell";
import { AppIcon } from "../components/app-icons";
import {
  getLatestEvidence,
  getWorkspace,
  type ClassSummary,
  type EvidencePackage,
  type EvidenceSignal,
  type SchoolMetric,
} from "../lib/veriq-api";
import "./school-pulse.css";

type ScopeType = "school" | "class" | "metric";
type HealthState = "attention" | "watch" | "stable";

function classState(summary: ClassSummary): HealthState {
  if (summary.risk_score >= 2) return "attention";
  if (summary.risk_score === 1) return "watch";
  return "stable";
}

function stateLabel(state: HealthState) {
  return state === "attention"
    ? "Needs attention"
    : state === "watch"
      ? "Watch closely"
      : "Stable / improving";
}

function valueLabel(value: number, category: string) {
  return category === "behaviour" ? `${value}` : `${value}%`;
}

function changeLabel(change: number, category: string) {
  const prefix = change > 0 ? "+" : "";
  return category === "behaviour"
    ? `${prefix}${change} incidents`
    : `${prefix}${change} pp`;
}

function signalName(signal: EvidenceSignal) {
  if (signal.category === "assessment") return "Assessment";
  return signal.category.charAt(0).toUpperCase() + signal.category.slice(1);
}

function metricValue(metric: SchoolMetric) {
  if (metric.unit === "status") return metric.display_value ?? metric.fact;
  return `${metric.current_value}${metric.unit === "%" ? "%" : ""}`;
}

function metricChange(metric: SchoolMetric) {
  if (metric.unit === "status")
    return metric.tone === "attention" ? "Leadership review" : "Current status";
  const prefix = metric.change > 0 ? "+" : "";
  return `${prefix}${metric.change}${metric.unit === "%" ? " pp" : ` ${metric.unit}`}`;
}

export default function SchoolPulsePage() {
  const router = useRouter();
  const [evidence, setEvidence] = useState<EvidencePackage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [userName, setUserName] = useState("School leader");

  useEffect(() => {
    getWorkspace()
      .then((workspace) => setUserName(workspace.user_name))
      .catch(() => undefined);
    getLatestEvidence(true)
      .then(setEvidence)
      .catch((requestError) =>
        setError(
          requestError instanceof Error
            ? requestError.message
            : "School intelligence could not be loaded.",
        ),
      );
  }, []);

  const learnerCounts = useMemo(() => {
    const learners = evidence?.learner_summaries ?? [];
    return {
      total: learners.length,
      attention: learners.filter((learner) => learner.risk_factors.length >= 2)
        .length,
      watch: learners.filter((learner) => learner.risk_factors.length === 1)
        .length,
      stable: learners.filter((learner) => learner.risk_factors.length === 0)
        .length,
    };
  }, [evidence]);

  const askBeacon = (question: string, scope: ScopeType, scopeId?: string) => {
    if (!evidence) return;
    const params = new URLSearchParams({
      question,
      scope,
      analysisId: evidence.analysis_id,
      focus: "1",
    });
    if (scopeId) params.set("scopeId", scopeId);
    router.push(`/beacon?${params.toString()}`);
  };

  if (error)
    return (
      <AppShell>
        <main className="pulse-exec">
          <section className="pulse-state pulse-state-error" role="alert">
            <AppIcon name="sparkles" size={22} />
            <div>
              <strong>School Pulse is unavailable.</strong>
              <p>{error}</p>
              <button type="button" onClick={() => window.location.reload()}>
                Try again
              </button>
            </div>
          </section>
        </main>
      </AppShell>
    );
  if (!evidence)
    return (
      <AppShell>
        <main className="pulse-exec">
          <section className="pulse-state">
            <span className="pulse-loader" />
            <div>
              <strong>Building the whole-school picture…</strong>
              <p>
                Connecting school, class and learner evidence from the latest
                package.
              </p>
            </div>
          </section>
        </main>
      </AppShell>
    );

  const sourceLabel =
    evidence.source === "csv_import"
      ? "Latest persisted CSV upload"
      : "Prepared evidence package";
  const schoolHealth = evidence.school_metrics.find(
    (metric) => metric.unit === "status",
  );
  const schoolFacts = evidence.school_metrics
    .filter((metric) => metric.unit !== "status")
    .map((metric) => metric.fact);
  const analysisRef = evidence.analysis_id.slice(-8).toUpperCase();

  return (
    <AppShell>
      <main className="pulse-exec">
        <header className="pulse-exec-header page-reveal">
          <div>
            <p className="pulse-kicker">WHOLE-SCHOOL EXECUTIVE VIEW</p>
            <h1>Good morning, {userName.split(" ")[0]}.</h1>
            <p>
              A connected view of <strong>{evidence.school_name}</strong> from
              school health to every monitored learner.
            </p>
          </div>
          <dl className="pulse-source-facts">
            <div>
              <dt>Source</dt>
              <dd>{sourceLabel}</dd>
            </div>
            <div>
              <dt>Reporting period</dt>
              <dd>{evidence.analysis_period}</dd>
            </div>
            <div>
              <dt>Coverage</dt>
              <dd>
                {evidence.data_summary.classes} class
                {evidence.data_summary.classes === 1 ? "" : "es"} ·{" "}
                {evidence.data_summary.learners} learners
              </dd>
            </div>
            <div>
              <dt>Analysis</dt>
              <dd>{analysisRef}</dd>
            </div>
          </dl>
        </header>

        <section className="pulse-beacon" aria-labelledby="pulse-beacon-title">
          <div className="pulse-beacon-mark">
            <AppIcon name="sparkles" size={24} />
          </div>
          <div className="pulse-beacon-copy">
            <p>BEACON · SCHOOL SCOPE</p>
            <h2 id="pulse-beacon-title">
              {schoolHealth?.display_value ?? "Current school evidence"}
            </h2>
            <span>{schoolFacts.join(" ")}</span>
            <button
              type="button"
              onClick={() =>
                askBeacon(
                  "Give me an executive review of the whole school, explain the connected patterns and what leadership should verify next.",
                  "school",
                )
              }
            >
              Explore the whole-school pattern{" "}
              <AppIcon name="arrow-right" size={16} />
            </button>
          </div>
          <div className="pulse-confidence">
            <span>CONFIDENCE</span>
            <strong>{evidence.confidence}%</strong>
            <small>{evidence.confidence_explanation}</small>
          </div>
        </section>

        <section className="pulse-band" aria-labelledby="school-health-title">
          <div className="pulse-section-heading">
            <div>
              <p className="pulse-kicker">SCHOOL</p>
              <h2 id="school-health-title">School health indicators</h2>
              <span>
                Previous and current values from the same evidence package.
              </span>
            </div>
            <button
              type="button"
              className="pulse-text-action"
              onClick={() =>
                askBeacon(
                  "Explain the overall health of the school across attendance, behaviour and assessment.",
                  "school",
                )
              }
            >
              Ask Beacon about school health{" "}
              <AppIcon name="arrow-right" size={14} />
            </button>
          </div>
          <div className="pulse-health-grid">
            {evidence.school_metrics.map((metric) => (
              <article
                className={`pulse-health-card ${metric.tone}`}
                key={metric.id}
              >
                <div className="pulse-health-top">
                  <span>{metric.label}</span>
                  <i>
                    {metric.tone === "attention"
                      ? "Needs review"
                      : "Stable / improving"}
                  </i>
                </div>
                <strong>{metricValue(metric)}</strong>
                {metric.unit !== "status" ? (
                  <div className="pulse-period-values">
                    <span>
                      Previous{" "}
                      <b>
                        {metric.previous_value}
                        {metric.unit === "%" ? "%" : ""}
                      </b>
                    </span>
                    <span>
                      Current{" "}
                      <b>
                        {metric.current_value}
                        {metric.unit === "%" ? "%" : ""}
                      </b>
                    </span>
                  </div>
                ) : (
                  <p>{metric.fact}</p>
                )}
                <div className="pulse-health-foot">
                  <span>{metricChange(metric)}</span>
                  <button
                    type="button"
                    aria-label={`Ask Beacon about ${metric.label}`}
                    onClick={() =>
                      askBeacon(
                        `Explain the current ${metric.label.toLowerCase()} evidence and what changed.`,
                        "metric",
                        metric.id,
                      )
                    }
                  >
                    <AppIcon name="sparkles" size={14} /> Ask Beacon
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section
          className="pulse-hierarchy"
          aria-label="Class and learner overview"
        >
          <div className="pulse-classes">
            <div className="pulse-section-heading">
              <div>
                <p className="pulse-kicker">CLASSES</p>
                <h2>Every class in the evidence</h2>
                <span>
                  {evidence.class_summaries.length} class
                  {evidence.class_summaries.length === 1 ? "" : "es"} compared
                  across the verified signals.
                </span>
              </div>
            </div>
            {evidence.class_summaries.length ? (
              <div className="pulse-class-list">
                {evidence.class_summaries.map((summary) => {
                  const status = classState(summary);
                  return (
                    <article
                      className="pulse-class-row"
                      key={summary.class_name}
                    >
                      <div className="pulse-class-identity">
                        <span className={`pulse-status-dot ${status}`} />
                        <div>
                          <h3>{summary.class_name}</h3>
                          <p>
                            {summary.repeated_absences} repeated absence
                            {summary.repeated_absences === 1 ? "" : "s"}
                          </p>
                        </div>
                        <em className={status}>{stateLabel(status)}</em>
                      </div>
                      <div className="pulse-signal-strip">
                        {summary.signals.map((signal) => (
                          <div key={signal.id}>
                            <span>{signalName(signal)}</span>
                            <strong>
                              {valueLabel(
                                signal.previous_value,
                                signal.category,
                              )}{" "}
                              →{" "}
                              {valueLabel(
                                signal.current_value,
                                signal.category,
                              )}
                            </strong>
                            <small className={signal.severity}>
                              {changeLabel(signal.change, signal.category)} ·{" "}
                              {signal.severity}
                            </small>
                          </div>
                        ))}
                      </div>
                      <button
                        type="button"
                        className="pulse-scope-action"
                        onClick={() =>
                          askBeacon(
                            `Explain the connected evidence pattern for ${summary.class_name}.`,
                            "class",
                            summary.class_name,
                          )
                        }
                      >
                        <AppIcon name="sparkles" size={15} />
                        <span>
                          Ask Beacon<small>{summary.class_name} scope</small>
                        </span>
                        <AppIcon name="arrow-right" size={15} />
                      </button>
                    </article>
                  );
                })}
              </div>
            ) : (
              <div className="pulse-empty">
                <strong>No class summaries are available.</strong>
                <p>
                  Upload connected attendance, behaviour and assessment records
                  to populate the class view.
                </p>
              </div>
            )}
          </div>

          <aside className="pulse-learners">
            <div className="pulse-section-heading">
              <div>
                <p className="pulse-kicker">LEARNERS</p>
                <h2>Monitoring distribution</h2>
                <span>
                  Continuous monitoring across all connected learners.
                </span>
              </div>
            </div>
            <div className="pulse-learner-total">
              <span>All monitored learners</span>
              <strong>{learnerCounts.total}</strong>
              <small>
                from {evidence.data_summary.classes} class
                {evidence.data_summary.classes === 1 ? "" : "es"}
              </small>
            </div>
            <div className="pulse-learner-breakdown">
              <div className="attention">
                <span>High attention</span>
                <strong>{learnerCounts.attention}</strong>
                <small>2+ risk factors</small>
              </div>
              <div className="watch">
                <span>Watch</span>
                <strong>{learnerCounts.watch}</strong>
                <small>1 risk factor</small>
              </div>
              <div className="stable">
                <span>Stable / improving</span>
                <strong>{learnerCounts.stable}</strong>
                <small>0 risk factors</small>
              </div>
            </div>
            <button
              type="button"
              className="pulse-monitor-action"
              onClick={() => router.push("/early-intervention")}
            >
              View all monitored cases <AppIcon name="arrow-right" size={15} />
            </button>
            <p className="pulse-monitor-note">
              Opens the Early Intervention workspace with every learner case.
            </p>
          </aside>
        </section>

        <section className="pulse-bottom-grid">
          <div id="priorities" className="pulse-priorities">
            <div className="pulse-section-heading">
              <div>
                <p className="pulse-kicker">LEADERSHIP PRIORITIES</p>
                <h2>Priority patterns</h2>
                <span>Class-scoped findings from this analysis.</span>
              </div>
            </div>
            {evidence.priorities.length ? (
              <div className="pulse-priority-list">
                {evidence.priorities.map((priority) => (
                  <article key={priority.id}>
                    <span
                      className={`pulse-priority-level ${priority.level.toLowerCase()}`}
                    >
                      {priority.level} priority
                    </span>
                    <div>
                      <h3>{priority.title}</h3>
                      <p>{priority.description}</p>
                      <small>
                        {priority.class_name} · {evidence.analysis_period}
                      </small>
                    </div>
                    <button
                      type="button"
                      onClick={() =>
                        askBeacon(
                          `Explain why ${priority.class_name} is prioritised and identify the strongest verified evidence.`,
                          "class",
                          priority.scope_id,
                        )
                      }
                    >
                      <AppIcon name="sparkles" size={15} /> Explore with Beacon
                    </button>
                  </article>
                ))}
              </div>
            ) : (
              <div className="pulse-empty">
                <strong>No priority patterns in this package.</strong>
                <p>Beacon continues monitoring the current school evidence.</p>
              </div>
            )}
          </div>

          <div id="latest-findings" className="pulse-changes">
            <div className="pulse-section-heading">
              <div>
                <p className="pulse-kicker">LATEST EVIDENCE</p>
                <h2>Recent changes</h2>
                <span>Metric-scoped updates from analysis {analysisRef}.</span>
              </div>
            </div>
            {evidence.alerts.length ? (
              <div className="pulse-change-list">
                {evidence.alerts.map((alert) => (
                  <article key={alert.id}>
                    <span className={`pulse-change-marker ${alert.tone}`} />
                    <div>
                      <h3>{alert.title}</h3>
                      <p>{alert.detail}</p>
                    </div>
                    <button
                      type="button"
                      aria-label={`Ask Beacon about ${alert.title}`}
                      onClick={() =>
                        askBeacon(
                          `Explain this latest ${alert.category} evidence change.`,
                          "metric",
                          evidence.school_metrics.find(
                            (metric) => metric.category === alert.category,
                          )?.id ?? alert.category,
                        )
                      }
                    >
                      <AppIcon name="sparkles" size={14} /> Ask Beacon
                    </button>
                  </article>
                ))}
              </div>
            ) : (
              <div className="pulse-empty">
                <strong>No recent changes recorded.</strong>
                <p>This evidence package has no metric alerts.</p>
              </div>
            )}
          </div>
        </section>

        <footer className="pulse-trace">
          <span>{sourceLabel}</span>
          <span>Reporting period: {evidence.analysis_period}</span>
          <span>Analysis {analysisRef}</span>
          <span>Trace {evidence.trace_id.slice(-8).toUpperCase()}</span>
        </footer>
      </main>
    </AppShell>
  );
}
