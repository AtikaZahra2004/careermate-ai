import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AuthHero from "../components/AuthHero";

export default function Register() {
  const { register, login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ first_name: "", username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await register(form);
      await login(form.username, form.password);
      navigate("/dashboard");
    } catch (err) {
      const data = err.response?.data;
      setError(data ? Object.values(data).flat().join(" ") : "Registration failed.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-page">
      <AuthHero />
      <div className="auth-panel">
        <form className="auth-card" onSubmit={handleSubmit}>
          <h2>Create account</h2>
          <p className="sub">Start tracking jobs with AI</p>
          {error && <div className="error">{error}</div>}
          <div className="field">
            <label htmlFor="first_name">Full name</label>
            <input id="first_name" name="first_name" value={form.first_name} onChange={handleChange} required />
          </div>
          <div className="field">
            <label htmlFor="username">Username</label>
            <input id="username" name="username" value={form.username} onChange={handleChange} required />
          </div>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input id="email" name="email" type="email" value={form.email} onChange={handleChange} required />
          </div>
          <div className="field">
            <label htmlFor="password">Password (min 6 characters)</label>
            <input id="password" name="password" type="password" minLength={6} value={form.password} onChange={handleChange} required />
          </div>
          <button className="btn" disabled={busy}>{busy ? "Creating..." : "Register"}</button>
          <p className="switch">Already have an account? <Link to="/login">Login</Link></p>
        </form>
      </div>
    </div>
  );
}