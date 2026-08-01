const DEFAULT_API_BASE_URL = "http://localhost:8000/api/v1";
const TABLE_LIMIT = 8;

const state = {
  apiBaseUrl: DEFAULT_API_BASE_URL,
  mainResume: null, // { id, resume_name } or null if none found
};

// ---------------------------------------------------------------------------
// tiny API client (mirrors sample_frontend/website/src/api/client.js)
// ---------------------------------------------------------------------------

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function apiRequest(path, options = {}) {
  const url = `${state.apiBaseUrl.replace(/\/+$/, "")}${path}`;
  let res;
  try {
    res = await fetch(url, {
      headers: { "Content-Type": "application/json", ...(options.headers || {}) },
      ...options,
    });
  } catch (err) {
    throw new ApiError(
      `Could not reach the API at ${state.apiBaseUrl}. Check the backend URL in Settings and make sure the server is running.`,
      0
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
    if (Array.isArray(detail)) detail = detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
    if (res.status === 429) {
      detail = detail || "Rate limit reached (3 per minute). Please wait a moment and try again.";
    }
    throw new ApiError(detail || `Request failed (${res.status})`, res.status);
  }

  return body;
}

const api = {
  listClipboardNotes: () => apiRequest("/notes/clipboard"),
  getMainResume: () => apiRequest("/resumes/main"),
  listJobPostings: (limit) => apiRequest(`/job-postings/?limit=${limit}`),
  parseJobPosting: (data) => apiRequest("/job-postings/parse", { method: "POST", body: JSON.stringify(data) }),
};

// ---------------------------------------------------------------------------
// settings (chrome.storage.local)
// ---------------------------------------------------------------------------

function loadSettings() {
  return new Promise((resolve) => {
    chrome.storage.local.get(["apiBaseUrl"], (res) => {
      state.apiBaseUrl = res.apiBaseUrl || DEFAULT_API_BASE_URL;
      resolve();
    });
  });
}

function saveSettings(apiBaseUrl) {
  return new Promise((resolve) => {
    chrome.storage.local.set({ apiBaseUrl }, resolve);
  });
}

// ---------------------------------------------------------------------------
// toast
// ---------------------------------------------------------------------------

let toastTimer = null;
function showToast(message, type = "success") {
  const el = document.getElementById("toast");
  el.textContent = message;
  el.className = `toast${type === "error" ? " toast--error" : ""}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add("hidden"), 2600);
}

// ---------------------------------------------------------------------------
// active tab link auto-fill
// ---------------------------------------------------------------------------

function fillLinkFromActiveTab() {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs?.[0]?.url;
    const linkInput = document.getElementById("link");
    if (url && /^https?:\/\//.test(url) && !linkInput.value) {
      linkInput.value = url;
    }
  });
}

// ---------------------------------------------------------------------------
// clipboard: read the job posting text the user copied on the page
// ---------------------------------------------------------------------------

async function pasteFromClipboard({ silent = false } = {}) {
  const contentEl = document.getElementById("content");
  try {
    const text = await navigator.clipboard.readText();
    if (text && text.trim()) {
      contentEl.value = text;
      if (!silent) showToast("Pasted from clipboard");
      return true;
    }
  } catch {
    if (!silent) showToast("Couldn't read clipboard — click Paste to try again", "error");
  }
  return false;
}

// ---------------------------------------------------------------------------
// clipboard notes strip: saved notes flagged for quick clipboard copy
// ---------------------------------------------------------------------------

async function loadClipboardNotes() {
  const section = document.getElementById("clipboardSection");
  const list = document.getElementById("clipList");
  try {
    const notes = await api.listClipboardNotes();
    if (!notes || notes.length === 0) {
      section.classList.add("hidden");
      return;
    }
    list.innerHTML = "";
    notes.forEach((n) => {
      const btn = document.createElement("button");
      btn.className = "clip-btn";
      btn.title = n.content;
      btn.innerHTML = `<span class="clip-btn__glyph">⎘</span><span class="clip-btn__label"></span>`;
      btn.querySelector(".clip-btn__label").textContent = n.title || "Untitled note";
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(n.content);
          showToast(`Copied "${n.title || "note"}" to clipboard`);
        } catch {
          showToast("Couldn't access clipboard — copy blocked by browser", "error");
        }
      });
      list.appendChild(btn);
    });
    section.classList.remove("hidden");
  } catch {
    section.classList.add("hidden");
  }
}

// ---------------------------------------------------------------------------
// main resume (for scoring)
// ---------------------------------------------------------------------------

async function loadMainResume() {
  const checkbox = document.getElementById("includeScore");
  const label = document.getElementById("scoreLabel");
  try {
    const resume = await api.getMainResume();
    state.mainResume = resume;
    label.textContent = `Score against main resume (${resume.resume_name})`;
    checkbox.disabled = false;
  } catch {
    state.mainResume = null;
    label.textContent = "Score against main resume (none set)";
    checkbox.checked = false;
    checkbox.disabled = true;
  }
}

// ---------------------------------------------------------------------------
// job postings table
// ---------------------------------------------------------------------------

function scoreDialHtml(score) {
  if (score == null) return '<span class="hint">—</span>';
  const cls = score >= 70 ? "" : score >= 40 ? " score-dial--mid" : " score-dial--low";
  return `<span class="score-dial${cls}">${Math.round(score)}</span>`;
}

async function loadJobPostings() {
  const loadingEl = document.getElementById("tableLoading");
  const emptyEl = document.getElementById("tableEmpty");
  const tableEl = document.getElementById("jpTable");
  const bodyEl = document.getElementById("jpTableBody");

  loadingEl.classList.remove("hidden");
  emptyEl.classList.add("hidden");
  tableEl.classList.add("hidden");

  try {
    const postings = await api.listJobPostings(TABLE_LIMIT);
    loadingEl.classList.add("hidden");

    if (!postings || postings.length === 0) {
      emptyEl.classList.remove("hidden");
      return;
    }

    bodyEl.innerHTML = "";
    postings.forEach((jp) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="cell-title"></td>
        <td class="cell-company"></td>
        <td></td>
      `;
      tr.children[0].textContent = jp.title || "Untitled role";
      tr.children[1].textContent = jp.company || "—";
      tr.children[2].innerHTML = scoreDialHtml(jp.overall_score);
      tr.title = `${jp.title || "Untitled role"} — ${jp.company || "—"}`;
      bodyEl.appendChild(tr);
    });
    tableEl.classList.remove("hidden");
  } catch (err) {
    loadingEl.classList.add("hidden");
    emptyEl.classList.remove("hidden");
    emptyEl.querySelector("h3").textContent = "Couldn't load postings";
    emptyEl.querySelector("p").textContent =
      err instanceof ApiError ? err.message : "Check your backend connection in Settings.";
  }
}

// ---------------------------------------------------------------------------
// parse form
// ---------------------------------------------------------------------------

async function handleParseSubmit(e) {
  e.preventDefault();
  const contentEl = document.getElementById("content");
  const linkEl = document.getElementById("link");
  const includeScoreEl = document.getElementById("includeScore");
  const parseBtn = document.getElementById("parseBtn");

  const content = contentEl.value.trim();
  if (!content) {
    showToast("Paste a job posting first", "error");
    return;
  }

  const includeScore = includeScoreEl.checked;
  if (includeScore && !state.mainResume) {
    showToast("No main resume found to score against", "error");
    return;
  }

  parseBtn.disabled = true;
  const originalLabel = parseBtn.textContent;
  parseBtn.innerHTML = '<span class="spinner"></span> Parsing…';

  try {
    await api.parseJobPosting({
      link: linkEl.value || "",
      content,
      resume_id: includeScore ? state.mainResume.id : null,
      include_cover_letter: false,
      include_score: includeScore,
      cover_letter_prompt: null,
    });
    showToast("Job posting parsed");
    contentEl.value = "";
    linkEl.value = "";
    includeScoreEl.checked = false;
    await loadJobPostings();
  } catch (err) {
    showToast(err instanceof ApiError ? err.message : "Failed to parse job posting", "error");
  } finally {
    parseBtn.disabled = false;
    parseBtn.textContent = originalLabel;
  }
}

// ---------------------------------------------------------------------------
// settings panel
// ---------------------------------------------------------------------------

function initSettingsPanel() {
  const panel = document.getElementById("settingsPanel");
  const settingsBtn = document.getElementById("settingsBtn");
  const closeBtn = document.getElementById("closeSettingsBtn");
  const saveBtn = document.getElementById("saveSettingsBtn");
  const input = document.getElementById("apiBaseUrl");
  const status = document.getElementById("connStatus");

  settingsBtn.addEventListener("click", () => {
    input.value = state.apiBaseUrl;
    status.textContent = "";
    panel.classList.toggle("hidden");
  });
  closeBtn.addEventListener("click", () => panel.classList.add("hidden"));

  saveBtn.addEventListener("click", async () => {
    const value = input.value.trim() || DEFAULT_API_BASE_URL;
    await saveSettings(value);
    state.apiBaseUrl = value;
    status.textContent = "Saved. Reloading data…";
    panel.classList.add("hidden");
    await refreshAll();
  });
}

// ---------------------------------------------------------------------------
// init
// ---------------------------------------------------------------------------

async function refreshAll() {
  await Promise.all([loadClipboardNotes(), loadMainResume(), loadJobPostings()]);
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadSettings();
  initSettingsPanel();

  fillLinkFromActiveTab();
  document.getElementById("pasteBtn").addEventListener("click", () => pasteFromClipboard());
  document.getElementById("parseForm").addEventListener("submit", handleParseSubmit);
  document.getElementById("refreshBtn").addEventListener("click", loadJobPostings);

  // Best-effort: try to paste immediately so the popup opens ready to parse.
  // Falls back silently to the manual "Paste" button if the browser blocks
  // clipboard reads without a fresh user gesture.
  await pasteFromClipboard({ silent: true });

  await refreshAll();
});
