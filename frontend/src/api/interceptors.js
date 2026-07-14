import { toastError } from '../utils/toast';

export const setupInterceptors = (axiosInstance) => {
  // Request Interceptor
  axiosInstance.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      
      // Set Content-Type for JSON requests if not already set and data is an object
      if (!config.headers['Content-Type'] && config.data && !(config.data instanceof URLSearchParams)) {
        config.headers['Content-Type'] = 'application/json';
      }
      
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response Interceptor
  axiosInstance.interceptors.response.use(
    (response) => {
      // Return the complete data payload conforming to the API contract
      return response.data;
    },
    async (error) => {
      const originalRequest = error.config;
      
      // Handle 401 Unauthorized (Token Expiration)
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        
        try {
          // Attempt refresh logic here if endpoint exists, otherwise logout
          // For now, if 401 occurs, we forcefully clear auth
          localStorage.removeItem('token');
          window.location.href = '/login';
          return Promise.reject(error);
        } catch (refreshError) {
          return Promise.reject(refreshError);
        }
      }

      // Format standard error message
      const errorMessage = error.response?.data?.message || error.message || 'An unexpected error occurred';
      toastError(errorMessage);

      return Promise.reject(error);
    }
  );
};
