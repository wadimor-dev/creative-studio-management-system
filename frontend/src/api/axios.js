import axios from 'axios';
import { setupInterceptors } from './interceptors';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'; // 'https://api-csms.idekode.web.id/api/v1';

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

// Attach interceptors
setupInterceptors(apiClient);

export default apiClient;
