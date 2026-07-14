import { useState, useEffect, useCallback } from 'react';
import { productMasterService } from '../api/services/productMasterService';
import { toastError } from '../utils/toast';

export const useProductMaster = (entityType) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!entityType) return;
    setLoading(true);
    setError(null);
    try {
      const res = await productMasterService.getAll(entityType);
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
  }, [entityType]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
};
