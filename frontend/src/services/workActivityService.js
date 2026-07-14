import api from '../api/axios';

const workActivityService = {
  createActivity: async (data) => {
    const response = await api.post('/work-activities', data);
    return response;
  },
  startActivity: async (id, assets = []) => {
    const response = await api.patch(`/work-activities/${id}/start`, { assets });
    return response;
  },
  pauseActivity: async (id) => {
    const response = await api.patch(`/work-activities/${id}/pause`);
    return response;
  },
  resumeActivity: async (id) => {
    const response = await api.patch(`/work-activities/${id}/resume`);
    return response;
  },
  cancelActivity: async (id) => {
    const response = await api.patch(`/work-activities/${id}/cancel`);
    return response;
  },
  finishActivity: async (id) => {
    const response = await api.patch(`/work-activities/${id}/finish`);
    return response;
  },
  getMyActivities: async () => {
    const response = await api.get('/work-activities/me');
    return response;
  },
  getTodayActivities: async () => {
    const response = await api.get('/work-activities/me/today');
    return response;
  },
  getCurrentActivity: async () => {
    const response = await api.get('/work-activities/current');
    return response;
  },
  getActivityById: async (id) => {
    const response = await api.get(`/work-activities/${id}`);
    return response;
  },
};

export default workActivityService;
