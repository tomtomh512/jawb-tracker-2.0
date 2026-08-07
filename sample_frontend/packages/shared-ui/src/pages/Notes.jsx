import { useEffect, useState } from "react";
import { useApi } from "../api/useApi";
import { useToast } from "../context/ToastContext";
import Modal from "../components/Modal";
import Pagination from "../components/Pagination";

const LIMIT = 12;

function NoteForm({ initial, onSubmit, onCancel }) {
  const [title, setTitle] = useState(initial?.title || "");
  const [content, setContent] = useState(initial?.content || "");
  const [clipboard, setClipboard] = useState(initial?.copy_to_clipboard || false);
  const [submitting, setSubmitting] = useState(false);

  async function submit(e) {
    e.preventDefault();
    if (!content.trim()) return;
    setSubmitting(true);
    try {
      await onSubmit({ title: title || null, content, copy_to_clipboard: clipboard });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={submit}>
      <div className="field">
        <label>Title</label>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g. LinkedIn summary" />
      </div>
      <div className="field">
        <label>Content</label>
        <textarea rows={8} value={content} onChange={(e) => setContent(e.target.value)} />
      </div>
      <div className="checkbox-line" style={{ marginBottom: 14 }}>
        <input type="checkbox" checked={clipboard} onChange={(e) => setClipboard(e.target.checked)} />
        Show as a clipboard button on the home page
      </div>
      <div className="btn-row" style={{ justifyContent: "flex-end" }}>
        <button type="button" className="btn btn--ghost" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn btn--accent" disabled={submitting}>
          {submitting ? "Saving…" : "Save note"}
        </button>
      </div>
    </form>
  );
}

export default function Notes() {
  const api = useApi();
  const { showToast } = useToast();
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [skip, setSkip] = useState(0);
  const [modal, setModal] = useState(null); // { mode: 'create' | 'edit', note }

  function load() {
    setLoading(true);
    api
      .listNotes({ skip, limit: LIMIT })
      .then(setNotes)
      .catch((err) => showToast(err.message, "error"))
      .finally(() => setLoading(false));
  }

  useEffect(load, [skip]);

  async function handleCreate(payload) {
    try {
      await api.createNote(payload);
      showToast("Note added");
      setModal(null);
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleUpdate(id, payload) {
    try {
      await api.updateNote(id, payload);
      showToast("Note updated");
      setModal(null);
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this note?")) return;
    try {
      await api.deleteNote(id);
      showToast("Note deleted");
      load();
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  return (
    <div className="page">
      <div className="card">
        <div className="card__header">
          <div>
            <span className="card__eyebrow">Reference</span>
            <h2>Notes</h2>
          </div>
          <button className="btn btn--accent btn--sm" onClick={() => setModal({ mode: "create" })}>
            + New note
          </button>
        </div>
        <div className="card__body">
          {loading ? (
            <div className="loading-line">Loading notes…</div>
          ) : notes.length === 0 ? (
            <div className="empty-state">
              <h3>No notes yet</h3>
              <p>Save reusable snippets — like a summary blurb or portfolio link — and pin the ones you copy often to the home page.</p>
            </div>
          ) : (
            <div className="note-card-grid">
              {notes.map((n) => (
                <div className="note-card" key={n.id}>
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                    <span className="note-card__title">{n.title || "Untitled note"}</span>
                    {n.copy_to_clipboard && <span className="main-badge">clipboard</span>}
                  </div>
                  <div className="note-card__content">{n.content}</div>
                  <div className="btn-row">
                    <button
                      className="icon-btn"
                      onClick={() => {
                        navigator.clipboard.writeText(n.content);
                        showToast("Copied to clipboard");
                      }}
                    >
                      Copy
                    </button>
                    <button className="icon-btn" onClick={() => setModal({ mode: "edit", note: n })}>
                      Edit
                    </button>
                    <button className="icon-btn" onClick={() => handleDelete(n.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        {!loading && notes.length > 0 && <Pagination skip={skip} limit={LIMIT} count={notes.length} onPage={setSkip} />}
      </div>

      {modal && (
        <Modal title={modal.mode === "create" ? "New note" : "Edit note"} onClose={() => setModal(null)}>
          <NoteForm
            initial={modal.note}
            onCancel={() => setModal(null)}
            onSubmit={(payload) => (modal.mode === "create" ? handleCreate(payload) : handleUpdate(modal.note.id, payload))}
          />
        </Modal>
      )}
    </div>
  );
}
