import { useEffect, useState } from "react";

/**
 * Inline click-to-edit text block. Shows the current value with a small
 * "Edit" affordance; clicking it swaps in a textarea with Save/Cancel.
 * Errors from onSave (e.g. backend validation) are surfaced right next to
 * the field instead of only in a toast, so the person can fix and retry
 * without losing what they typed.
 */
export default function InlineEditable({
  value,
  onSave,
  rows = 4,
  placeholder = "",
  emptyText = "Nothing here yet.",
  allowEmpty = true,
  requiredMessage = "This can't be empty.",
  textClassName = "bullet-block",
}) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(value || "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Keep the draft in sync if the underlying value changes elsewhere
  // (e.g. a regenerate action) while we're not actively editing it.
  useEffect(() => {
    if (!editing) setDraft(value || "");
  }, [value, editing]);

  function startEdit() {
    setDraft(value || "");
    setError("");
    setEditing(true);
  }

  function cancel() {
    setDraft(value || "");
    setError("");
    setEditing(false);
  }

  async function save() {
    if (!allowEmpty && !draft.trim()) {
      setError(requiredMessage);
      return;
    }
    setError("");
    setSaving(true);
    try {
      await onSave(draft);
      setEditing(false);
    } catch (err) {
      setError(err?.message || "Could not save changes.");
    } finally {
      setSaving(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Escape") {
      e.preventDefault();
      cancel();
    } else if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      save();
    }
  }

  if (!editing) {
    return (
      <div className="inline-editable">
        {value ? (
          <div className={textClassName}>{value}</div>
        ) : (
          <div className="hint">{emptyText}</div>
        )}
        <button type="button" className="btn btn--ghost btn--sm inline-editable__edit-btn" onClick={startEdit}>
          Edit
        </button>
      </div>
    );
  }

  return (
    <div className="inline-editable inline-editable--editing">
      <textarea
        rows={rows}
        value={draft}
        placeholder={placeholder}
        autoFocus
        disabled={saving}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      {error && <div className="inline-editable__error">{error}</div>}
      <div className="btn-row" style={{ marginTop: 8 }}>
        <button type="button" className="btn btn--ghost btn--sm" onClick={cancel} disabled={saving}>
          Cancel
        </button>
        <button type="button" className="btn btn--accent btn--sm" onClick={save} disabled={saving}>
          {saving ? "Saving…" : "Save"}
        </button>
      </div>
    </div>
  );
}
