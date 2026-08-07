import { Routes, Route } from "react-router-dom";
import TopBar from "./components/TopBar";
import Home from "./pages/Home";
import JobPostingDetail from "./pages/JobPostingDetail";
import Resumes from "./pages/Resumes";
import ResumeDetail from "./pages/ResumeDetail";
import Notes from "./pages/Notes";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <div className="app-shell">
      <TopBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/job-postings/:id" element={<JobPostingDetail />} />
        <Route path="/resumes" element={<Resumes />} />
        <Route path="/resumes/:id" element={<ResumeDetail />} />
        <Route path="/notes" element={<Notes />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="*" element={<div className="page">Page not found.</div>} />
      </Routes>
    </div>
  );
}
