import type { BeaconContext } from "../lib/presentation-types";

type BeaconContextPanelProps = {
  context: BeaconContext;
  selectedQuestion: string | null;
  onQuestionSelect: (question: string) => void;
  onClose: () => void;
};

export function BeaconContextPanel({ context, selectedQuestion, onQuestionSelect, onClose }: BeaconContextPanelProps) {
  return <aside className="beacon-context-panel" id={`beacon-context-${context.id}`} aria-live="polite">
    <div className="context-rail" aria-hidden="true"><span>✦</span></div>
    <div className="context-main"><div className="context-heading"><div><p className="context-label">BEACON • {context.label}</p><h3>{context.title}</h3></div><button className="context-close" type="button" onClick={onClose} aria-label={`Close Beacon context for ${context.label}`}>×</button></div>
      <p className="context-summary">{selectedQuestion ? `Beacon is helping you explore: ${selectedQuestion}` : context.summary}</p>
      <p className="context-evidence"><span>Evidence</span>{context.evidence}</p>
      <div className="context-questions"><span>Explore with Beacon</span><div>{context.questions.map((question) => <button key={question} type="button" className={selectedQuestion === question ? "selected" : ""} onClick={() => onQuestionSelect(question)}>{question}<b>→</b></button>)}</div></div>
    </div>
  </aside>;
}
