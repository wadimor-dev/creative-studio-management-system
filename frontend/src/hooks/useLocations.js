import { useState, useEffect } from 'react';
import { locationService } from '../api/services/locationService';
import { toastError } from '../utils/toast';

export const useLocations = () => {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchLocations = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await locationService.getAll();
      if (res.success) {
        setLocations(res.data);
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
    fetchLocations();
  }, []);

  return { locations, loading, error, refetch: fetchLocations };
};
