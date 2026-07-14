import type { InterventionEvidence } from "../lib/presentation-types";

type InterventionEvidenceProps = { evidence: InterventionEvidence[] };

export function InterventionEvidenceList({ evidence }: InterventionEvidenceProps) {
  return <section className="intervention-section"><div className="intervention-section-heading"><div><p className="eyebrow">VERIFIED EVIDENCE</p><h2>What Beacon is seeing</h2></div><span>Traceable school records</span></div><div className="evidence-list">{evidence.map((item) => <article className={`evidence-item ${item.tone}`} key={item.label}><span className="evidence-marker" /><div><h3>{item.label}</h3><p>{item.detail}</p></div></article>)}</div></section>;
}
