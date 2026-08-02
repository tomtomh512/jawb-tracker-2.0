export class ApiError extends Error {
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
      `Could not reach the API at ${baseUrl}. Check the backend URL in Settings and make sure the server is running (and CORS is enabled).`,
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
      detail = detail || "Rate limit reached. This action is limited (3 per minute) — please wait a moment and try again.";
    }
    throw new ApiError(detail || `Request failed (${res.status})`, res.status, body);
  }

  return body;
}

async function requestForm(baseUrl, path, formData) {
  const url = `${baseUrl.replace(/\/+$/, "")}${path}`;
  let res;
  try {
    res = await fetch(url, {
      method: "POST",
      body: formData, // no headers set — the browser adds the correct multipart Content-Type + boundary automatically
    });
  } catch (err) {
    throw new ApiError(
      `Could not reach the API at ${baseUrl}. Check the backend URL in Settings and make sure the server is running (and CORS is enabled).`,
      0,
      null
    );
  }

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
      detail = detail || "Rate limit reached. This action is limited (3 per minute) — please wait a moment and try again.";
    }
    throw new ApiError(detail || `Request failed (${res.status})`, res.status, body);
  }

  return body;
}

export function makeApi(baseUrl) {
  const get = (path) => request(baseUrl, path);
  const post = (path, data) => request(baseUrl, path, { method: "POST", body: JSON.stringify(data ?? {}) });
  const postForm = (path, formData) => requestForm(baseUrl, path, formData);
  const patch = (path, data) => request(baseUrl, path, { method: "PATCH", body: JSON.stringify(data ?? {}) });
  const del = (path) => request(baseUrl, path, { method: "DELETE" });

  const qs = (params) => {
    const usp = new URLSearchParams();
    Object.entries(params || {}).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") usp.set(k, v);
    });
    const s = usp.toString();
    return s ? `?${s}` : "";
  };

  return {
    // ---- job postings ----
    listJobPostings: (params) => get(`/job-postings/${qs(params)}`),
    getJobPosting: (id) => get(`/job-postings/${id}`),
    createJobPosting: (data) => post(`/job-postings/`, data),
    parseJobPosting: (data) => post(`/job-postings/parse`, data),
    updateJobPosting: (id, data) => patch(`/job-postings/${id}`, data),
    generateCoverLetter: (id, data) => post(`/job-postings/${id}/cover-letter`, data),
    generateScore: (id, data) => post(`/job-postings/${id}/score`, data),
    deleteJobPosting: (id) => del(`/job-postings/${id}`),

    // ---- resumes ----
    listResumes: (params) => get(`/resumes/${qs(params)}`),
    getMainResume: () => get(`/resumes/main`),
    getResume: (id) => get(`/resumes/${id}`),
    createResume: (data) => post(`/resumes/`, data),
    parseResume: (data) => post(`/resumes/parse`, data),
    parseResumePdf: (resumeName, file) => {
      const formData = new FormData();
      formData.append("resume_name", resumeName);
      formData.append("pdf", file);
      return postForm(`/resumes/parsePdf`, formData);
    },
    updateResume: (id, data) => patch(`/resumes/${id}`, data),
    setMainResume: (id) => patch(`/resumes/${id}/main`),
    deleteResume: (id) => del(`/resumes/${id}`),

    // ---- resume sub-resources ----
    subresource: (kind) => {
      const path = SUBRESOURCE_PATHS[kind];
      return {
        list: (resumeId) => get(`/resumes/${resumeId}/${path}/`),
        create: (resumeId, data) => post(`/resumes/${resumeId}/${path}/`, data),
        update: (resumeId, itemId, data) => patch(`/resumes/${resumeId}/${path}/${itemId}`, data),
        remove: (resumeId, itemId) => del(`/resumes/${resumeId}/${path}/${itemId}`),
      };
    },

    // ---- notes ----
    listNotes: (params) => get(`/notes/${qs(params)}`),
    listClipboardNotes: () => get(`/notes/clipboard`),
    getNote: (id) => get(`/notes/${id}`),
    createNote: (data) => post(`/notes/`, data),
    updateNote: (id, data) => patch(`/notes/${id}`, data),
    deleteNote: (id) => del(`/notes/${id}`),
  };
}

export const SUBRESOURCE_PATHS = {
  educations: "educations",
  experiences: "experiences",
  projects: "projects",
  skillCategories: "skill-categories",
  certifications: "certifications",
  publications: "publications",
  awards: "awards",
  customSections: "custom-sections",
};
