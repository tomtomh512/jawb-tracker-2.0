import { useState } from "react";

/** Editable list of plain strings, rendered as tags with an "add" input. */
export function TagListEditor({ label, values, onChange, placeholder }) {
  const [draft, setDraft] = useState("");

  function add() {
    const v = draft.trim();
    if (!v) return;
    onChange([...(values || []), v]);
    setDraft("");
  }

  function remove(idx) {
    onChange(values.filter((_, i) => i !== idx));
  }

  return (
    <div className="field">
      {label && <label>{label}</label>}
      <div className="tag-list" style={{ marginBottom: values?.length ? 8 : 0 }}>
        {(values || []).map((v, i) => (
          <span className="tag" key={i}>
            {v}
            <button type="button" onClick={() => remove(i)} aria-label="Remove">
              ×
            </button>
          </span>
        ))}
      </div>
      <div style={{ display: "flex", gap: 6 }}>
        <input
          type="text"
          value={draft}
          placeholder={placeholder || "Add and press Enter"}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              add();
            }
          }}
        />
        <button type="button" className="btn btn--ghost btn--sm" onClick={add}>
          Add
        </button>
      </div>
    </div>
  );
}

/** Editable list of multi-line strings (e.g. bullet points), one per row. */
export function LineListEditor({ label, values, onChange, placeholder }) {
  const list = values || [];

  function update(idx, val) {
    const next = [...list];
    next[idx] = val;
    onChange(next);
  }

  function remove(idx) {
    onChange(list.filter((_, i) => i !== idx));
  }

  function add() {
    onChange([...list, ""]);
  }

  return (
    <div className="field">
      {label && <label>{label}</label>}
      {list.map((v, i) => (
        <div className="list-editor__row" key={i}>
          <input
            type="text"
            value={v}
            placeholder={placeholder}
            onChange={(e) => update(i, e.target.value)}
          />
          <button type="button" className="icon-btn" onClick={() => remove(i)}>
            Remove
          </button>
        </div>
      ))}
      <button type="button" className="btn btn--ghost btn--sm" onClick={add}>
        + Add line
      </button>
    </div>
  );
}
