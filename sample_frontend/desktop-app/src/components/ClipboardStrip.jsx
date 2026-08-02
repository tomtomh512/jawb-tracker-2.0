import { useEffect, useState } from "react";
import { useApi } from "../api/useApi";
import { useToast } from "../context/ToastContext";

export default function ClipboardStrip() {
  const api = useApi();
  const { showToast } = useToast();
  const [notes, setNotes] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    let cancelled = false;
    api
      .listClipboardNotes()
      .then((list) => !cancelled && setNotes(list))
      .catch(() => !cancelled && setError(true));
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function copy(note) {
    try {
      await navigator.clipboard.writeText(note.content);
      showToast(`Copied "${note.title || "note"}" to clipboard`);
    } catch {
      showToast("Couldn't access clipboard — copy blocked by browser", "error");
    }
  }

  if (error || notes.length === 0) return null;

  return (
    <div className="clipboard-strip">
      <div className="clipboard-strip__title">Clipboard notes</div>
      <div className="clip-list">
        {notes.map((n) => (
          <button key={n.id} className="clip-btn" onClick={() => copy(n)} title={n.content}>
            <span className="clip-btn__glyph">⎘</span>
            {n.title || "Untitled note"}
          </button>
        ))}
      </div>
    </div>
  );
}
