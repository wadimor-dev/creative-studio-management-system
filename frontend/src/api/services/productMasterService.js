import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const productMasterService = {
  getAll: (entityType) => {
    if (entityType === 'locations') return apiClient.get(ENDPOINTS.LOCATIONS);
    return apiClient.get(`${ENDPOINTS.PRODUCT_MASTER}/${entityType}`);
  },
  
  create: (entityType, data) => {
    if (entityType === 'locations') return apiClient.post(ENDPOINTS.LOCATIONS, data);
    return apiClient.post(`${ENDPOINTS.PRODUCT_MASTER}/${entityType}`, data);
  },
  
  update: (entityType, id, data) => {
    if (entityType === 'locations') return apiClient.put(`${ENDPOINTS.LOCATIONS}/${id}`, data);
    return apiClient.put(`${ENDPOINTS.PRODUCT_MASTER}/${entityType}/${id}`, data);
  },
  
  delete: (entityType, id) => {
    if (entityType === 'locations') return apiClient.delete(`${ENDPOINTS.LOCATIONS}/${id}`);
    return apiClient.delete(`${ENDPOINTS.PRODUCT_MASTER}/${entityType}/${id}`);
  }
};
