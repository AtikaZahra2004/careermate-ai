import { useEffect, useState } from "react";
import api from "../api/axios";

const COLUMNS = [
  ["saved", "Saved", "#15803d", "#dcfce7"],
  ["applied", "Applied", "#c2410c", "#ffedd5"],
  ["interview", "Interview", "#a16207", "#fef9c3"],
  ["offer", "Offer", "#0f766e", "#ccfbf1"],
  ["rejected", "Rejected", "#b91c1c", "#fee2e2"],
];

export default function Tracker() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/applications/")
      .then((res) => setApps(res.data))
      .catch(() => setError("Could not load applications."))
      .finally(() => setLoading(false));
  }, []);

  const changeStatus = async (id, status) => {
    setError("");
    try {
      const { data } = await api.patch(`/applications/${id}/`, { status });
      setApps(apps.map((a) => (a.id === id ? data : a)));
    } catch {
      setError("Could not update status.");
    }
  };

  const remove = async (id) => {
    if (!window.confirm("Remove this job from your tracker?")) return;
    setError("");
    try {
      await api.delete(`/applications/${id}/`);
      setApps(apps.filter((a) => a.id !== id));
    } catch {
      setError("Could not remove this job.");
    }
  };

  return (
    <div>
      <h1 className="page-title">Application Tracker</h1>
      <p className="muted">Change the status of a job using the dropdown on its card</p>
      {error && <div className="error">{error}</div>}
      {loading && <p className="muted">Loading...</p>}

      {!loading && apps.length === 0 && !error && (
        <div className="card">
          <p className="muted">Nothing here yet. Go to Jobs and save a job.</p>
        </div>
      )}

      {apps.length > 0 && (
        <div className="board">
          {COLUMNS.map(([key, label, color, bg]) => {
            const items = apps.filter((a) => a.status === key);
            return (
              <div className="col" key={key} style={{ background: bg }}>
                <div className="col-title" style={{ color }}>
                  {label} ({items.length})
                </div>
                {items.map((a) => (
                  <div className="t-card" key={a.id} style={{ borderTop: `4px solid ${color}` }}>
                    <b>{a.job.title}</b>
                    <span className="muted">{a.job.company} · {a.job.city}</span>
                    <select
                      value={a.status}
                      onChange={(e) => changeStatus(a.id, e.target.value)}
                      aria-label={`Status for ${a.job.title}`}
                    >
                      {COLUMNS.map(([k, l]) => (
                        <option key={k} value={k}>{l}</option>
                      ))}
                    </select>
                    <button className="link-btn" onClick={() => remove(a.id)}>Remove</button>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}