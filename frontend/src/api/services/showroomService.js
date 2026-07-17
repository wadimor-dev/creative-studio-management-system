import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const showroomService = {
  // Dashboard
  getDashboardStats: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM.DASHBOARD);
  },
  
  getRecentMovements: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.MOVEMENTS, { params });
  },

  // Stock
  getStockStats: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.STOCK, { params });
  },
  
  getStockMovements: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.MOVEMENTS, { params });
  },

  // Transfers
  getTransfers: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.TRANSFERS, { params });
  },
  
  getTransferStats: () => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM.TRANSFERS}/stats`);
  },
  
  createTransfer: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM.TRANSFERS, data);
  },
  
  updateTransfer: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM.TRANSFERS}/${id}`, data);
  },
  
  cancelTransfer: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM.TRANSFERS}/${id}/cancel`);
  },
  
  confirmTransferReceipt: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM.TRANSFERS}/${id}/confirm`);
  },

  // Stock In
  getStockIn: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.STOCK_IN, { params });
  },
  
  getStockInStats: () => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM.STOCK_IN}/stats`);
  },
  
  createStockIn: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM.STOCK_IN, data);
  },
  
  updateStockIn: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM.STOCK_IN}/${id}`, data);
  },

  // Stock Out
  getStockOut: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.STOCK_OUT, { params });
  },
  
  getStockOutStats: () => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM.STOCK_OUT}/stats`);
  },
  
  createStockOut: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM.STOCK_OUT, data);
  },
  
  updateStockOut: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM.STOCK_OUT}/${id}`, data);
  },

  // Locations
  getLocations: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM.LOCATIONS);
  },
};
