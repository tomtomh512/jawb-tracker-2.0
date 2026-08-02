import { useState } from "react";
import ClipboardStrip from "../components/ClipboardStrip";
import ParsePanel from "../components/ParsePanel";
import JobPostingsTable from "../components/JobPostingsTable";

export default function Home() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="page">
      <ClipboardStrip />
      <div className="home-grid">
        <ParsePanel onCreated={() => setRefreshKey((k) => k + 1)} />
        <JobPostingsTable refreshKey={refreshKey} onCreated={() => setRefreshKey((k) => k + 1)} />
      </div>
    </div>
  );
}
