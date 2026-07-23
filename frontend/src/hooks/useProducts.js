import { useState, useEffect, useCallback } from 'react';
import { productService } from '../api/services/productService';
import { toastError } from '../utils/toast';

export const useProducts = (filters = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (currentFilters = filters) => {
    setLoading(true);
    setError(null);
    try {
      const res = await productService.getAll({ ...currentFilters, page: 1, size: 0 });
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
  }, []);

  useEffect(() => {
    fetchData(filters);
  }, [fetchData, JSON.stringify(filters)]);

  return { data, loading, error, refetch: fetchData };
};
