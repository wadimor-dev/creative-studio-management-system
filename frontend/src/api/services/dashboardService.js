import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const dashboardService = {
  getMetrics: (days = 7) => {
    return apiClient.get(`${ENDPOINTS.DASHBOARD.METRICS}?days=${days}`);
  }
};
