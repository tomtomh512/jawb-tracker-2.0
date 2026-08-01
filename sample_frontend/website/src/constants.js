export const JOB_STATUSES = [
  "saved",
  "applied",
  "assessment",
  "interview",
  "offer",
  "accepted",
  "rejected",
  "withdrawn",
  "ghosted",
];

export const STATUS_LABELS = {
  saved: "Saved",
  applied: "Applied",
  assessment: "Assessment",
  interview: "Interview",
  offer: "Offer",
  accepted: "Accepted",
  rejected: "Rejected",
  withdrawn: "Withdrawn",
  ghosted: "Ghosted",
};

export const EMPLOYMENT_TYPES = [
  "full_time",
  "part_time",
  "contract",
  "temporary",
  "internship",
  "freelance",
];

export const EMPLOYMENT_TYPE_LABELS = {
  full_time: "Full-time",
  part_time: "Part-time",
  contract: "Contract",
  temporary: "Temporary",
  internship: "Internship",
  freelance: "Freelance",
};

export const EDUCATION_LEVELS = ["high_school", "associates", "bachelors", "masters", "phd"];

export const EDUCATION_LEVEL_LABELS = {
  high_school: "High school",
  associates: "Associate's",
  bachelors: "Bachelor's",
  masters: "Master's",
  phd: "PhD",
};

export function formatSalary(jp) {
  if (jp.min_salary == null && jp.max_salary == null) return "—";
  const cur = jp.currency ? `${jp.currency} ` : "";
  const period = jp.period ? `/${jp.period}` : "";
  if (jp.min_salary != null && jp.max_salary != null && jp.min_salary !== jp.max_salary) {
    return `${cur}${jp.min_salary.toLocaleString()}–${jp.max_salary.toLocaleString()}${period}`;
  }
  const val = jp.min_salary ?? jp.max_salary;
  return `${cur}${val.toLocaleString()}${period}`;
}

export function formatDate(d) {
  if (!d) return "—";
  try {
    return new Date(d).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
  } catch {
    return d;
  }
}
