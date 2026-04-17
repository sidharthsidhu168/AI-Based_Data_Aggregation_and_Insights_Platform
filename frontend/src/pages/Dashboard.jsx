import { useEffect, useState } from "react";
import { getDatasets, getSummary } from "../api/apiClient";
import { useAuth } from "../context/AuthContext";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  LineChart, Line, ResponsiveContainer, CartesianGrid
} from "recharts";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [datasets, setDatasets] = useState([]);
  const [selected, setSelected] = useState(null);
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    getDatasets().then(({ data }) => setDatasets(data.datasets));
  }, []);

  const loadSummary = async (datasetId) => {
    setSelected(datasetId);
    const { data } = await getSummary(datasetId);
    setSummary(data);
  };

  // Convert stats to chart-ready format
  const chartData = summary
    ? Object.entries(summary.stats).map(([col, vals]) => ({
        name: col.length > 10 ? col.substring(0, 10) + "…" : col,
        mean: vals.mean,
        max: vals.max,
        min: vals.min,
      }))
    : [];

  return (
    <div style={{ padding: "24px", maxWidth: 1000, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h2>Welcome, {user?.name}</h2>
        <button onClick={logout}>Logout</button>
      </div>

      <h3>Your Datasets</h3>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        {datasets.map((d) => (
          <div key={d.dataset_id}
            onClick={() => loadSummary(d.dataset_id)}
            style={{
              padding: "12px 16px", border: "1px solid #ccc",
              borderRadius: 8, cursor: "pointer",
              background: selected === d.dataset_id ? "#e8f4ff" : "white"
            }}>
            <strong>{d.filename}</strong>
            <p style={{ margin: 0, fontSize: 13, color: "#666" }}>
              {d.row_count} rows · {d.columns.length} columns
            </p>
          </div>
        ))}
      </div>

      {summary && (
        <>
          <h3>Column Statistics</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="mean" fill="#4f8ef7" name="Mean" />
              <Bar dataKey="max" fill="#f47b4f" name="Max" />
            </BarChart>
          </ResponsiveContainer>
        </>
      )}
    </div>
  );
}