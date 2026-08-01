// Jawb Tracker popup logic

let mainResumeId = null;

function showToast(message, type = "success") {
  const host = document.getElementById("toastHost");
  const el = document.createElement("div");
  el.className = `toast${type === "error" ? " toast--error" : ""}`;
  el.textContent = message;
  host.innerHTML = "";
  host.appendChild(el);
  setTimeout(() => {
    if (host.contains(el)) host.removeChild(el);
  }, 3200);
}

function scoreDialHtml(score) {
  if (score == null) return `<span class="hint">—</span>`;
  const cls = score >= 70 ? "" : score >= 40 ? " score-dial--mid" : " score-dial--low";
  return `<span class="score-dial${cls}">${Math.round(score)}</span>`;
}

// ---------- tabs ----------

function initTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"));
      document.getElementById(`view-${btn.dataset.view}`).classList.add("active");
      if (btn.dataset.view === "postings") loadPostings();
    });
  });
}

// ---------- clipboard notes ----------

async function loadClipboardStrip() {
  const host = document.getElementById("clipboardStrip");
  try {
    const api = await makeApi();
    const notes = await api.listClipboardNotes();
    if (!notes || notes.length === 0) {
      host.innerHTML = "";
      return;
    }
    host.innerHTML = `
      <div class="clipboard-strip__title">Clipboard notes</div>
      <div class="clip-list">
        ${notes
          .map(
            (n) => `
          <button class="clip-btn" data-content="${escapeAttr(n.content)}" title="${escapeAttr(n.content)}">
            <span class="clip-btn__glyph">⎘</span>
            <span class="clip-btn__label">${escapeHtml(n.title || "Untitled note")}</span>
          </button>`
          )
          .join("")}
      </div>`;
    host.querySelectorAll(".clip-btn").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(btn.dataset.content);
          showToast("Copied to clipboard");
        } catch {
          showToast("Couldn't access clipboard", "error");
        }
      });
    });
  } catch (err) {
    host.innerHTML = "";
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function escapeAttr(s) {
  return escapeHtml(s).replace(/\n/g, " ");
}

// ---------- main resume ----------

async function loadMainResume() {
  const hint = document.getElementById("mainResumeHint");
  const checkbox = document.getElementById("scoreCheckbox");
  try {
    const api = await makeApi();
    const resume = await api.getMainResume();
    mainResumeId = resume.id;
    hint.textContent = `Main resume: ${resume.resume_name}`;
    hint.className = "hint";
  } catch (err) {
    mainResumeId = null;
    checkbox.checked = false;
    checkbox.disabled = true;
    hint.textContent = "No main resume set — set one in the full tracker to enable scoring.";
    hint.className = "hint hint--warn";
  }
}

// ---------- active tab link autofill ----------

async function autofillLink() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab && tab.url && /^https?:\/\//.test(tab.url)) {
      document.getElementById("linkInput").value = tab.url;
    }
  } catch {
    // ignore — activeTab permission may not have resolved yet
  }
}

// ---------- paste from clipboard ----------

function initPasteButton() {
  document.getElementById("pasteBtn").addEventListener("click", async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (!text) {
        showToast("Clipboard is empty", "error");
        return;
      }
      document.getElementById("contentInput").value = text;
      showToast("Pasted from clipboard");
    } catch {
      showToast("Couldn't read clipboard — paste manually instead", "error");
    }
  });
}

// ---------- parse form ----------

function initParseForm() {
  const form = document.getElementById("parseForm");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const content = document.getElementById("contentInput").value.trim();
    const link = document.getElementById("linkInput").value.trim();
    const wantsScore = document.getElementById("scoreCheckbox").checked;

    if (!content) {
      showToast("Paste a job posting first", "error");
      return;
    }
    if (wantsScore && !mainResumeId) {
      showToast("No main resume available to score against", "error");
      return;
    }

    const submitBtn = document.getElementById("submitBtn");
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner"></span> Parsing…`;

    try {
      const api = await makeApi();
      const posting = await api.parseJobPosting({
        link: link || "",
        content,
        resume_id: wantsScore ? mainResumeId : null,
        include_cover_letter: false,
        include_score: wantsScore,
        cover_letter_prompt: null,
      });
      showToast("Job posting parsed");
      renderResult(posting);
      document.getElementById("contentInput").value = "";
      form.reset();
      autofillLink();
    } catch (err) {
      showToast(err.message || "Failed to parse job posting", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Parse job posting";
    }
  });
}

function renderResult(posting) {
  const host = document.getElementById("resultCard");
  const score = posting.rubric ? posting.rubric.overall_score : null;
  host.innerHTML = `
    <div class="result-card">
      <div class="result-card__info">
        <div class="result-card__title">${escapeHtml(posting.title || "Untitled role")}</div>
        <div class="result-card__sub">${escapeHtml(posting.company || "—")}</div>
      </div>
      ${scoreDialHtml(score)}
    </div>`;
}

// ---------- postings table ----------

async function loadPostings() {
  const host = document.getElementById("postingsTableWrap");
  host.innerHTML = `<div class="loading-line">Loading…</div>`;
  try {
    const api = await makeApi();
    const postings = await api.listJobPostings({ limit: 15 });
    if (!postings || postings.length === 0) {
      host.innerHTML = `<div class="empty-state">No job postings yet. Parse one from the Parse tab.</div>`;
      return;
    }
    const settings = await getSettings();
    host.innerHTML = `
      <table class="jp-table">
        <thead><tr><th>Role</th><th>Company</th><th>Score</th></tr></thead>
        <tbody>
          ${postings
            .map(
              (jp) => `
            <tr data-id="${jp.id}">
              <td class="cell-title">${escapeHtml(jp.title || "Untitled role")}</td>
              <td class="cell-muted">${escapeHtml(jp.company || "—")}</td>
              <td>${scoreDialHtml(jp.overall_score)}</td>
            </tr>`
            )
            .join("")}
        </tbody>
      </table>`;
    host.querySelectorAll("tbody tr").forEach((row) => {
      row.addEventListener("click", () => {
        const id = row.dataset.id;
        chrome.tabs.create({ url: `${settings.webAppUrl.replace(/\/+$/, "")}/job-postings/${id}` });
      });
    });
  } catch (err) {
    host.innerHTML = `<div class="empty-state">${escapeHtml(err.message || "Failed to load job postings")}</div>`;
  }
}

// ---------- footer / options ----------

async function initFooter() {
  const settings = await getSettings();
  document.getElementById("openAppLink").href = settings.webAppUrl;
}

document.getElementById("openOptionsBtn").addEventListener("click", () => {
  chrome.runtime.openOptionsPage();
});
document.getElementById("refreshPostingsBtn").addEventListener("click", loadPostings);

// ---------- init ----------

initTabs();
initPasteButton();
initParseForm();
loadClipboardStrip();
loadMainResume();
autofillLink();
initFooter();
