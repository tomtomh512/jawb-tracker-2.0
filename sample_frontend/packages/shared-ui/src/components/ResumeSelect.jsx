import { useEffect, useState } from "react";
import { useApi } from "../api/useApi";

export const CUSTOM_RESUME_VALUE = "__custom__";

export default function ResumeSelect({
  value,
  onChange,
  label = "Resume",
  allowCustom = false,
  customValue = "",
  onCustomChange,
}) {
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

  const isCustom = allowCustom && value === CUSTOM_RESUME_VALUE;

  return (
    <>
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
          {allowCustom && <option value={CUSTOM_RESUME_VALUE}>Other</option>}
        </select>
      </div>

      {isCustom && (
        <div className="field">
          <label>Tailored resume</label>
          <textarea
            rows={8}
            className="content-textarea"
            placeholder="Paste the resume you tailored for this specific job posting…"
            value={customValue}
            onChange={(e) => onCustomChange?.(e.target.value)}
          />
        </div>
      )}
    </>
  );
}