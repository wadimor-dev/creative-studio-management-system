import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const productMovementService = {
  getAll: (params) => apiClient.get(ENDPOINTS.PRODUCT_MOVEMENTS, { params }),
  create: (data) => apiClient.post(ENDPOINTS.PRODUCT_MOVEMENTS, data),
};

export const productStockService = {
  getAll: (params) => apiClient.get(ENDPOINTS.PRODUCT_STOCKS, { params }),
  performOpname: (data) => apiClient.post(`${ENDPOINTS.PRODUCT_STOCKS}/opname`, data),
};
