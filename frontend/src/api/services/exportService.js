import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const exportService = {
  exportProductMovementsExcel: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/product-movements/excel`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportProductMovementsPdf: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/product-movements/pdf`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportReportsExcel: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/reports/excel`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportReportsPdf: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/reports/pdf`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportItemsExcel: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/items/excel`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportItemsPdf: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/items/pdf`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportInventoryTransactionsExcel: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/inventory-transactions/excel`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  },
  exportInventoryTransactionsPdf: async (params) => {
    const response = await apiClient.post(`${ENDPOINTS.EXPORT}/inventory-transactions/pdf`, {}, {
      params,
      responseType: 'blob'
    });
    return response;
  }
};
