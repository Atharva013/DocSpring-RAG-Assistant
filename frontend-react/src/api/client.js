import axios from 'axios';

// Base Axios instance pointing to FastAPI backend running on http://localhost:8000
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 45000,
});

export default apiClient;
