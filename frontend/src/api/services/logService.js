import apiClient from '../axios';

export const logService = {
  getActivityLogs: async (skip = 0, limit = 50) => {
    const response = await apiClient.get('/logs/activity', { params: { skip, limit } });
    return response.data;
  },
  getAuditLogs: async (skip = 0, limit = 50) => {
    const response = await apiClient.get('/logs/audit', { params: { skip, limit } });
    return response.data;
  },
};
