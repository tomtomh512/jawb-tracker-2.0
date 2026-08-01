// Shared tiny API client + settings helper for the Jawb Tracker extension.

const SETTINGS_KEY = "jawb_ext_settings_v1";

const DEFAULT_SETTINGS = {
  apiBaseUrl: "http://localhost:8000/api/v1",
  webAppUrl: "http://localhost:5173",
};

async function getSettings() {
  const stored = await chrome.storage.sync.get(SETTINGS_KEY);
  return { ...DEFAULT_SETTINGS, ...(stored[SETTINGS_KEY] || {}) };
}

async function setSettings(patch) {
  const current = await getSettings();
  const next = { ...current, ...patch };
  await chrome.storage.sync.set({ [SETTINGS_KEY]: next });
  return next;
}

class ApiError extends Error {
  constructor(message, status, detail) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

async function request(baseUrl, path, options = {}) {
  const url = `${baseUrl.replace(/\/+$/, "")}${path}`;
  let res;
  try {
    res = await fetch(url, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });
  } catch (err) {
    throw new ApiError(
      `Could not reach the API at ${baseUrl}. Check the backend URL in the extension options and make sure the server is running.`,
      0,
      null
    );
  }

  if (res.status === 204) return null;

  let body = null;
  const text = await res.text();
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = text;
    }
  }

  if (!res.ok) {
    let detail = body?.detail;
    if (Array.isArray(detail)) {
      detail = detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
    }
    if (res.status === 429) {
      detail = detail || "Rate limit reached (3 per minute). Please wait a moment and try again.";
    }
    throw new ApiError(detail || `Request failed (${res.status})`, res.status, body);
  }

  return body;
}

async function makeApi() {
  const { apiBaseUrl } = await getSettings();
  const get = (path) => request(apiBaseUrl, path);
  const post = (path, data) => request(apiBaseUrl, path, { method: "POST", body: JSON.stringify(data ?? {}) });

  const qs = (params) => {
    const usp = new URLSearchParams();
    Object.entries(params || {}).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") usp.set(k, v);
    });
    const s = usp.toString();
    return s ? `?${s}` : "";
  };

  return {
    listJobPostings: (params) => get(`/job-postings/${qs(params)}`),
    parseJobPosting: (data) => post(`/job-postings/parse`, data),
    getMainResume: () => get(`/resumes/main`),
    listClipboardNotes: () => get(`/notes/clipboard`),
  };
}
