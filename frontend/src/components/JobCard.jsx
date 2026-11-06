import { useState } from "react";
import api from "../api/axios";

const APPLIED = ["applied", "interview", "offer", "rejected"];

export default function JobCard({ job }) {
  const [status, setStatus] = useState(job.my_status);
  const [match, setMatch] = useState(null);
  const [msg, setMsg] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);

  const saveJob = async () => {
    setMsg("");
    try {
      await api.post("/applications/", { job_id: job.id, status: "saved" });
      setStatus("saved");
    } catch (err) {
      const text = err.response?.data?.error || "Could not save this job.";
      if (text.includes("already")) setStatus((s) => s || "saved");
      else setMsg(text);
    }
  };

  const applyJob = async () => {
    setMsg("");
    setNote("");
    // open the company link first (inside the click, so the browser allows it)
    if (job.apply_url) window.open(job.apply_url, "_blank", "noopener,noreferrer");
    setBusy(true);
    try {
      const { data } = await api.post("/applications/apply/", { job_id: job.id });
      setStatus(data.status);
      setNote("Marked as applied in your tracker.");
    } catch (err) {
      setMsg(err.response?.data?.error || "Could not mark as applied.");
    } finally {
      setBusy(false);
    }
  };

  const checkMatch = async () => {
    setMsg("");
    try {
      const { data } = await api.get(`/jobs/${job.id}/match/`);
      setMatch(data);
    } catch (err) {
      setMsg(err.response?.data?.error || "Could not check match.");
    }
  };

  const isApplied = APPLIED.includes(status);

  return (
    <div className="job">
      <div className="job-top">
        <div>
          <h3>{job.title}</h3>
          <div className="muted">{job.company} · {job.city}</div>
        </div>
        <span className="pill type">{job.job_type}</span>
      </div>
      <p className="desc">{job.description}</p>
      <div className="skills">
        {job.skills.map((s) => (
          <span key={s} className="skill">{s}</span>
        ))}
      </div>
      <div className="muted">Experience: {job.min_experience}-{job.max_experience} yrs</div>

      {match && (
        <div className="match">
          <b>{match.score}% match</b>
          {match.missing.length > 0 && <span> · Missing: {match.missing.join(", ")}</span>}
        </div>
      )}
      {note && <div className="success" style={{ margin: 0 }}>{note}</div>}
      {msg && <div className="error small">{msg}</div>}

      <div className="actions">
        <button className="btn-sm apply" onClick={applyJob} disabled={busy || isApplied}>
          {isApplied ? "Applied ✓" : busy ? "Applying..." : "Apply now"}
        </button>
        <button className="btn-sm primary" onClick={saveJob} disabled={!!status}>
          {status ? (isApplied ? "In tracker" : "Saved") : "Save"}
        </button>
        <button className="btn-sm" onClick={checkMatch}>Check match</button>
      </div>
    </div>
  );
}