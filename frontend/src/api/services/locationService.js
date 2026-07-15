import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const locationService = {
  getAll: () => {
    return apiClient.get(ENDPOINTS.LOCATIONS);
  },
  
  getById: (id) => {
    return apiClient.get(`${ENDPOINTS.LOCATIONS}/${id}`);
  },
  
  create: (data) => {
    return apiClient.post(ENDPOINTS.LOCATIONS, data);
  },
  
  update: (id, data) => {
    return apiClient.put(`${ENDPOINTS.LOCATIONS}/${id}`, data);
  },
  
  delete: (id) => {
    return apiClient.delete(`${ENDPOINTS.LOCATIONS}/${id}`);
  }
};
