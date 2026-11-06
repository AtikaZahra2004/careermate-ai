import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const links = [
  ["/dashboard", "Dashboard"],
  ["/jobs", "Jobs"],
  ["/tracker", "Tracker"],
  ["/resume", "My Resume"],
  ["/chat", "AI Chat"],
];

export default function Layout() {
  const { logout } = useAuth();
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">Career<span>Mate</span> AI</div>
        <nav>
          {links.map(([to, label]) => (
            <NavLink key={to} to={to} className={({ isActive }) => (isActive ? "nav active" : "nav")}>
              {label}
            </NavLink>
          ))}
        </nav>
        <button className="logout-btn" onClick={logout}>Logout</button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}