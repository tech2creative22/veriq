import type { BeaconContext, Metric } from "../lib/presentation-types";

type MetricCardProps = Metric & {
  isActive: boolean;
  onAskBeacon: (context: BeaconContext) => void;
};

export function MetricCard({ label, value, detail, change, tone, icon, insight, beacon, isActive, onAskBeacon }: MetricCardProps) {
  return <article className={`metric-card${isActive ? " is-active" : ""}`}>
    <div className="metric-top"><span className={`metric-icon ${tone}`}>{icon}</span><span className={`metric-change ${tone}`}>{change}</span></div>
    <p>{label}</p><h3>{value}</h3><small>{detail}</small>
    <p className="metric-beacon-insight"><span>✦ Beacon</span>{insight}</p>
    <button className="ask-beacon" type="button" onClick={() => onAskBeacon(beacon)} aria-expanded={isActive}>
      <span>✦</span> Ask Beacon
    </button>
  </article>;
}
