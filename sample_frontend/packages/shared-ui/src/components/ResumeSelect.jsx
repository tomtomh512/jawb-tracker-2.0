import { useEffect, useState } from "react";
import { useApi } from "../api/useApi";

export default function ResumeSelect({ value, onChange, label = "Resume" }) {
  const api = useApi();
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      try {
        const list = await api.listResumes({ limit: 50 });
        if (cancelled) return;
        setResumes(list);
        if (!value) {
          const main = list.find((r) => r.is_main) || list[0];
          if (main) onChange(main.id);
        }
      } catch {
        // ignore — surfaced elsewhere
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="field">
      <label>{label}</label>
      <select value={value || ""} onChange={(e) => onChange(e.target.value)} disabled={loading}>
        {resumes.length === 0 && <option value="">{loading ? "Loading…" : "No resumes yet"}</option>}
        {resumes.map((r) => (
          <option key={r.id} value={r.id}>
            {r.resume_name}
            {r.is_main ? " (main)" : ""}
          </option>
        ))}
      </select>
    </div>
  );
}
