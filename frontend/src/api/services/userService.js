import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const userService = {
  getUsers: (params) => {
    return apiClient.get(ENDPOINTS.USERS.LIST, { params });
  },
  
  createUser: (data) => {
    return apiClient.post(ENDPOINTS.USERS.LIST, data);
  },
  
  updateUser: (id, data) => {
    return apiClient.put(`${ENDPOINTS.USERS.LIST}/${id}`, data);
  },
  
  deleteUser: (id) => {
    return apiClient.delete(`${ENDPOINTS.USERS.LIST}/${id}`);
  },
  
  updateProfile: (data) => {
    // using generic users profile endpoint, or could be /auth/profile
    return apiClient.put(ENDPOINTS.USERS.PROFILE, data);
  },
  
  changePassword: (data) => {
    return apiClient.put(`${ENDPOINTS.USERS.PROFILE}/password`, data);
  }
};
