import { useState } from "react";
import { uploadFile } from "../api/apiClient";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return setStatus("Please select a file first.");
    setStatus("Uploading...");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const { data } = await uploadFile(formData);
      setResult(data);
      setStatus("Upload successful!");
    } catch (err) {
      setStatus(err.response?.data?.error || "Upload failed.");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", padding: "0 20px" }}>
      <h2>Upload Dataset</h2>
      <input type="file" accept=".csv,.xlsx,.xls"
        onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} style={{ marginLeft: 12 }}>Upload</button>
      <p>{status}</p>
      {result && (
        <div style={{ marginTop: 16, padding: 16, border: "1px solid #ccc", borderRadius: 8 }}>
          <p>Dataset ID: <code>{result.dataset_id}</code></p>
          <p>Rows: {result.row_count} | Columns: {result.columns.length}</p>
          <p>Columns: {result.columns.join(", ")}</p>
          <button onClick={() => navigate("/insights?id=" + result.dataset_id)}>
            View Insights →
          </button>
        </div>
      )}
    </div>
  );
}