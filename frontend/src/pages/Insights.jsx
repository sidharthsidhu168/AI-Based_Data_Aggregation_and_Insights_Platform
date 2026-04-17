import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getTrend, runRegression, runClustering, getAnomalies } from "../api/apiClient";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function Insights() {
  const [params] = useSearchParams();
  const datasetId = params.get("id");

  const [column, setColumn] = useState("");
  const [trendData, setTrendData] = useState(null);
  const [clusterResult, setClusterResult] = useState(null);
  const [anomalyResult, setAnomalyResult] = useState(null);

  const loadTrend = async () => {
    const { data } = await getTrend(datasetId, column);
    const formatted = data.values.map((v, i) => ({
      index: i, value: v,
      rolling: data.rolling_mean[i] ?? null
    }));
    setTrendData(formatted);
  };

  const loadClusters = async () => {
    const { data } = await runClustering(datasetId, { n_clusters: 3 });
    setClusterResult(data);
  };

  const loadAnomalies = async () => {
    const { data } = await getAnomalies(datasetId, column);
    setAnomalyResult(data);
  };

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", padding: "0 20px" }}>
      <h2>AI Insights</h2>
      <p>Dataset ID: <code>{datasetId}</code></p>

      <div style={{ marginBottom: 24 }}>
        <input placeholder="Enter column name for analysis" value={column}
          onChange={(e) => setColumn(e.target.value)}
          style={{ marginRight: 8, padding: "6px 10px" }} />
        <button onClick={loadTrend}>Show Trend</button>
        <button onClick={loadAnomalies} style={{ marginLeft: 8 }}>Detect Anomalies</button>
        <button onClick={loadClusters} style={{ marginLeft: 8 }}>Run Clustering</button>
      </div>

      {trendData && (
        <>
          <h3>Trend: {column}</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#4f8ef7" dot={false} name="Value" />
              <Line type="monotone" dataKey="rolling" stroke="#f47b4f" dot={false}
                strokeDasharray="5 5" name="5-period avg" />
            </LineChart>
          </ResponsiveContainer>
        </>
      )}

      {clusterResult && (
        <div style={{ marginTop: 24 }}>
          <h3>Clustering Result ({clusterResult.n_clusters} groups)</h3>
          {Object.entries(clusterResult.cluster_sizes).map(([k, v]) => (
            <p key={k}>Group {k}: {v} records</p>
          ))}
        </div>
      )}

      {anomalyResult && (
        <div style={{ marginTop: 24 }}>
          <h3>Anomalies Found: {anomalyResult.count}</h3>
          {anomalyResult.anomalies.slice(0, 5).map((row, i) => (
            <pre key={i} style={{ background: "#fff3cd", padding: 8, borderRadius: 4 }}>
              {JSON.stringify(row, null, 2)}
            </pre>
          ))}
        </div>
      )}
    </div>
  );
}