import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const showroomService = {
  // Legacy Dashboard
  getDashboardStats: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM.DASHBOARD);
  },
  
  getRecentMovements: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.MOVEMENTS, { params });
  },

  // Legacy Stock
  getStockStats: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.STOCK, { params });
  },
  
  getStockMovements: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM.MOVEMENTS, { params });
  },

  // Legacy Transfers
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

  // Legacy Stock In
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

  // Legacy Stock Out
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

  // Products (for SearchableSelect)
  getProducts: (params) => {
    return apiClient.get(ENDPOINTS.PRODUCTS, { params });
  },

  // ==================== SHOWROOM V2 ====================

  // Dashboard KPI
  getDashboardKPI: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD);
  },

  getBorrowingStats: () => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.DASHBOARD}/borrowing-stats`);
  },

  getGuestStats: () => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.DASHBOARD}/guest-stats`);
  },

  getOverdueBorrowings: () => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.DASHBOARD}/overdue-borrowings`);
  },

  // Sample Management
  getStockSummary: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.SAMPLES.STOCK, { params });
  },

  getProductStock: (productId) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.SAMPLES.STOCK}/${productId}`);
  },

  handoverFromInventory: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.SAMPLES.HANDOVER, data);
  },

  transferStock: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.SAMPLES.TRANSFER, data);
  },

  borrowSample: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.SAMPLES.BORROW, data);
  },

  returnSample: (borrowingId, data) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.SAMPLES.RETURN}/${borrowingId}`, data);
  },

  adjustStock: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.SAMPLES.ADJUST, data);
  },

  getLocations: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.SAMPLES.LOCATIONS);
  },

  // Borrowings
  getBorrowings: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.BORROWINGS, { params });
  },

  getBorrowing: (id) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.BORROWINGS}/${id}`);
  },

  approveBorrowing: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.BORROWINGS}/${id}/approve`);
  },

  extendBorrowing: (id, data) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.BORROWINGS}/${id}/extend`, data);
  },

  cancelBorrowing: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.BORROWINGS}/${id}/cancel`);
  },

  // Guest Releases
  getGuestReleases: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.GUESTS, { params });
  },

  getGuestRelease: (id) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.GUESTS}/${id}`);
  },

  createGuestRelease: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.GUESTS, data);
  },

  approveGuestRelease: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.GUESTS}/${id}/approve`);
  },

  returnFromGuest: (id, data) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.GUESTS}/${id}/return`, data);
  },

  // Stock Control - Opname
  getOpnameSessions: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.OPNAME);
  },

  createOpnameSession: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.OPNAME, data);
  },

  addOpnameItem: (sessionId, data) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.OPNAME}/${sessionId}/items`, data);
  },

  completeOpname: (sessionId) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.OPNAME}/${sessionId}/complete`);
  },

  approveOpname: (sessionId) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.OPNAME}/${sessionId}/approve`);
  },

  // Stock Control - Restock
  getRestockRequests: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.RESTOCK, { params });
  },

  createRestockRequest: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.RESTOCK, data);
  },

  approveRestock: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.RESTOCK}/${id}/approve`);
  },

  // Stock Control - Maintenance
  getMaintenance: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.MAINTENANCE, { params });
  },

  createMaintenance: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.MAINTENANCE, data);
  },

  // Stock Control - Reservations
  getReservations: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.RESERVATIONS, { params });
  },

  createReservation: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.RESERVATIONS, data);
  },

  // Reports
  getKPI: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.REPORTS.KPI);
  },

  getMovementSummary: (days) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.REPORTS.MOVEMENT_SUMMARY, { params: { days } });
  },

  getStockByLocation: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.REPORTS.STOCK_BY_LOCATION);
  },

  getProductHistory: (productId, limit) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.REPORTS.PRODUCT_HISTORY}/${productId}`, { params: { limit } });
  },

  getBorrowingSummary: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.REPORTS.BORROWING_SUMMARY);
  },

  getGuestSummary: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.REPORTS.GUEST_SUMMARY);
  },

  // Sample Movements
  getMovements: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.SAMPLES_MOVEMENTS, { params });
  },

  // Master Data
  getMasterData: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.MASTER_DATA, { params });
  },

  createMasterData: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.MASTER_DATA, data);
  },

  updateMasterData: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM_V2.MASTER_DATA}/${id}`, data);
  },

  deleteMasterData: (id) => {
    return apiClient.delete(`${ENDPOINTS.SHOWROOM_V2.MASTER_DATA}/${id}`);
  },

  seedMasterData: () => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.MASTER_DATA}/seed`);
  },

  rejectGuestRelease: (id, data) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.GUESTS}/${id}/reject`, data);
  },

  completeMaintenance: (id) => {
    return apiClient.post(`${ENDPOINTS.SHOWROOM_V2.STOCK_CONTROL.MAINTENANCE}/${id}/complete`);
  },

  // Location Management
  getAllLocations: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.LOCATIONS_ALL);
  },

  createLocation: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.SAMPLES.LOCATIONS, data);
  },

  updateLocation: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM_V2.SAMPLES.LOCATIONS}/${id}`, data);
  },

  deleteLocation: (id) => {
    return apiClient.delete(`${ENDPOINTS.SHOWROOM_V2.SAMPLES.LOCATIONS}/${id}`);
  },

  // Public scan (no auth required)
  getPublicLocationScan: (code) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.PUBLIC.SCAN}/${code}`);
  },

  getQRCodeUrl: (code) => {
    const baseUrl = import.meta.env.VITE_API_URL || 'https://api-csms.idekode.web.id/api/v1';
    return `${baseUrl}/showroom-v2/public/scan/${code}/qr`;
  },

  // Storage Locations
  getStorageLocations: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STORAGE.BASE, { params });
  },

  getStorages: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STORAGE.BASE, { params });
  },

  getStorageTree: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STORAGE.TREE, { params });
  },

  getStorageById: (id) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.STORAGE.BASE}/${id}`);
  },

  createStorageLocation: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.STORAGE.BASE, data);
  },

  updateStorageLocation: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM_V2.STORAGE.BASE}/${id}`, data);
  },

  deleteStorageLocation: (id) => {
    return apiClient.delete(`${ENDPOINTS.SHOWROOM_V2.STORAGE.BASE}/${id}`);
  },

  // QR Entities
  getQREntities: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.STORAGE.QR, { params });
  },

  getQREntityById: (id) => {
    return apiClient.get(`${ENDPOINTS.SHOWROOM_V2.STORAGE.QR}/${id}`);
  },

  createQREntity: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.STORAGE.QR, data);
  },

  updateQREntity: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM_V2.STORAGE.QR}/${id}`, data);
  },

  deleteQREntity: (id) => {
    return apiClient.delete(`${ENDPOINTS.SHOWROOM_V2.STORAGE.QR}/${id}`);
  },

  // QR Image URL
  getQRImageUrl: (token) => {
    const baseURL = import.meta.env.VITE_API_URL || 'https://api-csms.idekode.web.id/api/v1';
    return `${baseURL}/showroom-v2/public/qr/${token}/image`;
  },

  // QR Scan
  resolveQR: (token) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.QR_SCAN.RESOLVE, { token });
  },

  storageScan: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.QR_SCAN.STORAGE, data);
  },

  productScan: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.QR_SCAN.PRODUCT, data);
  },

  // Dashboard V2
  getDashboardSummary: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.SUMMARY);
  },

  getDashboardMovements: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.MOVEMENTS, { params });
  },

  getHeatmapData: () => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.HEATMAP);
  },

  getMovementTrends: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.TRENDS, { params });
  },

  getTopProducts: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.TOP_PRODUCTS, { params });
  },

  createSnapshot: (params) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.SNAPSHOT, null, { params });
  },

  rebuildSummary: (params) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.REBUILD_SUMMARY, null, { params });
  },

  getSummaryHistory: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.DASHBOARD_V2.SUMMARY_HISTORY, { params });
  },

  // ==================== SHOWROOM MANAGEMENT ====================

  getManageProducts: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.MANAGE.BASE, { params });
  },

  getMovementTypes: async () => {
    const res = await apiClient.get(ENDPOINTS.SHOWROOM_V2.MANAGE.MOVEMENT_TYPES);
    if (res?.data?.length) {
      return { ...res, data: res.data.map(t => ({ value: t.code, label: t.name, direction: t.direction, notes: t.notes })) };
    }
    return res;
  },

  addManageProduct: (params) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.MANAGE.BASE + '/add', null, { params });
  },

  addManageMovement: (params) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.MANAGE.BASE + '/add', null, { params });
  },

  removeManageProduct: (stockId, params) => {
    return apiClient.delete(`${ENDPOINTS.SHOWROOM_V2.MANAGE.BASE}/${stockId}`, { params });
  },

  getManageReport: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.MANAGE.REPORT, { params });
  },

  // ==================== MOVEMENT TYPES CRUD ====================

  listMovementTypes: (params) => {
    return apiClient.get(ENDPOINTS.SHOWROOM_V2.MOVEMENT_TYPES.BASE, { params });
  },

  createMovementType: (data) => {
    return apiClient.post(ENDPOINTS.SHOWROOM_V2.MOVEMENT_TYPES.BASE, data);
  },

  updateMovementType: (id, data) => {
    return apiClient.put(`${ENDPOINTS.SHOWROOM_V2.MOVEMENT_TYPES.BASE}/${id}`, data);
  },

  deleteMovementType: (id) => {
    return apiClient.delete(`${ENDPOINTS.SHOWROOM_V2.MOVEMENT_TYPES.BASE}/${id}`);
  },
};
