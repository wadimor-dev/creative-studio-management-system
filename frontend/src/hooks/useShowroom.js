import { useState, useEffect, useCallback } from 'react';
import { showroomService } from '../api/services/showroomService';
import { toastError } from '../utils/toast';
import { useAuth } from '../contexts/AuthContext';
import { hasPermission } from '../utils/permissions';

export const useShowroomDashboard = () => {
  const [stats, setStats] = useState(null);
  const [movements, setMovements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, movementsRes] = await Promise.all([
        showroomService.getDashboardStats(),
        showroomService.getRecentMovements({ limit: 5 }),
      ]);

      if (statsRes.success) {
        setStats(statsRes.data);
      }
      if (movementsRes.success) {
        setMovements(movementsRes.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      // Use mock data as fallback when API fails
      setStats({
        totalStock: '1,245',
        stockInToday: '+120',
        stockOutToday: '-45',
        pendingTransfer: '8',
        stockInCount: '5 transaksi',
        stockOutCount: '3 transaksi',
        inTransit: '2 dalam perjalanan',
      });
      setMovements([
        { id: 'MOV-001', product: 'Kain Batik Motif X', type: 'IN', quantity: 50, location: 'Showroom Utama', status: 'completed' },
        { id: 'MOV-002', product: 'Kain Tenun Ikat', type: 'OUT', quantity: 20, location: 'Showroom Utama', status: 'completed' },
        { id: 'MOV-003', product: 'Songket Palembang', type: 'TRANSFER', quantity: 15, location: 'Cabang A', status: 'in_transit' },
        { id: 'MOV-004', product: 'Ulos Batak', type: 'IN', quantity: 30, location: 'Showroom Utama', status: 'completed' },
      ]);
      // Only show toast for non-404 errors
      if (err.response?.status !== 404) {
        toastError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) {
      return;
    }
    fetchDashboard();
  }, [user, fetchDashboard]);

  return { stats, movements, loading, error, refetch: fetchDashboard };
};

export const useShowroomStock = (filters = {}) => {
  const [stats, setStats] = useState(null);
  const [movements, setMovements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchStockData = useCallback(async (params = filters) => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, movementsRes] = await Promise.all([
        showroomService.getStockStats(params),
        showroomService.getStockMovements(params),
      ]);

      if (statsRes.success) {
        setStats(statsRes.data);
      }
      if (movementsRes.success) {
        setMovements(movementsRes.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      // Use mock data as fallback when API fails
      setStats({
        totalStock: '1,245',
        stockInToday: '+120',
        stockOutToday: '-45',
        pendingTransfer: '8',
        stockInCount: '5 transaksi',
        stockOutCount: '3 transaksi',
        inTransit: '2 dalam perjalanan',
      });
      setMovements([
        { id: 'MOV-001', product: { sku: 'SKU-001', name: 'Kain Batik Motif X' }, type: 'IN', quantity: 50, location: 'Showroom Utama', date: '2026-07-17', status: 'completed', reference: 'PO-1234' },
        { id: 'MOV-002', product: { sku: 'SKU-002', name: 'Kain Tenun Ikat' }, type: 'OUT', quantity: 20, location: 'Showroom Utama', date: '2026-07-17', status: 'completed', reference: 'SO-5678' },
        { id: 'MOV-003', product: { sku: 'SKU-003', name: 'Songket Palembang' }, type: 'TRANSFER', quantity: 15, location: 'Cabang A', date: '2026-07-16', status: 'in_transit', reference: 'TRF-001' },
        { id: 'MOV-004', product: { sku: 'SKU-004', name: 'Ulos Batak' }, type: 'IN', quantity: 30, location: 'Showroom Utama', date: '2026-07-16', status: 'completed', reference: 'PO-1235' },
        { id: 'MOV-005', product: { sku: 'SKU-005', name: 'Batik Tulis Solo' }, type: 'OUT', quantity: 10, location: 'Cabang B', date: '2026-07-15', status: 'completed', reference: 'SO-5679' },
      ]);
      if (err.response?.status !== 404) {
        toastError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) {
      return;
    }
    fetchStockData(filters);
  }, [user, fetchStockData, JSON.stringify(filters)]);

  return { stats, movements, loading, error, refetch: fetchStockData };
};

export const useShowroomTransfers = (filters = {}) => {
  const [stats, setStats] = useState(null);
  const [transfers, setTransfers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchTransfers = useCallback(async (params = filters) => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, transfersRes] = await Promise.all([
        showroomService.getTransferStats(),
        showroomService.getTransfers(params),
      ]);

      if (statsRes.success) {
        setStats(statsRes.data);
      }
      if (transfersRes.success) {
        setTransfers(transfersRes.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      // Use mock data as fallback when API fails
      setStats({
        pendingTransfer: '5',
        inTransit: '3',
        completedToday: '8',
        totalThisMonth: '42',
      });
      setTransfers([
        { id: 'TRF-001', fromLocation: 'Showroom Utama', toLocation: 'Cabang A', items: [{ product: 'Kain Batik Motif X', quantity: 20 }], totalQuantity: 20, status: 'pending', createdAt: '2026-07-17', estimatedArrival: '2026-07-18' },
        { id: 'TRF-002', fromLocation: 'Gudang', toLocation: 'Showroom Utama', items: [{ product: 'Songket Palembang', quantity: 10 }], totalQuantity: 10, status: 'in_transit', createdAt: '2026-07-16', estimatedArrival: '2026-07-17' },
        { id: 'TRF-003', fromLocation: 'Cabang B', toLocation: 'Showroom Utama', items: [{ product: 'Ulos Batak', quantity: 25 }], totalQuantity: 25, status: 'completed', createdAt: '2026-07-15', estimatedArrival: '2026-07-15' },
        { id: 'TRF-004', fromLocation: 'Showroom Utama', toLocation: 'Cabang A', items: [{ product: 'Batik Tulis Solo', quantity: 30 }], totalQuantity: 30, status: 'cancelled', createdAt: '2026-07-14', estimatedArrival: '2026-07-15' },
        { id: 'TRF-005', fromLocation: 'Gudang', toLocation: 'Cabang B', items: [{ product: 'Kain Batik Motif Y', quantity: 50 }], totalQuantity: 50, status: 'completed', createdAt: '2026-07-13', estimatedArrival: '2026-07-14' },
      ]);
      if (err.response?.status !== 404) {
        toastError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) {
      return;
    }
    fetchTransfers(filters);
  }, [user, fetchTransfers, JSON.stringify(filters)]);

  const createTransfer = useCallback(async (data) => {
    try {
      const res = await showroomService.createTransfer(data);
      if (res.success) {
        await fetchTransfers(filters);
        return res;
      }
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      toastError(msg);
      throw err;
    }
  }, [fetchTransfers, filters]);

  const cancelTransfer = useCallback(async (id) => {
    try {
      const res = await showroomService.cancelTransfer(id);
      if (res.success) {
        await fetchTransfers(filters);
        return res;
      }
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      toastError(msg);
      throw err;
    }
  }, [fetchTransfers, filters]);

  const confirmReceipt = useCallback(async (id) => {
    try {
      const res = await showroomService.confirmTransferReceipt(id);
      if (res.success) {
        await fetchTransfers(filters);
        return res;
      }
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      toastError(msg);
      throw err;
    }
  }, [fetchTransfers, filters]);

  return { 
    stats, 
    transfers, 
    loading, 
    error, 
    refetch: fetchTransfers,
    createTransfer,
    cancelTransfer,
    confirmReceipt,
  };
};

export const useShowroomStockIn = (filters = {}) => {
  const [stats, setStats] = useState(null);
  const [stockIn, setStockIn] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchStockIn = useCallback(async (params = filters) => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, stockInRes] = await Promise.all([
        showroomService.getStockInStats(),
        showroomService.getStockIn(params),
      ]);

      if (statsRes.success) {
        setStats(statsRes.data);
      }
      if (stockInRes.success) {
        setStockIn(stockInRes.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      // Use mock data as fallback when API fails
      setStats({
        todayIn: '120',
        thisWeek: '450',
        thisMonth: '1,890',
        totalSuppliers: '15',
      });
      setStockIn([
        { id: 'IN-001', product: { sku: 'SKU-001', name: 'Kain Batik Motif X' }, quantity: 50, supplier: 'PT Batik Jaya', location: 'Showroom Utama', date: '2026-07-17', status: 'completed', reference: 'PO-1234', notes: 'Stok baru untuk koleksi musim ini' },
        { id: 'IN-002', product: { sku: 'SKU-002', name: 'Kain Tenun Ikat' }, quantity: 30, supplier: 'CV Tenun Nusantara', location: 'Showroom Utama', date: '2026-07-17', status: 'completed', reference: 'PO-1235', notes: 'Restock item terlaris' },
        { id: 'IN-003', product: { sku: 'SKU-003', name: 'Songket Palembang' }, quantity: 20, supplier: 'UD Songket Asli', location: 'Cabang A', date: '2026-07-16', status: 'completed', reference: 'PO-1236', notes: '' },
        { id: 'IN-004', product: { sku: 'SKU-004', name: 'Ulos Batak' }, quantity: 25, supplier: 'Kerajinan Batak', location: 'Gudang', date: '2026-07-16', status: 'pending', reference: 'PO-1237', notes: 'Menunggu verifikasi kualitas' },
        { id: 'IN-005', product: { sku: 'SKU-005', name: 'Batik Tulis Solo' }, quantity: 15, supplier: 'Seni Batik Solo', location: 'Showroom Utama', date: '2026-07-15', status: 'completed', reference: 'PO-1238', notes: 'Koleksi premium' },
      ]);
      if (err.response?.status !== 404) {
        toastError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) {
      return;
    }
    fetchStockIn(filters);
  }, [user, fetchStockIn, JSON.stringify(filters)]);

  const createStockIn = useCallback(async (data) => {
    try {
      const res = await showroomService.createStockIn(data);
      if (res.success) {
        await fetchStockIn(filters);
        return res;
      }
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      toastError(msg);
      throw err;
    }
  }, [fetchStockIn, filters]);

  return { 
    stats, 
    stockIn, 
    loading, 
    error, 
    refetch: fetchStockIn,
    createStockIn,
  };
};

export const useShowroomStockOut = (filters = {}) => {
  const [stats, setStats] = useState(null);
  const [stockOut, setStockOut] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchStockOut = useCallback(async (params = filters) => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, stockOutRes] = await Promise.all([
        showroomService.getStockOutStats(),
        showroomService.getStockOut(params),
      ]);

      if (statsRes.success) {
        setStats(statsRes.data);
      }
      if (stockOutRes.success) {
        setStockOut(stockOutRes.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      // Use mock data as fallback when API fails
      setStats({
        todayOut: '45',
        thisWeek: '180',
        thisMonth: '720',
        totalCustomers: '28',
      });
      setStockOut([
        { id: 'OUT-001', product: { sku: 'SKU-001', name: 'Kain Batik Motif X' }, quantity: 20, customer: 'Toko Kain Barokah', location: 'Showroom Utama', date: '2026-07-17', status: 'completed', reference: 'SO-5678', reason: 'Penjualan regular', notes: 'Customer VIP' },
        { id: 'OUT-002', product: { sku: 'SKU-002', name: 'Kain Tenun Ikat' }, quantity: 15, customer: 'Hj. Siti Aminah', location: 'Showroom Utama', date: '2026-07-17', status: 'completed', reference: 'SO-5679', reason: 'Penjualan regular', notes: '' },
        { id: 'OUT-003', product: { sku: 'SKU-003', name: 'Songket Palembang' }, quantity: 10, customer: 'CV Wastra Nusantara', location: 'Cabang A', date: '2026-07-16', status: 'completed', reference: 'SO-5680', reason: 'Pesanan khusus', notes: 'Untuk event' },
        { id: 'OUT-004', product: { sku: 'SKU-004', name: 'Ulos Batak' }, quantity: 5, customer: 'Bapak Budi Santoso', location: 'Gudang', date: '2026-07-16', status: 'pending', reference: 'SO-5681', reason: 'Penjualan regular', notes: 'Menunggu pembayaran' },
        { id: 'OUT-005', product: { sku: 'SKU-005', name: 'Batik Tulis Solo' }, quantity: 8, customer: 'Ibu Ratna Sari', location: 'Showroom Utama', date: '2026-07-15', status: 'completed', reference: 'SO-5682', reason: 'Penjualan regular', notes: 'Koleksi pribadi' },
      ]);
      if (err.response?.status !== 404) {
        toastError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) {
      return;
    }
    fetchStockOut(filters);
  }, [user, fetchStockOut, JSON.stringify(filters)]);

  const createStockOut = useCallback(async (data) => {
    try {
      const res = await showroomService.createStockOut(data);
      if (res.success) {
        await fetchStockOut(filters);
        return res;
      }
      throw new Error(res.message);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      toastError(msg);
      throw err;
    }
  }, [fetchStockOut, filters]);

  return { 
    stats, 
    stockOut, 
    loading, 
    error, 
    refetch: fetchStockOut,
    createStockOut,
  };
};

export const useShowroomLocations = () => {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetchLocations = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await showroomService.getLocations();
      if (res.success) {
        setLocations(res.data);
      }
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      // Use mock data as fallback when API fails
      setLocations([
        { id: 'showroom-utama', name: 'Showroom Utama' },
        { id: 'cabang-a', name: 'Cabang A' },
        { id: 'cabang-b', name: 'Cabang B' },
        { id: 'gudang', name: 'Gudang' },
      ]);
      if (err.response?.status !== 404) {
        toastError(msg);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) {
      return;
    }
    fetchLocations();
  }, [user, fetchLocations]);

  return { locations, loading, error, refetch: fetchLocations };
};
