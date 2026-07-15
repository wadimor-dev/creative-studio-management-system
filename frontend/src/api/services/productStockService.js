import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const productStockService = {
  getAll: (params) => {
    return apiClient.get(ENDPOINTS.PRODUCT_STOCKS, { params });
  }
};
