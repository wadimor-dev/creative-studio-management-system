import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const categoryService = {
  getAll: () => {
    return apiClient.get(ENDPOINTS.CATEGORIES);
  },
  
  create: (data) => {
    return apiClient.post(ENDPOINTS.CATEGORIES, data);
  },
  
  update: (id, data) => {
    return apiClient.put(`${ENDPOINTS.CATEGORIES}/${id}`, data);
  },
  
  delete: (id) => {
    return apiClient.delete(`${ENDPOINTS.CATEGORIES}/${id}`);
  }
};
