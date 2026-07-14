import { useState } from 'react';
import { userService } from '../api/services/userService';
import { toastError } from '../utils/toast';
import { useAuth } from '../contexts/AuthContext';

export const useProfile = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const updateProfile = async (data) => {
    setLoading(true);
    setError(null);
    try {
      const res = await userService.updateProfile(data);
      if (res.success) {
        // Technically auth context should refetch me() to update global user state
        // This will be handled by the component or we can return true
        return true;
      }
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      toastError(msg);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const changePassword = async (data) => {
    setLoading(true);
    setError(null);
    try {
      const res = await userService.changePassword(data);
      if (res.success) return true;
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      toastError(msg);
      return false;
    } finally {
      setLoading(false);
    }
  };

  return { user, updateProfile, changePassword, loading, error };
};
