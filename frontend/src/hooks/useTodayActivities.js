import { useState, useCallback, useEffect } from 'react';
import workActivityService from '../services/workActivityService';

export const useTodayActivities = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTodayActivities = useCallback(async () => {
    setLoading(true);
    try {
      const data = await workActivityService.getTodayActivities();
      setActivities(data?.data ?? data ?? []);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch today activities');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTodayActivities();
  }, [fetchTodayActivities]);

  return { activities, loading, error, refetch: fetchTodayActivities };
};
