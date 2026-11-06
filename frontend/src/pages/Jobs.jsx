import { useEffect, useState } from "react";
import api from "../api/axios";
import JobCard from "../components/JobCard";

export default function Jobs() {
  const [filters, setFilters] = useState({ q: "", city: "", job_type: "" });
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ count: 0, results: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const timer = setTimeout(async () => {
      setLoading(true);
      setError("");
      try {
        const params = { page };
        Object.entries(filters).forEach(([k, v]) => {
          if (v) params[k] = v;
        });
        const res = await api.get("/jobs/", { params });
        setData(res.data);
      } catch {
        setError("Could not load jobs.");
      } finally {
        setLoading(false);
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [filters, page]);

  const change = (e) => {
    setPage(1);
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const totalPages = Math.max(1, Math.ceil(data.count / 10));

  return (
    <div>
      <h1 className="page-title">Find Jobs</h1>
      <div className="filters">
        <input name="q" placeholder="Search title, company, keyword" value={filters.q} onChange={change} aria-label="Search" />
        <input name="city" placeholder="City (e.g. Bengaluru)" value={filters.city} onChange={change} aria-label="City" />
        <select name="job_type" value={filters.job_type} onChange={change} aria-label="Job type">
          <option value="">All types</option>
          <option value="Full-time">Full-time</option>
          <option value="Internship">Internship</option>
        </select>
      </div>

      {error && <div className="error">{error}</div>}
      {loading && <p className="muted">Loading jobs...</p>}
      {!loading && data.results.length === 0 && !error && <p className="muted">No jobs found.</p>}

      <div className="job-grid">
        {data.results.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>

      {data.count > 10 && (
        <div className="pager">
          <button className="btn-sm" disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button>
          <span>Page {page} of {totalPages}</span>
          <button className="btn-sm" disabled={page >= totalPages} onClick={() => setPage(page + 1)}>Next</button>
        </div>
      )}
    </div>
  );
}