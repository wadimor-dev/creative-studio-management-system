import { useState, useEffect, useCallback } from 'react';
import { reportService } from '../api/services/reportService';
import { toastError } from '../utils/toast';

export const useReports = () => {
  const [data, setData] = useState({ summary: null, items: [], total: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async (params = {}) => {
    setLoading(true);
    setError(null);
    try {
      const res = await reportService.getReports(params);
      if (res.success) {
        setData(res.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      toastError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, refetch: fetchData };
};
