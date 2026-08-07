import { useState } from "react";
import { useApi } from "../api/useApi";
import { useToast } from "../context/ToastContext";
import Modal from "./Modal";
import EntityForm from "./EntityForm";

export default function ResumeSection({ resumeId, kind, title, fields, items, onChange, renderSummary }) {
  const api = useApi();
  const { showToast } = useToast();
  const [modal, setModal] = useState(null); // { mode, item }
  const sub = api.subresource(kind);

  async function handleCreate(payload) {
    try {
      const created = await sub.create(resumeId, payload);
      onChange([...(items || []), created]);
      setModal(null);
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleUpdate(id, payload) {
    try {
      const updated = await sub.update(resumeId, id, payload);
      onChange(items.map((it) => (it.id === id ? updated : it)));
      setModal(null);
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleDelete(id) {
    if (!confirm(`Remove this ${title.toLowerCase().replace(/s$/, "")} entry?`)) return;
    try {
      await sub.remove(resumeId, id);
      onChange(items.filter((it) => it.id !== id));
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  return (
    <div className="section-block">
      <div className="section-block__head">
        <strong>{title}</strong>
        <button className="btn btn--ghost btn--sm" onClick={() => setModal({ mode: "create" })}>
          + Add
        </button>
      </div>
      <div className="section-block__body">
        {(!items || items.length === 0) && <p className="hint mt-0">Nothing added yet.</p>}
        {items?.map((item) => (
          <div className="entry-card" key={item.id}>
            <div className="entry-card__actions">
              <button className="icon-btn" onClick={() => setModal({ mode: "edit", item })}>
                Edit
              </button>
              <button className="icon-btn" onClick={() => handleDelete(item.id)}>
                Delete
              </button>
            </div>
            {renderSummary(item)}
          </div>
        ))}
      </div>

      {modal && (
        <Modal title={modal.mode === "create" ? `Add ${title.toLowerCase().replace(/s$/, "")}` : `Edit entry`} onClose={() => setModal(null)}>
          <EntityForm
            fields={fields}
            initial={modal.item}
            onCancel={() => setModal(null)}
            onSubmit={(payload) => (modal.mode === "create" ? handleCreate(payload) : handleUpdate(modal.item.id, payload))}
          />
        </Modal>
      )}
    </div>
  );
}
