import { useState, useEffect, useCallback } from 'react';
import { inventoryService } from '../api/services/inventoryService';
import { toastError } from '../utils/toast';
import { useAuth } from '../contexts/AuthContext';
import { hasPermission } from '../utils/permissions';

export const useInventory = (type = 'items', filters = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchData = useCallback(async (params = filters) => {
    setLoading(true);
    setError(null);
    try {
      let res;
      if (type === 'items') {
        res = await inventoryService.getItems(params);
      } else {
        res = await inventoryService.getTransactions(params);
      }
      
      if (res.success) {
        setData(res.data);
      } else {
        throw new Error(res.message);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      toastError(msg);
    } finally {
      setLoading(false);
    }
  }, [type]);

  useEffect(() => {

    if (!hasPermission(user, 'INVENTORY')) {
        return;
    }

    fetchData(filters);

  }, [user, fetchData, JSON.stringify(filters)]);

  return { data, loading, error, refetch: fetchData };
};
