import api from '../axios';

export const scannerService = {
  resolvePlacement: async (placementCode) => {
    const response = await api.get(`/product-scanner/${placementCode}`);
    return response;
  },

  // This just wraps the movement API for convenience from the scanner
  executeMovement: async (data) => {
    const response = await api.post('/product-movements', data);
    return response;
  },
  
  executeOpname: async (data) => {
    const response = await api.post('/product-opname', data);
    return response;
  }
};
