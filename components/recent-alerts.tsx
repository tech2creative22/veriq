import type { Alert } from "../lib/presentation-types";

type RecentAlertsProps = {
  alerts: Alert[];
  activeId: string | null;
  onAskBeacon: (alert: Alert) => void;
  renderContext: (id: string) => React.ReactNode;
};

export function RecentAlerts({ alerts, activeId, onAskBeacon, renderContext }: RecentAlertsProps) {
  return <section className="alerts-card" id="latest-findings"><div className="section-heading"><div><p className="eyebrow">ACTIVITY</p><h2>Latest Beacon findings</h2></div><span className="section-meta">Latest 3</span></div><div className="alerts-list">{alerts.map((alert) => <div key={alert.id}><article className={`alert-row${activeId === alert.id ? " is-active" : ""}`}><span className={`alert-dot ${alert.tone}`} /><div><h3>{alert.title}</h3><p>{alert.detail}</p><small className="alert-why"><b>Why it matters:</b> {alert.beacon.summary}</small><button className="alert-beacon-action" type="button" onClick={() => onAskBeacon(alert)} aria-expanded={activeId === alert.id}><span>✦</span> Ask Beacon</button></div><time>{alert.time}</time></article>{activeId === alert.id ? renderContext(alert.id) : null}</div>)}</div></section>;
}
