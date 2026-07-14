import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const inventoryService = {
  getItems: (params) => {
    return apiClient.get(ENDPOINTS.INVENTORY.ITEMS, { params });
  },
  
  createItem: (data) => {
    return apiClient.post(ENDPOINTS.INVENTORY.ITEMS, data);
  },
  
  updateItem: (id, data) => {
    return apiClient.put(`${ENDPOINTS.INVENTORY.ITEMS}/${id}`, data);
  },
  
  deleteItem: (id) => {
    return apiClient.delete(`${ENDPOINTS.INVENTORY.ITEMS}/${id}`);
  },
  
  getTransactions: (params) => {
    return apiClient.get(ENDPOINTS.INVENTORY.TRANSACTIONS, { params });
  },
  
  createTransaction: (data) => {
    return apiClient.post(ENDPOINTS.INVENTORY.TRANSACTIONS, data);
  }
};
