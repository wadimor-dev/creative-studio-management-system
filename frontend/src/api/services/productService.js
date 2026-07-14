import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const productService = {
  getAll: (params) => {
    return apiClient.get(ENDPOINTS.PRODUCTS, { params });
  },
  
  create: (data) => {
    return apiClient.post(ENDPOINTS.PRODUCTS, data);
  },
  
  update: (id, data) => {
    return apiClient.put(`${ENDPOINTS.PRODUCTS}/${id}`, data);
  },
  
  delete: (id) => {
    return apiClient.delete(`${ENDPOINTS.PRODUCTS}/${id}`);
  }
};
