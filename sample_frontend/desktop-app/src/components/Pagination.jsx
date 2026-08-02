export default function Pagination({ skip, limit, count, onPage }) {
  const page = Math.floor(skip / limit) + 1;
  const hasNext = count === limit; // best-effort: backend doesn't return a total count
  const hasPrev = skip > 0;

  return (
    <div className="pager">
      <span>
        Page {page} · showing {count} {count === 1 ? "result" : "results"}
      </span>
      <div style={{ flex: 1 }} />
      <button className="icon-btn" disabled={!hasPrev} onClick={() => onPage(Math.max(0, skip - limit))}>
        ← Prev
      </button>
      <button className="icon-btn" disabled={!hasNext} onClick={() => onPage(skip + limit)}>
        Next →
      </button>
    </div>
  );
}
