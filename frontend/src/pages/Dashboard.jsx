import { useEffect, useState } from "react";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

const STATUS = [
  ["saved", "Saved", "#15803d", "#dcfce7"],
  ["applied", "Applied", "#c2410c", "#ffedd5"],
  ["interview", "Interview", "#a16207", "#fef9c3"],
  ["offer", "Offer", "#0f766e", "#ccfbf1"],
  ["rejected", "Rejected", "#b91c1c", "#fee2e2"],
];

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/applications/dashboard/")
      .then((res) => setData(res.data))
      .catch(() => setError("Could not load dashboard."));
  }, []);

  return (
    <div>
      <h1 className="page-title">Welcome back, {user?.first_name || user?.username}</h1>
      <p className="muted">Your job search at a glance</p>
      {error && <div className="error">{error}</div>}
      {!data && !error && <p className="muted">Loading...</p>}
      {data && (
        <>
          <div className="stats">
            {STATUS.map(([key, label, color, bg]) => (
              <div className="stat" key={key} style={{ borderTop: `4px solid ${color}` }}>
                <span className="muted">{label}</span>
                <b style={{ color }}>{data.counts[key]}</b>
              </div>
            ))}
          </div>
          <div className="card">
            <h2>Recent activity</h2>
            {data.recent.length === 0 && (
              <p className="muted">No applications yet. Go to Jobs and save one.</p>
            )}
            {data.recent.map((a) => {
              const s = STATUS.find((x) => x[0] === a.status);
              return (
                <div className="row" key={a.id}>
                  <div>
                    <b>{a.job.title}</b>
                    <div className="muted">{a.job.company} · {a.job.city}</div>
                  </div>
                  <span className="pill" style={{ color: s[2], background: s[3] }}>{s[1]}</span>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}