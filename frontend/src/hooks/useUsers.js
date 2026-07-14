import { useState, useEffect, useCallback } from 'react';
import { userService } from '../api/services/userService';
import { toastError } from '../utils/toast';

export const useUsers = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUsers = useCallback(async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const res = await userService.getUsers(params);
      if (res.status === 'success' || res.data) {
        setUsers(res.data || []);
      } else {
        throw new Error(res.message || "Failed to fetch users");
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      toastError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  return { users, loading, error, refetch: fetchUsers };
};
