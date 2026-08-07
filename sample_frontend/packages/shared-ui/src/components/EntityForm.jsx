import { useState } from "react";
import { TagListEditor, LineListEditor } from "./ListEditor";

/**
 * fields: [{ name, label, type: 'text'|'textarea'|'date'|'number'|'boolean'|'list'|'lines', placeholder? }]
 */
export default function EntityForm({ fields, initial, onSubmit, onCancel, submitLabel = "Save" }) {
  const blank = Object.fromEntries(
    fields.map((f) => [f.name, f.type === "list" || f.type === "lines" ? [] : f.type === "boolean" ? false : ""])
  );
  const [form, setForm] = useState({ ...blank, ...(initial || {}) });
  const [submitting, setSubmitting] = useState(false);

  function set(name, value) {
    setForm((f) => ({ ...f, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = { ...form };
      fields.forEach((f) => {
        if (f.type === "number") payload[f.name] = payload[f.name] === "" ? null : Number(payload[f.name]);
        if (f.type === "date" && payload[f.name] === "") payload[f.name] = null;
        if ((f.type === "text" || f.type === "textarea") && payload[f.name] === "") payload[f.name] = null;
      });
      await onSubmit(payload);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {fields.map((f) => {
        if (f.type === "list") {
          return <TagListEditor key={f.name} label={f.label} values={form[f.name]} onChange={(v) => set(f.name, v)} />;
        }
        if (f.type === "lines") {
          return (
            <LineListEditor
              key={f.name}
              label={f.label}
              values={form[f.name]}
              onChange={(v) => set(f.name, v)}
              placeholder={f.placeholder}
            />
          );
        }
        if (f.type === "boolean") {
          return (
            <div className="checkbox-line" key={f.name} style={{ marginBottom: 14 }}>
              <input type="checkbox" checked={!!form[f.name]} onChange={(e) => set(f.name, e.target.checked)} />
              {f.label}
            </div>
          );
        }
        if (f.type === "textarea") {
          return (
            <div className="field" key={f.name}>
              <label>{f.label}</label>
              <textarea rows={4} value={form[f.name] || ""} onChange={(e) => set(f.name, e.target.value)} />
            </div>
          );
        }
        return (
          <div className="field" key={f.name}>
            <label>{f.label}</label>
            <input
              type={f.type === "number" ? "number" : f.type === "date" ? "date" : "text"}
              value={form[f.name] ?? ""}
              placeholder={f.placeholder}
              step={f.type === "number" ? "any" : undefined}
              onChange={(e) => set(f.name, e.target.value)}
            />
          </div>
        );
      })}
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
