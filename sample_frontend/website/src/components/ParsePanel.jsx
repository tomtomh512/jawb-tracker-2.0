import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApi } from "../api/useApi";
import { useSettings } from "../context/SettingsContext";
import { useToast } from "../context/ToastContext";
import ResumeSelect from "./ResumeSelect";
import { ApiError } from "../api/client";

export default function ParsePanel({ onCreated }) {
  const api = useApi();
  const { settings } = useSettings();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [link, setLink] = useState("");
  const [content, setContent] = useState("");
  const [includeCoverLetter, setIncludeCoverLetter] = useState(false);
  const [includeScore, setIncludeScore] = useState(false);
  const [resumeId, setResumeId] = useState("");
  const [prompt, setPrompt] = useState(settings.defaultCoverLetterPrompt);
  const [promptTouched, setPromptTouched] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const needsResume = includeCoverLetter || includeScore;

  function resetPromptToDefault() {
    setPrompt(settings.defaultCoverLetterPrompt);
    setPromptTouched(false);
  }

  async function submit(e) {
    e.preventDefault();
    if (!content.trim()) {
      showToast("Paste a job posting first", "error");
      return;
    }
    if (needsResume && !resumeId) {
      showToast("Select a resume to base the cover letter / score on", "error");
      return;
    }
    setSubmitting(true);
    try {
      const posting = await api.parseJobPosting({
        link: link || "",
        content,
        resume_id: needsResume ? resumeId : null,
        include_cover_letter: includeCoverLetter,
        include_score: includeScore,
        cover_letter_prompt: includeCoverLetter ? prompt : null,
      });
      showToast("Job posting parsed");
      setContent("");
      setLink("");
      setIncludeCoverLetter(false);
      setIncludeScore(false);
      setPromptTouched(false);
      onCreated?.(posting);
      navigate(`/job-postings/${posting.id}`);
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "Failed to parse job posting";
      showToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="card">
      <div className="card__header">
        <div>
          <span className="card__eyebrow">Step one</span>
          <h2>Submit a job posting</h2>
        </div>
      </div>
      <form className="card__body" onSubmit={submit}>
        <div className="field">
          <label>Job posting text</label>
          <textarea
            className="content-textarea"
            rows={10}
            placeholder="Paste the full job posting here…"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
        </div>

        <div className="field">
          <label>Link (optional)</label>
          <input type="url" placeholder="https://…" value={link} onChange={(e) => setLink(e.target.value)} />
        </div>

        <div className="field">
          <label>Parse options</label>
          <div className="checkbox-line">
            <input type="checkbox" checked disabled readOnly />
            Parse the posting into structured fields
          </div>
          <div className="checkbox-line">
            <input
              type="checkbox"
              checked={includeCoverLetter}
              onChange={(e) => setIncludeCoverLetter(e.target.checked)}
            />
            Also generate a cover letter
          </div>
          <div className="checkbox-line">
            <input type="checkbox" checked={includeScore} onChange={(e) => setIncludeScore(e.target.checked)} />
            Also generate a match score
          </div>
        </div>

        {needsResume && (
          <>
            <ResumeSelect value={resumeId} onChange={setResumeId} />

            {includeCoverLetter && (
              <div className="field">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                  <label style={{ marginBottom: 0 }}>Cover letter prompt</label>
                  {promptTouched && (
                    <button type="button" className="icon-btn" onClick={resetPromptToDefault}>
                      Reset to default
                    </button>
                  )}
                </div>
                <textarea
                  rows={4}
                  value={prompt}
                  onChange={(e) => {
                    setPrompt(e.target.value);
                    setPromptTouched(true);
                  }}
                />
                <span className="hint">
                  Pulled from your default prompt in Settings — edit it here just for this posting.
                </span>
              </div>
            )}
          </>
        )}

        <button className="btn btn--accent btn--block" disabled={submitting} type="submit">
          {submitting && <span className="spinner" />}
          {submitting ? "Parsing…" : "Parse job posting"}
        </button>
        <p className="hint" style={{ marginTop: 8 }}>
          Parsing (and cover letter / score generation) call an LLM and are limited to 3 requests per minute.
        </p>
      </form>
    </div>
  );
}
