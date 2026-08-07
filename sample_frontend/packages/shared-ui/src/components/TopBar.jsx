import { NavLink } from "react-router-dom";

export default function TopBar() {
  return (
    <header className="topbar">
      <NavLink to="/" className="topbar__brand">
        <span className="topbar__brand-name">Jawb Tracker</span>
      </NavLink>
      <nav className="topbar__nav">
        <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
          Home
        </NavLink>
        <NavLink to="/resumes" className={({ isActive }) => (isActive ? "active" : "")}>
          Resumes
        </NavLink>
        <NavLink to="/notes" className={({ isActive }) => (isActive ? "active" : "")}>
          Notes
        </NavLink>
        <NavLink to="/settings" className={({ isActive }) => (isActive ? "active" : "")}>
          Settings
        </NavLink>
      </nav>
    </header>
  );
}
