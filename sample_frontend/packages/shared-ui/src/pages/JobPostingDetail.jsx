import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { useApi } from "../api/useApi";
import { useSettings } from "../context/SettingsContext";
import { useToast } from "../context/ToastContext";
import JobPostingForm from "../components/JobPostingForm";
import ResumeSelect from "../components/ResumeSelect";
import RubricView from "../components/RubricView";
import StatusStamp from "../components/StatusStamp";
import { formatDate, formatSalary } from "../constants";

export default function JobPostingDetail() {
  const { id } = useParams();
  const api = useApi();
  const { settings } = useSettings();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [posting, setPosting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);

  const [genResumeId, setGenResumeId] = useState("");
  const [genPrompt, setGenPrompt] = useState(settings.defaultCoverLetterPrompt);
  const [generatingLetter, setGeneratingLetter] = useState(false);
  const [generatingScore, setGeneratingScore] = useState(false);

  function load() {
    setLoading(true);
    api
      .getJobPosting(id)
      .then(setPosting)
      .catch((err) => showToast(err.message, "error"))
      .finally(() => setLoading(false));
  }

  useEffect(load, [id]);

  async function handleSave(payload) {
    try {
      const updated = await api.updateJobPosting(id, payload);
      setPosting(updated);
      setEditing(false);
      showToast("Job posting updated");
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleDelete() {
    if (!confirm("Delete this job posting? This cannot be undone.")) return;
    try {
      await api.deleteJobPosting(id);
      showToast("Job posting deleted");
      navigate("/");
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleGenerateCoverLetter() {
    if (!genResumeId) return showToast("Select a resume first", "error");
    setGeneratingLetter(true);
    try {
      const updated = await api.generateCoverLetter(id, { resume_id: genResumeId, prompt: genPrompt });
      setPosting(updated);
      showToast("Cover letter generated");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setGeneratingLetter(false);
    }
  }

  async function handleGenerateScore() {
    if (!genResumeId) return showToast("Select a resume first", "error");
    setGeneratingScore(true);
    try {
      const updated = await api.generateScore(id, { resume_id: genResumeId });
      setPosting(updated);
      showToast("Score generated");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setGeneratingScore(false);
    }
  }

  if (loading) return <div className="page loading-line">Loading job posting…</div>;
  if (!posting) return <div className="page empty-state">Job posting not found. <Link to="/">Back home</Link></div>;

  return (
    <div className="page">
      <div style={{ marginBottom: 14 }}>
        <Link to="/" className="hint">← Back to all postings</Link>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 12, marginBottom: 16 }}>
        <div>
          <h1 className="mt-0">{posting.title || "Untitled role"} at {posting.company || "Unknown company"}</h1>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <StatusStamp status={posting.status} />
            <span className="hint">Added {formatDate(posting.created_at)}</span>
          </div>
        </div>
        <div className="btn-row">
          {!editing && (
            <button className="btn btn--ghost" onClick={() => setEditing(true)}>
              Edit
            </button>
          )}
          <button className="btn btn--danger" onClick={handleDelete}>
            Delete
          </button>
        </div>
      </div>

      <div className="detail-grid">
        <div>
          {editing ? (
            <div className="card">
              <div className="card__header">
                <h3>Edit job posting</h3>
              </div>
              <div className="card__body">
                <JobPostingForm initial={posting} onSubmit={handleSave} onCancel={() => setEditing(false)} submitLabel="Save changes" />
              </div>
            </div>
          ) : (
            <>
              <div className="card" style={{ marginBottom: 16 }}>
                <div className="card__header">
                  <h3>Details</h3>
                </div>
                <div className="card__body">
                  <div className="field-row" style={{ marginBottom: 14 }}>
                    <DetailField label="Employment type" value={posting.employment_type} />
                    <DetailField label="Location" value={posting.location_raw || [posting.city, posting.state, posting.country].filter(Boolean).join(", ")} />
                    <DetailField label="Remote" value={posting.remote == null ? null : posting.remote ? `Yes${posting.remote_days_per_week ? ` (${posting.remote_days_per_week}d/wk)` : ""}` : "No"} />
                    <DetailField label="Education min." value={posting.education_minimum} />
                    <DetailField label="Education pref." value={posting.education_preferred} />
                  </div>
                  <div className="field-row" style={{ marginBottom: 14 }}>
                    <DetailField label="Salary" value={formatSalary(posting)} />
                    <DetailField label="Bonus" value={boolLabel(posting.bonus)} />
                    <DetailField label="Equity" value={boolLabel(posting.equity)} />
                    <DetailField label="Clearance required" value={boolLabel(posting.clearance_required)} />
                    <DetailField label="Visa sponsorship" value={boolLabel(posting.visa_sponsorship)} />
                  </div>
                  <div className="field-row" style={{ marginBottom: 14 }}>
                    <DetailField label="Link" value={posting.link ? <a href={posting.link} target="_blank" rel="noreferrer">{posting.link}</a> : null} />
                  </div>

                  {posting.skills?.length > 0 && (
                    <div className="field">
                      <label>Skills</label>
                      <div className="tag-list">{posting.skills.map((s, i) => <span className="tag" key={i}>{s}</span>)}</div>
                    </div>
                  )}
                  {posting.requirements?.length > 0 && (
                    <div className="field">
                      <label>Requirements</label>
                      <ul style={{ margin: 0, paddingLeft: 18 }}>{posting.requirements.map((r, i) => <li key={i}>{r}</li>)}</ul>
                    </div>
                  )}
                  {posting.responsibilities?.length > 0 && (
                    <div className="field">
                      <label>Responsibilities</label>
                      <ul style={{ margin: 0, paddingLeft: 18 }}>{posting.responsibilities.map((r, i) => <li key={i}>{r}</li>)}</ul>
                    </div>
                  )}
                  {posting.notes && (
                    <div className="field">
                      <label>Notes</label>
                      <div className="bullet-block">{posting.notes}</div>
                    </div>
                  )}
                </div>
              </div>

              {posting.original && (
                <div className="card" style={{ marginBottom: 16 }}>
                  <div className="card__header">
                    <h3>Original posting text</h3>
                    <button
                      className="btn btn--ghost btn--sm"
                      onClick={() => {
                        navigator.clipboard.writeText(posting.original);
                        showToast("Original copied to clipboard");
                      }}
                    >
                      Copy
                    </button>
                  </div>
                  <div className="card__body">
                    <div className="bullet-block" style={{ maxHeight: 260, overflowY: "auto", color: "var(--text-muted)" }}>
                      {posting.original}
                    </div>
                  </div>
                </div>
              )}

              {posting.cover_letter && (
                <div className="card" style={{ marginBottom: 16 }}>
                  <div className="card__header">
                    <h3>Cover letter</h3>
                    <button
                      className="btn btn--ghost btn--sm"
                      onClick={() => {
                        navigator.clipboard.writeText(posting.cover_letter);
                        showToast("Cover letter copied to clipboard");
                      }}
                    >
                      Copy
                    </button>
                  </div>
                  <div className="card__body">
                    <div className="cover-letter-view">{posting.cover_letter}</div>
                  </div>
                </div>
              )}

              {posting.rubric && (
                <div className="card">
                  <div className="card__header">
                    <h3>Match score</h3>
                  </div>
                  <div className="card__body">
                    <RubricView rubric={posting.rubric} />
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        <div className="card">
          <div className="card__header">
            <h3>Generate</h3>
          </div>
          <div className="card__body">
            <ResumeSelect value={genResumeId} onChange={setGenResumeId} />
            <div className="field">
              <label>Cover letter prompt</label>
              <textarea rows={4} value={genPrompt} onChange={(e) => setGenPrompt(e.target.value)} />
            </div>
            <div className="btn-row" style={{ flexDirection: "column" }}>
              <button className="btn btn--accent btn--block" onClick={handleGenerateCoverLetter} disabled={generatingLetter}>
                {generatingLetter ? "Generating…" : posting.cover_letter ? "Regenerate cover letter" : "Generate cover letter"}
              </button>
              <button className="btn btn--ghost btn--block" onClick={handleGenerateScore} disabled={generatingScore}>
                {generatingScore ? "Scoring…" : posting.rubric ? "Regenerate score" : "Generate score"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function boolLabel(v) {
  if (v == null) return null;
  return v ? "Yes" : "No";
}

function DetailField({ label, value }) {
  return (
    <div className="field">
      <label>{label}</label>
      <div>{value || <span className="hint">—</span>}</div>
    </div>
  );
}
