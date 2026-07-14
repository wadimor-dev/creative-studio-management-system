import { useState, useCallback, useEffect } from 'react';
import workActivityService from '../services/workActivityService';

export const useCurrentActivity = () => {
  const [currentActivity, setCurrentActivity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCurrentActivity = useCallback(async () => {
    setLoading(true);
    try {
      const data = await workActivityService.getCurrentActivity();
      setCurrentActivity(data?.data ?? data ?? null);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch current activity');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCurrentActivity();
  }, [fetchCurrentActivity]);

  return { currentActivity, loading, error, refetch: fetchCurrentActivity };
};
