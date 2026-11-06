import { useEffect, useRef, useState } from "react";
import api, { API_ROOT } from "../api/axios";

export default function Resume() {
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");
  const inputRef = useRef(null);

  useEffect(() => {
    api
      .get("/auth/resume/")
      .then((res) => setResume(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const upload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setError("");
    setOk("");

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setError("Please choose a PDF file.");
      e.target.value = "";
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError("File is too large (max 5 MB).");
      e.target.value = "";
      return;
    }

    const form = new FormData();
    form.append("file", file);
    setBusy(true);
    try {
      const { data } = await api.post("/auth/resume/", form);
      setResume(data);
      setOk("Resume uploaded. Your skills are updated.");
    } catch (err) {
      setError(err.response?.data?.error || "Upload failed. Please try again.");
    } finally {
      setBusy(false);
      e.target.value = "";
    }
  };

  const fileUrl = !resume?.file
    ? ""
    : resume.file.startsWith("http")
    ? resume.file
    : `${API_ROOT}${resume.file}`;

  return (
    <div>
      <h1 className="page-title">My Resume</h1>
      <p className="muted">Upload a text-based PDF. We detect your skills to calculate job match.</p>

      <div className="card">
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={upload}
          hidden
        />
        <div className="upload-box">
          <p style={{ margin: 0 }}>
            {resume ? "Want to replace your resume?" : "No resume uploaded yet"}
          </p>
          <button
            className="btn"
            style={{ maxWidth: 220 }}
            onClick={() => inputRef.current.click()}
            disabled={busy}
          >
            {busy ? "Uploading..." : resume ? "Upload new PDF" : "Upload PDF"}
          </button>
          <span className="muted">PDF only, max 5 MB</span>
        </div>
        {error && <div className="error" style={{ marginTop: 14 }}>{error}</div>}
        {ok && <div className="success">{ok}</div>}
      </div>

      {loading && <p className="muted">Loading...</p>}

      {resume && (
        <div className="card">
          <h2>Detected skills</h2>
          {resume.extracted_skills.length > 0 ? (
            <div className="skills">
              {resume.extracted_skills.map((s) => (
                <span key={s} className="skill">{s}</span>
              ))}
            </div>
          ) : (
            <p className="muted">
              No known skills found. Make sure your resume text mentions skills like Python, Django, React, SQL.
            </p>
          )}
          <p className="muted" style={{ marginTop: 14 }}>
            Uploaded on {new Date(resume.uploaded_at).toLocaleDateString()}
            {fileUrl && (
              <>
                {" · "}
                <a href={fileUrl} target="_blank" rel="noreferrer">View PDF</a>
              </>
            )}
          </p>
        </div>
      )}
    </div>
  );
}