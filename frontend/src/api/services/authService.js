import apiClient from '../axios';
import { ENDPOINTS } from '../endpoints';

export const authService = {
  login: (credentials) => {
    // FastAPI OAuth2PasswordRequestForm expects form data with 'username' and 'password'
    const formData = new URLSearchParams();
    formData.append('username', credentials.email); // using email as username
    formData.append('password', credentials.password);
    
    return apiClient.post(ENDPOINTS.AUTH.LOGIN, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
  },
  
  getProfile: () => {
    return apiClient.get(ENDPOINTS.AUTH.PROFILE);
  }
};
