type BeaconBriefProps = {
  onUnderstandPattern: () => void;
  headline?: string;
  summary?: string;
  confidence?: number;
  sourceLabel?: string;
};

export function BeaconBrief({
  onUnderstandPattern,
  headline = "I’ve reviewed today’s school evidence.",
  summary = "Overall, your school is healthy. One class deserves attention while the pattern is still early enough to influence.",
  confidence = 87,
  sourceLabel = "Prepared evidence",
}: BeaconBriefProps) {
  return <section className="beacon-brief page-reveal"><div className="beacon-orb"><span>✦</span></div><div className="beacon-copy"><div className="beacon-label"><span className="sparkle">✦</span> BEACON BRIEF <span className="live-dot" /> {sourceLabel.toUpperCase()}</div><h2>{headline}</h2><p>{summary}</p><button className="beacon-action" type="button" onClick={onUnderstandPattern}>Understand the pattern <span>→</span></button></div><div className="brief-confidence"><span>CONFIDENCE</span><strong>{confidence}%</strong><small>Three verified signals explain this confidence</small></div></section>;
}
