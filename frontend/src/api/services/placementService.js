import api from '../axios';

export const placementService = {
  getAll: async () => {
    const response = await api.get('/product-placements');
    return response;
  },

  getHierarchy: async () => {
    const response = await api.get('/product-placements/hierarchy');
    return response;
  },

  getTypes: async () => {
    const response = await api.get('/product-placements/types');
    return response;
  },

  create: async (data) => {
    const response = await api.post('/product-placements', data);
    return response;
  },

  update: async (id, data) => {
    const response = await api.put(`/product-placements/${id}`, data);
    return response;
  },

  delete: async (id) => {
    const response = await api.delete(`/product-placements/${id}`);
    return response;
  },
  
  createType: async (data) => {
    const response = await api.post('/product-placements/types', data);
    return response;
  },
  
  updateType: async (id, data) => {
    const response = await api.put(`/product-placements/types/${id}`, data);
    return response;
  }
};
