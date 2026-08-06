import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useApi } from "../api/useApi";
import { useToast } from "../context/ToastContext";
import Modal from "../components/Modal";
import { formatDate } from "../constants";

const MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024;
const ACCEPTED_UPLOAD_TYPES = ["application/pdf", "image/jpeg", "image/png"];

function CreateResumeForm({ onCreatedManual, onParsed, onCancel }) {
  const api = useApi();
  const { showToast } = useToast();
  const [mode, setMode] = useState("manual");
  const [name, setName] = useState("");
  const [pasteText, setPasteText] = useState("");
  const [uploadFile, setUploadFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function submit(e) {
    e.preventDefault();
    if (!name.trim()) return showToast("Give the resume a name", "error");
    setSubmitting(true);
    try {
      if (mode === "manual") {
        const created = await api.createResume({ resume_name: name });
        onCreatedManual(created);
      } else if (mode === "paste") {
        if (!pasteText.trim()) return showToast("Paste resume text to parse", "error");
        const created = await api.parseResume({ resume_name: name, content: pasteText });
        onParsed(created);
      } else if (mode === "upload") {
        if (!uploadFile) return showToast("Choose a file to upload", "error");
        if (!ACCEPTED_UPLOAD_TYPES.includes(uploadFile.type)) {
          return showToast("File must be a PDF, JPG, or PNG", "error");
        }
        if (uploadFile.size > MAX_UPLOAD_SIZE_BYTES) {
          return showToast("File must be under 10MB", "error");
        }
        const created = await api.parseResumeUpload(name, uploadFile);
        onParsed(created);
      }
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="field">
        <label>Resume name</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Software Engineer — General" />
      </div>

      <div className="field">
        <label>Creation method</label>
        <div className="checkbox-line">
          <input type="radio" name="mode" checked={mode === "manual"} onChange={() => setMode("manual")} /> Start blank, build sections manually
        </div>
        <div className="checkbox-line">
          <input type="radio" name="mode" checked={mode === "paste"} onChange={() => setMode("paste")} /> Paste resume text and let AI parse it
        </div>
        <div className="checkbox-line">
          <input type="radio" name="mode" checked={mode === "upload"} onChange={() => setMode("upload")} /> Upload a PDF or image and let AI parse it
        </div>
      </div>

      {mode === "paste" && (
        <div className="field">
          <label>Resume text</label>
          <textarea className="content-textarea" rows={10} value={pasteText} onChange={(e) => setPasteText(e.target.value)} placeholder="Paste your resume content here…" />
        </div>
      )}

      {mode === "upload" && (
        <div className="field">
          <label>Resume file</label>
          <input
            type="file"
            accept="application/pdf,image/jpeg,image/png"
            onChange={(e) => setUploadFile(e.target.files[0] ?? null)}
          />
          {uploadFile && <span className="hint">{uploadFile.name}</span>}
        </div>
      )}

      <div className="btn-row" style={{ justifyContent: "flex-end" }}>
        <button type="button" className="btn btn--ghost" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn btn--accent" disabled={submitting}>
          {submitting ? "Creating…" : "Create resume"}
        </button>
      </div>
    </form>
  );
}

export default function Resumes() {
  const api = useApi();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);

  function load() {
    setLoading(true);
    api
      .listResumes({ limit: 50 })
      .then(setResumes)
      .catch((err) => showToast(err.message, "error"))
      .finally(() => setLoading(false));
  }

  useEffect(load, []);

  async function setMain(id) {
    try {
      await api.setMainResume(id);
      showToast("Main resume updated");
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function remove(id) {
    if (!confirm("Delete this resume? This also removes any scores based on it.")) return;
    try {
      await api.deleteResume(id);
      showToast("Resume deleted");
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  return (
    <div className="page page--narrow">
      <div className="card">
        <div className="card__header">
          <div>
            <span className="card__eyebrow">Library</span>
            <h2>Resumes</h2>
          </div>
          <button className="btn btn--accent btn--sm" onClick={() => setShowCreate(true)}>
            + New resume
          </button>
        </div>
        <div className="card__body">
          {loading ? (
            <div className="loading-line">Loading resumes…</div>
          ) : resumes.length === 0 ? (
            <div className="empty-state">
              <h3>No resumes yet</h3>
              <p>Add your main resume so it's ready to base cover letters and scores on.</p>
            </div>
          ) : (
            <div className="resume-card-list">
              {resumes.map((r) => (
                <div className="resume-card" key={r.id}>
                  <div>
                    <Link to={`/resumes/${r.id}`} style={{ fontWeight: 600, textDecoration: "none", color: "var(--text)" }}>
                      {r.resume_name}
                    </Link>{" "}
                    {r.is_main && <span className="main-badge">main</span>}
                    <div className="hint">Updated {formatDate(r.updated_at)}</div>
                  </div>
                  <div className="btn-row">
                    {!r.is_main && (
                      <button className="icon-btn" onClick={() => setMain(r.id)}>
                        Set as main
                      </button>
                    )}
                    <button className="icon-btn" onClick={() => navigate(`/resumes/${r.id}`)}>
                      Edit
                    </button>
                    <button className="icon-btn" onClick={() => remove(r.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {showCreate && (
        <Modal title="New resume" onClose={() => setShowCreate(false)}>
          <CreateResumeForm
            onCancel={() => setShowCreate(false)}
            onCreatedManual={(r) => {
              setShowCreate(false);
              navigate(`/resumes/${r.id}`);
            }}
            onParsed={(r) => {
              setShowCreate(false);
              showToast("Resume parsed");
              navigate(`/resumes/${r.id}`);
            }}
          />
        </Modal>
      )}
    </div>
  );
}