import apiClient from '../axios';

export const systemService = {
  getBackups: async () => {
    const response = await apiClient.get('/system/backups');
    return response.data;
  },
  triggerBackup: async () => {
    const response = await apiClient.post('/system/backups/trigger');
    return response.data;
  },
  downloadBackupUrl: (filename) => {
    return `${import.meta.env.VITE_API_URL}/api/v1/system/backups/download/${filename}`;
  }
};
