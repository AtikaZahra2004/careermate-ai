import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const FEATURES = [
  ["AI job assistant", "Chat in English or Hinglish. The AI searches jobs, saves them and updates your status."],
  ["Resume match score", "Upload your PDF resume and see how well you match each job, and which skills are missing."],
  ["Application tracker", "Move every job through Saved, Applied, Interview, Offer or Rejected."],
  ["Official apply links", "Apply opens the company careers page and marks the job as applied for you."],
];

const STEPS = [
  "Create a free account",
  "Upload your resume",
  "Chat with the AI to find jobs",
  "Apply and track every application",
];

export default function Landing() {
  const { user, loading } = useAuth();
  if (loading) return <div className="center-screen">Loading...</div>;
  if (user) return <Navigate to="/dashboard" replace />;

  return (
    <div className="land">
      <header className="land-nav">
        <div className="brand">Career<span>Mate</span> AI</div>
        <div className="land-links">
          <Link to="/login" className="land-login">Login</Link>
          <Link to="/register" className="land-cta small">Get started</Link>
        </div>
      </header>

      <section className="land-hero">
        <h1>Find jobs, match your resume and track every application</h1>
        <p>CareerMate AI is a job search assistant for freshers. Just chat with it, and it does the searching and tracking for you.</p>
        <div className="land-actions">
          <Link to="/register" className="land-cta">Create free account</Link>
          <Link to="/login" className="land-ghost">I already have an account</Link>
        </div>
      </section>

      <section className="land-section">
        <h2>What you can do</h2>
        <div className="feature-grid">
          {FEATURES.map(([title, text]) => (
            <div className="feature" key={title}>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="land-section">
        <h2>How it works</h2>
        <div className="steps">
          {STEPS.map((s, i) => (
            <div className="step" key={s}>
              <span>{i + 1}</span>
              <p>{s}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="land-footer">
        Built with Django REST Framework, React and MySQL
      </footer>
    </div>
  );
}