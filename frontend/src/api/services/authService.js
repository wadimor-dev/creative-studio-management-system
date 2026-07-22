import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const authService = {
  login: (credentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    return apiClient.post(ENDPOINTS.AUTH.LOGIN, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },

  getProfile: () => {
    return apiClient.get(ENDPOINTS.AUTH.PROFILE);
  },

  logout: () => {
    return apiClient.post('/auth/logout');
  }
};
