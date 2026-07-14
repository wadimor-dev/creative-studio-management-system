import { useState, useEffect } from 'react';
import { dashboardService } from '../api/services/dashboardService';
import { toastError } from '../utils/toast';
import { useAuth } from '../contexts/AuthContext';
import { hasPermission } from '../utils/permissions';

export const useDashboard = (days = 7) => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await dashboardService.getMetrics(days);
      if (res.success) {
        setMetrics(res.data);
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
  };

  useEffect(() => {

      if (!hasPermission(user, 'DASHBOARD')) {
          setLoading(false);
          return;
      }

      fetchDashboardData();

}, [days, user]);
  return { metrics, loading, error, refetch: fetchDashboardData };
};
