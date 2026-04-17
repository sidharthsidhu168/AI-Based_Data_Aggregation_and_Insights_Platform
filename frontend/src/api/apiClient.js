import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api",
});

// Attach token to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auth
export const login = (data) => api.post("/auth/login", data);
export const register = (data) => api.post("/auth/register", data);

// Upload
export const uploadFile = (formData) =>
  api.post("/upload/file", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
export const getDatasets = () => api.get("/upload/datasets");

// Insights
export const getSummary = (datasetId) =>
  api.get(`/insights/summary/${datasetId}`);
export const getTrend = (datasetId, column) =>
  api.get(`/insights/trend/${datasetId}?column=${column}`);
export const runRegression = (datasetId, data) =>
  api.post(`/insights/regression/${datasetId}`, data);
export const runClustering = (datasetId, data) =>
  api.post(`/insights/cluster/${datasetId}`, data);
export const getAnomalies = (datasetId, column) =>
  api.get(`/insights/anomalies/${datasetId}?column=${column}`);

export default api;