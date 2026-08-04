import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useApi } from "../api/useApi";
import { useToast } from "../context/ToastContext";
import { TagListEditor } from "../components/ListEditor";
import ResumeSection from "../components/ResumeSection";
import { formatDate } from "../constants";

function BasicsForm({ resume, onSave }) {
  const [form, setForm] = useState({
    resume_name: resume.resume_name,
    name: resume.name || "",
    email: resume.email || "",
    phone: resume.phone || "",
    location: resume.location || "",
    summary: resume.summary || "",
    websites: resume.websites || [],
  });
  const [saving, setSaving] = useState(false);

  function set(k, v) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e) {
    e.preventDefault();
    setSaving(true);
    try {
      await onSave(form);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="field-row">
        <div className="field">
          <label>Resume name</label>
          <input type="text" value={form.resume_name} onChange={(e) => set("resume_name", e.target.value)} required />
        </div>
        <div className="field">
          <label>Full name</label>
          <input type="text" value={form.name} onChange={(e) => set("name", e.target.value)} />
        </div>
      </div>
      <div className="field-row">
        <div className="field">
          <label>Email</label>
          <input type="text" value={form.email} onChange={(e) => set("email", e.target.value)} />
        </div>
        <div className="field">
          <label>Phone</label>
          <input type="text" value={form.phone} onChange={(e) => set("phone", e.target.value)} />
        </div>
        <div className="field">
          <label>Location</label>
          <input type="text" value={form.location} onChange={(e) => set("location", e.target.value)} />
        </div>
      </div>
      <div className="field">
        <label>Summary</label>
        <textarea rows={3} value={form.summary} onChange={(e) => set("summary", e.target.value)} />
      </div>
      <TagListEditor label="Websites / links" values={form.websites} onChange={(v) => set("websites", v)} placeholder="https://…" />
      <div className="btn-row" style={{ justifyContent: "flex-end" }}>
        <button className="btn btn--accent" type="submit" disabled={saving}>
          {saving ? "Saving…" : "Save basics"}
        </button>
      </div>
    </form>
  );
}

export default function ResumeDetail() {
  const { id } = useParams();
  const api = useApi();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);

  function load() {
    setLoading(true);
    api
      .getResume(id)
      .then(setResume)
      .catch((err) => showToast(err.message, "error"))
      .finally(() => setLoading(false));
  }

  useEffect(load, [id]);

  async function saveBasics(payload) {
    try {
      const updated = await api.updateResume(id, payload);
      setResume((r) => ({ ...r, ...updated }));
      showToast("Resume updated");
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function setMain() {
    try {
      await api.setMainResume(id);
      setResume((r) => ({ ...r, is_main: true }));
      showToast("Set as main resume");
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function remove() {
    if (!confirm("Delete this resume? This cannot be undone.")) return;
    try {
      await api.deleteResume(id);
      showToast("Resume deleted");
      navigate("/resumes");
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  if (loading) return <div className="page loading-line">Loading resume…</div>;
  if (!resume) return <div className="page empty-state">Resume not found. <Link to="/resumes">Back to resumes</Link></div>;

  return (
    <div className="page page--narrow">
      <div style={{ marginBottom: 14 }}>
        <Link to="/resumes" className="hint">← Back to resumes</Link>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 10, marginBottom: 16 }}>
        <div>
          <span className="card__eyebrow">Resume</span>
          <h1 className="mt-0">
            {resume.resume_name} {resume.is_main && <span className="main-badge">main</span>}
          </h1>
          <span className="hint">Updated {formatDate(resume.updated_at)}</span>
        </div>
        <div className="btn-row">
          {!resume.is_main && (
            <button className="btn btn--ghost" onClick={setMain}>
              Set as main
            </button>
          )}
          <button className="btn btn--danger" onClick={remove}>
            Delete
          </button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 18 }}>
        <div className="card__header">
          <h3>Basics</h3>
        </div>
        <div className="card__body">
          <BasicsForm resume={resume} onSave={saveBasics} />
        </div>
      </div>

      <ResumeSection
        resumeId={id}
        kind="experiences"
        title="Experience"
        items={resume.experiences}
        onChange={(v) => setResume((r) => ({ ...r, experiences: v }))}
        fields={[
          { name: "title", label: "Title", type: "text" },
          { name: "organization", label: "Organization", type: "text" },
          { name: "location", label: "Location", type: "text" },
          { name: "start_date", label: "Start date", type: "date" },
          { name: "end_date", label: "End date", type: "date" },
          { name: "current_job", label: "This is my current job", type: "boolean" },
          { name: "bullet_points", label: "Bullet points", type: "lines", placeholder: "Led a team of…" },
        ]}
        renderSummary={(e) => (
          <>
            <strong>{e.title}</strong> {e.organization && <span>· {e.organization}</span>}
            <div className="hint">
              {e.start_date || "?"} – {e.current_job ? "present" : e.end_date || "?"} {e.location && `· ${e.location}`}
            </div>
            {e.bullet_points?.length > 0 && (
              <ul style={{ margin: "6px 0 0", paddingLeft: 18 }}>
                {e.bullet_points.map((b, i) => <li key={i}>{b}</li>)}
              </ul>
            )}
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="educations"
        title="Education"
        items={resume.educations}
        onChange={(v) => setResume((r) => ({ ...r, educations: v }))}
        fields={[
          { name: "school", label: "School", type: "text" },
          { name: "degree", label: "Degree", type: "text" },
          { name: "field_of_study", label: "Field of study", type: "text" },
          { name: "gpa", label: "GPA", type: "number" },
          { name: "start_date", label: "Start date", type: "date" },
          { name: "end_date", label: "End date", type: "date" },
          { name: "honors", label: "Honors", type: "list" },
          { name: "coursework", label: "Coursework", type: "list" },
        ]}
        renderSummary={(e) => (
          <>
            <strong>{e.school}</strong>
            <div className="hint">
              {e.degree} {e.field_of_study && `in ${e.field_of_study}`} {e.gpa != null && `· GPA ${e.gpa}`}
            </div>
            <div className="hint">
              {e.start_date || "?"} – {e.end_date || "?"}
            </div>
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="projects"
        title="Projects"
        items={resume.projects}
        onChange={(v) => setResume((r) => ({ ...r, projects: v }))}
        fields={[
          { name: "name", label: "Name", type: "text" },
          { name: "description", label: "Description", type: "textarea" },
          { name: "skills", label: "Skills", type: "list" },
          { name: "links", label: "Links", type: "list" },
          { name: "bullet_points", label: "Bullet points", type: "lines" },
        ]}
        renderSummary={(p) => (
          <>
            <strong>{p.name}</strong>
            {p.description && <div className="hint">{p.description}</div>}
            {p.skills?.length > 0 && <div className="tag-list" style={{ marginTop: 6 }}>{p.skills.map((t, i) => <span className="tag" key={i}>{t}</span>)}</div>}
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="skillCategories"
        title="Skills"
        items={resume.skill_categories}
        onChange={(v) => setResume((r) => ({ ...r, skill_categories: v }))}
        fields={[
          { name: "category", label: "Category", type: "text", placeholder: "Languages, Frameworks…" },
          { name: "skills", label: "Skills", type: "list" },
        ]}
        renderSummary={(s) => (
          <>
            <strong>{s.category}</strong>
            {s.skills?.length > 0 && <div className="tag-list" style={{ marginTop: 6 }}>{s.skills.map((sk, i) => <span className="tag" key={i}>{sk}</span>)}</div>}
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="certifications"
        title="Certifications"
        items={resume.certifications}
        onChange={(v) => setResume((r) => ({ ...r, certifications: v }))}
        fields={[
          { name: "name", label: "Name", type: "text" },
          { name: "issuer", label: "Issuer", type: "text" },
          { name: "issue_date", label: "Issue date", type: "date" },
          { name: "expiration_date", label: "Expiration date", type: "date" },
          { name: "credential_id", label: "Credential ID", type: "text" },
          { name: "url", label: "URL", type: "text" },
        ]}
        renderSummary={(c) => (
          <>
            <strong>{c.name}</strong> {c.issuer && <span>· {c.issuer}</span>}
            <div className="hint">{c.issue_date || "?"} {c.expiration_date && `→ ${c.expiration_date}`}</div>
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="publications"
        title="Publications"
        items={resume.publications}
        onChange={(v) => setResume((r) => ({ ...r, publications: v }))}
        fields={[
          { name: "title", label: "Title", type: "text" },
          { name: "venue", label: "Venue", type: "text" },
          { name: "publisher", label: "Publisher", type: "text" },
          { name: "publication_date", label: "Publication date", type: "date" },
          { name: "url", label: "URL", type: "text" },
        ]}
        renderSummary={(p) => (
          <>
            <strong>{p.title}</strong>
            <div className="hint">{p.venue} {p.publication_date && `· ${p.publication_date}`}</div>
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="awards"
        title="Awards"
        items={resume.awards}
        onChange={(v) => setResume((r) => ({ ...r, awards: v }))}
        fields={[
          { name: "name", label: "Name", type: "text" },
          { name: "issuer", label: "Issuer", type: "text" },
          { name: "award_date", label: "Date", type: "date" },
          { name: "description", label: "Description", type: "textarea" },
        ]}
        renderSummary={(a) => (
          <>
            <strong>{a.name}</strong> {a.issuer && <span>· {a.issuer}</span>}
            <div className="hint">{a.award_date}</div>
          </>
        )}
      />

      <ResumeSection
        resumeId={id}
        kind="customSections"
        title="Custom sections"
        items={resume.custom_sections}
        onChange={(v) => setResume((r) => ({ ...r, custom_sections: v }))}
        fields={[
          { name: "title", label: "Section title", type: "text" },
          { name: "entries", label: "Entries", type: "list" },
        ]}
        renderSummary={(c) => (
          <>
            <strong>{c.title}</strong>
            {c.entries?.length > 0 && (
              <ul style={{ margin: "6px 0 0", paddingLeft: 18 }}>{c.entries.map((e, i) => <li key={i}>{e}</li>)}</ul>
            )}
          </>
        )}
      />
    </div>
  );
}
