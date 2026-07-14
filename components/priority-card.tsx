import Link from "next/link";
import type { BeaconContext, Priority } from "../lib/presentation-types";

type PriorityCardProps = Priority & {
  isActive: boolean;
  onAskBeacon: (context: BeaconContext) => void;
};

export function PriorityCard({ level, title, description, action, href, icon, beacon, isActive, onAskBeacon }: PriorityCardProps) {
  return <article className={`priority-card${isActive ? " is-active" : ""}`}>
    <span className={`priority-icon ${level.toLowerCase()}`}>{icon}</span>
    <div className="priority-content"><div className="priority-meta"><span className={`priority-pill ${level.toLowerCase()}`}>{level} priority</span><span>Today</span></div><h3>{title}</h3><p>{description}</p>
      {href ? <Link className="inline-action" href={href}>{action} <span>→</span></Link> : <button className="inline-action" type="button" onClick={() => onAskBeacon(beacon)} aria-expanded={isActive}>{action} <span>→</span></button>}
    </div>
  </article>;
}
