import { createContext, useContext, useEffect, useState } from "react";

const STORAGE_KEY = "jawb_settings_v1";

const DEFAULT_PROMPT =
  "Write a concise, confident cover letter that connects my strongest, most relevant experience to what this role asks for. Keep it to three or four short paragraphs, avoid clichés, and don't restate my resume line by line.";

const DEFAULTS = {
  apiBaseUrl: "http://localhost:8000/api/v1",
  defaultCoverLetterPrompt: DEFAULT_PROMPT,
};

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULTS };
    return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {
    return { ...DEFAULTS };
  }
}

const SettingsContext = createContext(null);

export function SettingsProvider({ children }) {
  const [settings, setSettings] = useState(load);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  }, [settings]);

  function updateSettings(patch) {
    setSettings((prev) => ({ ...prev, ...patch }));
  }

  function resetSettings() {
    setSettings({ ...DEFAULTS });
  }

  return (
    <SettingsContext.Provider value={{ settings, updateSettings, resetSettings, DEFAULTS }}>
      {children}
    </SettingsContext.Provider>
  );
}

export function useSettings() {
  const ctx = useContext(SettingsContext);
  if (!ctx) throw new Error("useSettings must be used within SettingsProvider");
  return ctx;
}
