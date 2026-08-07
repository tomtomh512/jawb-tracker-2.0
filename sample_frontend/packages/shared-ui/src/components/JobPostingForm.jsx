import { useState } from "react";
import { EMPLOYMENT_TYPES, EMPLOYMENT_TYPE_LABELS, EDUCATION_LEVELS, EDUCATION_LEVEL_LABELS, JOB_STATUSES, STATUS_LABELS } from "../constants";
import { TagListEditor } from "./ListEditor";

const BLANK = {
  status: "saved",
  link: "",
  title: "",
  company: "",
  employment_type: "",
  location_raw: "",
  city: "",
  state: "",
  country: "",
  remote: null,
  remote_days_per_week: "",
  responsibilities: [],
  requirements: [],
  skills: [],
  education_minimum: "",
  education_preferred: "",
  min_salary: "",
  max_salary: "",
  currency: "",
  period: "",
  bonus: null,
  equity: null,
  visa_sponsorship: null,
  clearance_required: null,
  notes: "",
};

export default function JobPostingForm({ initial, onSubmit, onCancel, submitLabel = "Save", includeStatus = true }) {
  const [form, setForm] = useState(() => ({ ...BLANK, ...(initial || {}) }));
  const [submitting, setSubmitting] = useState(false);

  function set(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function triBool(field, label) {
    const v = form[field];
    return (
      <div className="field">
        <label>{label}</label>
        <select
          value={v === null || v === undefined ? "" : v ? "true" : "false"}
          onChange={(e) => set(field, e.target.value === "" ? null : e.target.value === "true")}
        >
          <option value="">Unspecified</option>
          <option value="true">Yes</option>
          <option value="false">No</option>
        </select>
      </div>
    );
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = { ...form };
      ["min_salary", "max_salary", "remote_days_per_week"].forEach((k) => {
        payload[k] = payload[k] === "" || payload[k] === null ? null : Number(payload[k]);
      });
      ["employment_type", "education_minimum", "education_preferred", "link", "location_raw", "city", "state", "country", "currency", "period", "notes", "title", "company"].forEach(
        (k) => {
          if (payload[k] === "") payload[k] = null;
        }
      );
      await onSubmit(payload);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {includeStatus && (
        <div className="field">
          <label>Status</label>
          <select value={form.status} onChange={(e) => set("status", e.target.value)}>
            {JOB_STATUSES.map((s) => (
              <option key={s} value={s}>
                {STATUS_LABELS[s]}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="field-row">
        <div className="field">
          <label>Title</label>
          <input type="text" value={form.title || ""} onChange={(e) => set("title", e.target.value)} />
        </div>
        <div className="field">
          <label>Company</label>
          <input type="text" value={form.company || ""} onChange={(e) => set("company", e.target.value)} />
        </div>
      </div>

      <div className="field-row">
        <div className="field">
          <label>Link</label>
          <input type="text" value={form.link || ""} onChange={(e) => set("link", e.target.value)} />
        </div>
        <div className="field">
          <label>Employment type</label>
          <select value={form.employment_type || ""} onChange={(e) => set("employment_type", e.target.value)}>
            <option value="">Unspecified</option>
            {EMPLOYMENT_TYPES.map((t) => (
              <option key={t} value={t}>
                {EMPLOYMENT_TYPE_LABELS[t]}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="field-row">
        <div className="field">
          <label>Location (raw)</label>
          <input type="text" value={form.location_raw || ""} onChange={(e) => set("location_raw", e.target.value)} />
        </div>
        <div className="field">
          <label>City</label>
          <input type="text" value={form.city || ""} onChange={(e) => set("city", e.target.value)} />
        </div>
        <div className="field">
          <label>State</label>
          <input type="text" value={form.state || ""} onChange={(e) => set("state", e.target.value)} />
        </div>
        <div className="field">
          <label>Country</label>
          <input type="text" value={form.country || ""} onChange={(e) => set("country", e.target.value)} />
        </div>
      </div>

      <div className="field-row">
        {triBool("remote", "Remote")}
        <div className="field">
          <label>Remote days / week</label>
          <input
            type="number"
            min="0"
            max="7"
            value={form.remote_days_per_week ?? ""}
            onChange={(e) => set("remote_days_per_week", e.target.value)}
          />
        </div>
      </div>

      <TagListEditor label="Responsibilities" values={form.responsibilities} onChange={(v) => set("responsibilities", v)} />
      <TagListEditor label="Requirements" values={form.requirements} onChange={(v) => set("requirements", v)} />
      <TagListEditor label="Skills" values={form.skills} onChange={(v) => set("skills", v)} />

      <div className="field-row">
        <div className="field">
          <label>Minimum education</label>
          <select value={form.education_minimum || ""} onChange={(e) => set("education_minimum", e.target.value)}>
            <option value="">Unspecified</option>
            {EDUCATION_LEVELS.map((l) => (
              <option key={l} value={l}>
                {EDUCATION_LEVEL_LABELS[l]}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Preferred education</label>
          <select value={form.education_preferred || ""} onChange={(e) => set("education_preferred", e.target.value)}>
            <option value="">Unspecified</option>
            {EDUCATION_LEVELS.map((l) => (
              <option key={l} value={l}>
                {EDUCATION_LEVEL_LABELS[l]}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="field-row">
        <div className="field">
          <label>Min salary</label>
          <input type="number" value={form.min_salary ?? ""} onChange={(e) => set("min_salary", e.target.value)} />
        </div>
        <div className="field">
          <label>Max salary</label>
          <input type="number" value={form.max_salary ?? ""} onChange={(e) => set("max_salary", e.target.value)} />
        </div>
        <div className="field">
          <label>Currency</label>
          <input type="text" placeholder="USD" value={form.currency || ""} onChange={(e) => set("currency", e.target.value)} />
        </div>
        <div className="field">
          <label>Period</label>
          <input type="text" placeholder="year / hour" value={form.period || ""} onChange={(e) => set("period", e.target.value)} />
        </div>
      </div>

      <div className="field-row">
        {triBool("bonus", "Bonus")}
        {triBool("equity", "Equity")}
        {triBool("visa_sponsorship", "Visa sponsorship")}
        {triBool("clearance_required", "Clearance required")}
      </div>

      <div className="field">
        <label>Notes</label>
        <textarea rows={3} value={form.notes || ""} onChange={(e) => set("notes", e.target.value)} />
      </div>

      <div className="btn-row" style={{ justifyContent: "flex-end", marginTop: 8 }}>
        {onCancel && (
          <button type="button" className="btn btn--ghost" onClick={onCancel}>
            Cancel
          </button>
        )}
        <button type="submit" className="btn btn--accent" disabled={submitting}>
          {submitting ? "Saving…" : submitLabel}
        </button>
      </div>
    </form>
  );
}
