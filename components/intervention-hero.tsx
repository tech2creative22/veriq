type InterventionHeroProps = {
  className: string;
  title: string;
  summary: string;
  confidence: number;
  evidenceSources: string[];
  missingEvidenceCount: number;
  freshness: string;
  onAskBeacon: () => void;
};

export function InterventionHero({ className, title, summary, confidence, evidenceSources, missingEvidenceCount, freshness, onAskBeacon }: InterventionHeroProps) {
  return <section className="intervention-hero page-reveal"><div><p className="intervention-eyebrow">EARLY INTERVENTION · VERIFIED EVIDENCE</p><p className="intervention-class">{className}</p><h1>High intervention opportunity</h1><p className="intervention-title">{title}</p><p className="intervention-summary">{summary}</p><button className="intervention-beacon-button" type="button" onClick={onAskBeacon}>✦ Ask Beacon about this evidence <span>→</span></button></div><div className="intervention-confidence"><span>CONFIDENCE</span><strong>{confidence}%</strong><ul>{evidenceSources.map((source) => <li key={source}><b>✓</b>{source}</li>)}</ul><small>Missing evidence: {missingEvidenceCount} {missingEvidenceCount === 1 ? "source" : "sources"}<br />Freshness: {freshness}</small></div></section>;
}
