import { useState } from "react";
import { useSettings } from "../context/SettingsContext";
import { useToast } from "../context/ToastContext";
import { useApi } from "../api/useApi";

export default function Settings() {
  const { settings, updateSettings, resetSettings } = useSettings();
  const { showToast } = useToast();
  const api = useApi();

  const [apiBaseUrl, setApiBaseUrl] = useState(settings.apiBaseUrl);
  const [prompt, setPrompt] = useState(settings.defaultCoverLetterPrompt);
  const [testing, setTesting] = useState(false);

  function save(e) {
    e.preventDefault();
    updateSettings({ apiBaseUrl: apiBaseUrl.trim().replace(/\/+$/, ""), defaultCoverLetterPrompt: prompt });
    showToast("Settings saved");
  }

  async function testConnection() {
    setTesting(true);
    try {
      await api.listJobPostings({ limit: 1 });
      showToast("Connected to the API successfully");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setTesting(false);
    }
  }

  return (
    <div className="page page--narrow">
      <div className="card">
        <div className="card__header">
          <div>
            <span className="card__eyebrow">Configuration</span>
            <h2>Settings</h2>
          </div>
        </div>
        <form className="card__body settings-form" onSubmit={save}>
          <div className="field">
            <label>Backend API URL</label>
            <input type="text" value={apiBaseUrl} onChange={(e) => setApiBaseUrl(e.target.value)} placeholder="http://localhost:8000/api/v1" />
            <span className="hint">Where the Jawb Tracker FastAPI backend is running, including the /api/v1 prefix.</span>
          </div>

          <div className="field">
            <label>Default cover letter prompt</label>
            <textarea rows={6} value={prompt} onChange={(e) => setPrompt(e.target.value)} />
            <span className="hint">
              This is pulled in automatically whenever you request a cover letter — from the parse panel or a job posting's page —
              but you can always edit it for a single request.
            </span>
          </div>

          <div className="btn-row" style={{ justifyContent: "space-between" }}>
            <div className="btn-row">
              <button type="button" className="btn btn--ghost" onClick={testConnection} disabled={testing}>
                {testing ? "Testing…" : "Test connection"}
              </button>
              <button
                type="button"
                className="btn btn--ghost"
                onClick={() => {
                  resetSettings();
                  showToast("Settings reset to defaults");
                }}
              >
                Reset to defaults
              </button>
            </div>
            <button type="submit" className="btn btn--accent">
              Save settings
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
