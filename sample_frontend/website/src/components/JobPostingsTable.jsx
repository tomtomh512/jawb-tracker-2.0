import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useApi } from "../api/useApi";
import { useToast } from "../context/ToastContext";
import { JOB_STATUSES, STATUS_LABELS, formatSalary, formatDate } from "../constants";
import StatusStamp from "./StatusStamp";
import ScoreDial from "./ScoreDial";
import Pagination from "./Pagination";
import Modal from "./Modal";
import JobPostingForm from "./JobPostingForm";

const LIMIT = 10;

export default function JobPostingsTable({ refreshKey, onCreated }) {
  const api = useApi();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [status, setStatus] = useState("");
  const [skip, setSkip] = useState(0);
  const [postings, setPostings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showManual, setShowManual] = useState(false);

  useEffect(() => {
    setSkip(0);
  }, [status]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api
      .listJobPostings({ status: status || undefined, skip, limit: LIMIT })
      .then((list) => !cancelled && setPostings(list))
      .catch((err) => !cancelled && showToast(err.message, "error"))
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [status, skip, refreshKey]);

  async function handleManualCreate(payload) {
    try {
      const created = await api.createJobPosting(payload);
      showToast("Job posting added");
      setShowManual(false);
      onCreated?.(created);
      navigate(`/job-postings/${created.id}`);
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  return (
    <div className="card">
      <div className="card__header">
        <div>
          <span className="card__eyebrow">Tracker</span>
          <h2>Job postings</h2>
        </div>
        <div className="toolbar">
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">All statuses</option>
            {JOB_STATUSES.map((s) => (
              <option key={s} value={s}>
                {STATUS_LABELS[s]}
              </option>
            ))}
          </select>
          <button className="btn btn--ghost btn--sm" onClick={() => setShowManual(true)}>
            + Add manually
          </button>
        </div>
      </div>

      <div className="table-wrap">
        {loading ? (
          <div className="loading-line">Loading job postings…</div>
        ) : postings.length === 0 ? (
          <div className="empty-state">
            <h3>Nothing here yet</h3>
            <p>Paste a posting on the left, or add one manually.</p>
          </div>
        ) : (
          <table className="jp-table">
            <thead>
              <tr>
                <th>Role</th>
                <th>Company</th>
                <th>Status</th>
                <th>Salary</th>
                <th>Score</th>
                <th>Added</th>
              </tr>
            </thead>
            <tbody>
              {postings.map((jp) => (
                <tr key={jp.id} onClick={() => navigate(`/job-postings/${jp.id}`)}>
                  <td className="cell-title">{jp.title || "Untitled role"}</td>
                  <td>{jp.company || "—"}</td>
                  <td>
                    <StatusStamp status={jp.status} />
                  </td>
                  <td className="cell-mono cell-muted">{formatSalary(jp)}</td>
                  <td>
                    <ScoreDial score={jp.overall_score} />
                  </td>
                  <td className="cell-muted cell-mono">{formatDate(jp.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {!loading && postings.length > 0 && (
        <Pagination skip={skip} limit={LIMIT} count={postings.length} onPage={setSkip} />
      )}

      {showManual && (
        <Modal title="Add a job posting manually" onClose={() => setShowManual(false)} wide>
          <JobPostingForm
            onSubmit={handleManualCreate}
            onCancel={() => setShowManual(false)}
            submitLabel="Add job posting"
            includeStatus
          />
        </Modal>
      )}
    </div>
  );
}
