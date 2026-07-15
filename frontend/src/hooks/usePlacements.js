import { useState, useEffect, useCallback } from 'react';
import { placementService } from '../api/services/placementService';

export const usePlacements = (fetchHierarchy = false) => {
  const [placements, setPlacements] = useState([]);
  const [types, setTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [placementsRes, typesRes] = await Promise.all([
        fetchHierarchy ? placementService.getHierarchy() : placementService.getAll(),
        placementService.getTypes()
      ]);
      setPlacements(placementsRes.data || []);
      setTypes(typesRes.data || []);
      setError(null);
    } catch (err) {
      setError(err);
      setPlacements([]);
      setTypes([]);
    } finally {
      setLoading(false);
    }
  }, [fetchHierarchy]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { placements, types, loading, error, refetch: fetchData };
};
