import { useState, useEffect, useCallback } from 'react';
import { productMovementService } from '../api/services/productMovementService';
import { toastError } from '../utils/toast';

export const useProductMovements = (filters = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await productMovementService.getAll(filters);
      if (res.success) {
        setData(res.data);
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    } finally {
      setLoading(false);
    }
  }, [JSON.stringify(filters)]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, refetch: fetchData };
};
