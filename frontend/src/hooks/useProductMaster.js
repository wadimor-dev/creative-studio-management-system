import { useState, useEffect, useCallback } from 'react';
import { productMasterService } from '../api/services/productMasterService';
import { toastError } from '../utils/toast';

export const useProductMaster = (entityType, { paginated = true } = {}) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [size, setSize] = useState(10);

  const fetchData = useCallback(async (p, s) => {
    if (!entityType) return;
    setLoading(true);
    setError(null);
    try {
      const res = paginated
        ? await productMasterService.getAll(entityType, { page: p, size: s })
        : await productMasterService.getAllDropdown(entityType);
      if (res.success || res.data) {
        const items = res.data || [];
        setData(Array.isArray(items) ? items : []);
        setTotal(res.meta?.total || items.length || 0);
        if (paginated) {
          setPage(res.meta?.page || p);
          setSize(res.meta?.size || s);
        }
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
  }, [entityType, paginated]);

  useEffect(() => {
    if (paginated) setPage(1);
  }, [entityType, paginated]);

  useEffect(() => {
    fetchData(page, size);
  }, [fetchData, page, size]);

  const goToPage = (newPage) => { if (paginated) setPage(newPage); };
  const changeSize = (newSize) => { if (paginated) { setSize(newSize); setPage(1); } };

  return { data, loading, error, refetch: () => fetchData(page, size), page, size, total, goToPage, changeSize };
};
