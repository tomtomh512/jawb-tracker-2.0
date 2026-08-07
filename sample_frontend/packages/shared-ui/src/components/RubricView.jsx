import ScoreDial from "./ScoreDial";

export default function RubricView({ rubric }) {
  if (!rubric) return null;
  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
        <ScoreDial score={rubric.overall_score} />
        <div>
          <div style={{ fontWeight: 600 }}>Overall match: {Math.round(rubric.overall_score)} / 100</div>
          <div className="hint">Based on {rubric.resume_name}</div>
        </div>
      </div>

      {rubric.missing_required?.length > 0 && (
        <div className="field">
          <label>Missing required</label>
          <div className="tag-list">
            {rubric.missing_required.map((m, i) => (
              <span className="tag" key={i} style={{ background: "var(--danger-tint)", color: "var(--danger)", borderColor: "var(--danger)" }}>
                {m}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="field-row">
        {rubric.strengths?.length > 0 && (
          <div className="field">
            <label>Strengths</label>
            <ul style={{ margin: 0, paddingLeft: 18 }}>
              {rubric.strengths.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}
        {rubric.weaknesses?.length > 0 && (
          <div className="field">
            <label>Weaknesses</label>
            <ul style={{ margin: 0, paddingLeft: 18 }}>
              {rubric.weaknesses.map((w, i) => (
                <li key={i}>{w}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {rubric.items?.length > 0 && (
        <div style={{ marginTop: 10 }}>
          <label style={{ display: "block", marginBottom: 8, fontSize: 12, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>
            Rubric items
          </label>
          {rubric.items.map((item) => (
            <div className="rubric-item" key={item.id}>
              <div className="rubric-item__head">
                <span className="rubric-item__name">
                  {item.name} {item.required && <span className="rubric-item__req">required</span>}
                </span>
                <span className="rubric-item__score">
                  {item.score}/10 · weighted {item.weighted_score.toFixed(1)}
                </span>
              </div>
              <div className="hint" style={{ marginBottom: 4 }}>{item.description}</div>
              <div style={{ fontSize: 13 }}>{item.reasoning}</div>
              {item.evidence?.length > 0 && (
                <div className="hint" style={{ marginTop: 4 }}>Evidence: {item.evidence.join("; ")}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
