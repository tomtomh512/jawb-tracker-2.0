export default function ScoreDial({ score }) {
  if (score == null) return <span className="hint">—</span>;
  const cls = score >= 70 ? "" : score >= 40 ? " score-dial--mid" : " score-dial--low";
  return <span className={`score-dial${cls}`}>{Math.round(score)}</span>;
}
