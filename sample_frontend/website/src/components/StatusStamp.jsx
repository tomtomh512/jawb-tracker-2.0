import { STATUS_LABELS } from "../constants";

export default function StatusStamp({ status }) {
  if (!status) return null;
  return <span className={`stamp stamp--${status}`}>{STATUS_LABELS[status] || status}</span>;
}
