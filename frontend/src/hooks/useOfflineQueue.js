import { useState, useCallback, useEffect, useRef } from 'react';

const STORAGE_KEY = 'csms_offline_queue';
const MAX_RETRY = 5;
const BASE_DELAY_MS = 1000;

const loadQueue = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
};

const saveQueue = (queue) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(queue));
  } catch {}
};

export const useOfflineQueue = () => {
  const [queue, setQueue] = useState(loadQueue);
  const [isSyncing, setIsSyncing] = useState(false);
  const timerRef = useRef(null);

  useEffect(() => { saveQueue(queue); }, [queue]);

  const enqueue = useCallback((item) => {
    const entry = {
      id: `${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      ...item,
      status: 'PENDING',
      retry_count: 0,
      max_retry: MAX_RETRY,
      created_at: new Date().toISOString(),
      last_error: null,
    };
    setQueue((prev) => [...prev, entry]);
    return entry.id;
  }, []);

  const remove = useCallback((id) => {
    setQueue((prev) => prev.filter((q) => q.id !== id));
  }, []);

  const updateStatus = useCallback((id, status, error = null) => {
    setQueue((prev) =>
      prev.map((q) =>
        q.id === id
          ? { ...q, status, last_error: error, retry_count: q.retry_count + 1 }
          : q
      )
    );
  }, []);

  const processQueue = useCallback(async () => {
    if (isSyncing) return;
    const pending = queue.filter((q) => q.status === 'PENDING' && q.retry_count < q.max_retry);
    if (pending.length === 0) return;

    setIsSyncing(true);
    for (const item of pending) {
      if (!navigator.onLine) break;

      updateStatus(item.id, 'SYNCING');
      try {
        const response = await fetch(item.url, {
          method: item.method || 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(item.headers || {}),
          },
          body: JSON.stringify(item.body),
        });

        if (response.ok) {
          updateStatus(item.id, 'SUCCESS');
        } else if (response.status === 409) {
          updateStatus(item.id, 'CONFLICT', `HTTP ${response.status}`);
        } else {
          updateStatus(item.id, 'PENDING', `HTTP ${response.status}`);
        }
      } catch (err) {
        updateStatus(item.id, 'PENDING', err.message);
      }
    }
    setIsSyncing(false);
  }, [queue, isSyncing, updateStatus]);

  const retry = useCallback((id) => {
    setQueue((prev) =>
      prev.map((q) =>
        q.id === id ? { ...q, status: 'PENDING', last_error: null } : q
      )
    );
  }, []);

  const clearCompleted = useCallback(() => {
    setQueue((prev) => prev.filter((q) => q.status !== 'SUCCESS'));
  }, []);

  useEffect(() => {
    const handleOnline = () => { processQueue(); };
    window.addEventListener('online', handleOnline);
    return () => window.removeEventListener('online', handleOnline);
  }, [processQueue]);

  useEffect(() => {
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, []);

  const pendingCount = queue.filter((q) => q.status === 'PENDING').length;
  const failedCount = queue.filter((q) => q.status === 'FAILED' || q.status === 'CONFLICT').length;

  return {
    queue,
    enqueue,
    remove,
    retry,
    clearCompleted,
    processQueue,
    isSyncing,
    pendingCount,
    failedCount,
  };
};
