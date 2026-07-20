import { useState, useEffect, useCallback } from 'react';
import { showroomService } from '../api/services/showroomService';
import { toastError } from '../utils/toast';
import { useAuth } from '../contexts/AuthContext';
import { hasPermission } from '../utils/permissions';

// ============================================================
// Dashboard KPI
// ============================================================
export const useShowroomDashboardKPI = () => {
  const [kpi, setKpi] = useState(null);
  const [borrowingStats, setBorrowingStats] = useState(null);
  const [guestStats, setGuestStats] = useState(null);
  const [overdueBorrowings, setOverdueBorrowings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [kpiRes, bStats, gStats, overdue] = await Promise.all([
        showroomService.getDashboardKPI(),
        showroomService.getBorrowingStats(),
        showroomService.getGuestStats(),
        showroomService.getOverdueBorrowings(),
      ]);

      if (kpiRes.success) setKpi(kpiRes.data);
      if (bStats.success) setBorrowingStats(bStats.data);
      if (gStats.success) setGuestStats(gStats.data);
      if (overdue.success) setOverdueBorrowings(overdue.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setKpi({
        total_sample: 245,
        at_showroom: 180,
        borrowed: 35,
        released_this_month: 12,
        maintenance: 3,
        retired: 1,
        need_restock: 12,
        overdue_borrowing: 3,
        top_borrowed_product: { id: 1, name: 'Kain Batik Motif X', borrow_count: 5 },
        top_released_product: { id: 2, name: 'Songket Palembang', release_count: 3 },
      });
      setBorrowingStats({ borrowed: 35, overdue: 3, returned_this_month: 18 });
      setGuestStats({ pending_approval: 5, released_this_month: 12, total_guests: 28 });
      setOverdueBorrowings([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch]);

  return { kpi, borrowingStats, guestStats, overdueBorrowings, loading, error, refetch: fetch };
};

// ============================================================
// Sample Stock
// ============================================================
export const useShowroomSampleStock = (locationId = null) => {
  const [stock, setStock] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async (locId = locationId) => {
    setLoading(true);
    setError(null);
    try {
      const params = locId ? { location_id: locId } : {};
      const [stockRes, locRes] = await Promise.all([
        showroomService.getStockSummary(params),
        showroomService.getLocations(),
      ]);
      if (stockRes.success) setStock(stockRes.data);
      if (locRes.success) setLocations(locRes.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setStock([]);
      setLocations([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, [locationId]);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch, locationId]);

  const handover = useCallback(async (data) => {
    try {
      const res = await showroomService.handoverFromInventory(data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const transfer = useCallback(async (data) => {
    try {
      const res = await showroomService.transferStock(data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const adjust = useCallback(async (data) => {
    try {
      const res = await showroomService.adjustStock(data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const borrow = useCallback(async (data) => {
    try {
      const res = await showroomService.borrowSample(data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  return { stock, locations, loading, error, refetch: fetch, handover, transfer, adjust, borrow };
};

// ============================================================
// Borrowings
// ============================================================
export const useShowroomBorrowings = (statusFilter = null) => {
  const [borrowings, setBorrowings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async (status = statusFilter) => {
    setLoading(true);
    setError(null);
    try {
      const params = status && status !== 'all' ? { status } : {};
      const res = await showroomService.getBorrowings(params);
      if (res.success) setBorrowings(res.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setBorrowings([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch, statusFilter]);

  const approve = useCallback(async (id) => {
    try {
      const res = await showroomService.approveBorrowing(id);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const extend = useCallback(async (id, data) => {
    try {
      const res = await showroomService.extendBorrowing(id, data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const cancel = useCallback(async (id) => {
    try {
      const res = await showroomService.cancelBorrowing(id);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const returnSample = useCallback(async (id, data) => {
    try {
      const res = await showroomService.returnSample(id, data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  return { borrowings, loading, error, refetch: fetch, approve, extend, cancel, returnSample };
};

// ============================================================
// Guest Releases
// ============================================================
export const useShowroomGuestReleases = (statusFilter = null) => {
  const [releases, setReleases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async (status = statusFilter) => {
    setLoading(true);
    setError(null);
    try {
      const params = status && status !== 'all' ? { status } : {};
      const res = await showroomService.getGuestReleases(params);
      if (res.success) setReleases(res.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setReleases([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, [statusFilter]);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch, statusFilter]);

  const create = useCallback(async (data) => {
    try {
      const res = await showroomService.createGuestRelease(data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const approve = useCallback(async (id) => {
    try {
      const res = await showroomService.approveGuestRelease(id);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const reject = useCallback(async (id, data) => {
    try {
      const res = await showroomService.rejectGuestRelease(id, data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const returnFromGuest = useCallback(async (id, data) => {
    try {
      const res = await showroomService.returnFromGuest(id, data);
      if (res.success) { await fetch(); return res; }
      throw new Error(res.message);
    } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  return { releases, loading, error, refetch: fetch, create, approve, reject, returnFromGuest };
};

// ============================================================
// Stock Control
// ============================================================
export const useShowroomStockControl = () => {
  const [opnameSessions, setOpnameSessions] = useState([]);
  const [restockRequests, setRestockRequests] = useState([]);
  const [maintenance, setMaintenance] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [opRes, rsRes, mtRes, rvRes] = await Promise.all([
        showroomService.getOpnameSessions(),
        showroomService.getRestockRequests(),
        showroomService.getMaintenance(),
        showroomService.getReservations(),
      ]);
      if (opRes.success) setOpnameSessions(opRes.data);
      if (rsRes.success) setRestockRequests(rsRes.data);
      if (mtRes.success) setMaintenance(mtRes.data);
      if (rvRes.success) setReservations(rvRes.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setOpnameSessions([]);
      setRestockRequests([]);
      setMaintenance([]);
      setReservations([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch]);

  const createOpname = useCallback(async (data) => {
    try { const res = await showroomService.createOpnameSession(data); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const completeOpname = useCallback(async (id) => {
    try { const res = await showroomService.completeOpname(id); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const approveOpname = useCallback(async (id) => {
    try { const res = await showroomService.approveOpname(id); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const createRestock = useCallback(async (data) => {
    try { const res = await showroomService.createRestockRequest(data); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const approveRestock = useCallback(async (id) => {
    try { const res = await showroomService.approveRestock(id); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const createMaintenance = useCallback(async (data) => {
    try { const res = await showroomService.createMaintenance(data); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const completeMaintenance = useCallback(async (id) => {
    try { const res = await showroomService.completeMaintenance(id); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const createReservation = useCallback(async (data) => {
    try { const res = await showroomService.createReservation(data); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  return {
    opnameSessions, restockRequests, maintenance, reservations,
    loading, error, refetch: fetch,
    createOpname, completeOpname, approveOpname,
    createRestock, approveRestock,
    createMaintenance, completeMaintenance,
    createReservation,
  };
};

// ============================================================
// Reports
// ============================================================
export const useShowroomReports = () => {
  const [kpi, setKpi] = useState(null);
  const [movementSummary, setMovementSummary] = useState([]);
  const [stockByLocation, setStockByLocation] = useState([]);
  const [borrowingSummary, setBorrowingSummary] = useState(null);
  const [guestSummary, setGuestSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [kpiRes, msRes, sblRes, bsRes, gsRes] = await Promise.all([
        showroomService.getKPI(),
        showroomService.getMovementSummary(30),
        showroomService.getStockByLocation(),
        showroomService.getBorrowingSummary(),
        showroomService.getGuestSummary(),
      ]);
      if (kpiRes.success) setKpi(kpiRes.data);
      if (msRes.success) setMovementSummary(msRes.data);
      if (sblRes.success) setStockByLocation(sblRes.data);
      if (bsRes.success) setBorrowingSummary(bsRes.data);
      if (gsRes.success) setGuestSummary(gsRes.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setKpi(null);
      setMovementSummary([]);
      setStockByLocation([]);
      setBorrowingSummary(null);
      setGuestSummary(null);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch]);

  return { kpi, movementSummary, stockByLocation, borrowingSummary, guestSummary, loading, error, refetch: fetch };
};

// ============================================================
// Master Data
// ============================================================
export const useShowroomMasterData = (typeFilter = null) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async (type = typeFilter) => {
    setLoading(true);
    setError(null);
    try {
      const params = type ? { type } : {};
      const res = await showroomService.getMasterData(params);
      if (res.success) setItems(res.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setItems([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, [typeFilter]);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch, typeFilter]);

  const create = useCallback(async (data) => {
    try { const res = await showroomService.createMasterData(data); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const update = useCallback(async (id, data) => {
    try { const res = await showroomService.updateMasterData(id, data); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const remove = useCallback(async (id) => {
    try { const res = await showroomService.deleteMasterData(id); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  const seed = useCallback(async () => {
    try { const res = await showroomService.seedMasterData(); if (res.success) { await fetch(); return res; } throw new Error(res.message); } catch (err) { toastError(err.response?.data?.message || err.message); throw err; }
  }, [fetch]);

  return { items, loading, error, refetch: fetch, create, update, remove, seed };
};

// ============================================================
// Sample Movements
// ============================================================
export const useShowroomMovements = (productId = null) => {
  const [movements, setMovements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { user } = useAuth();

  const fetch = useCallback(async (pId = productId) => {
    setLoading(true);
    setError(null);
    try {
      const params = pId ? { product_id: pId, limit: 100 } : { limit: 100 };
      const res = await showroomService.getMovements(params);
      if (res.success) setMovements(res.data);
    } catch (err) {
      const msg = err.response?.data?.message || err.message;
      setError(msg);
      setMovements([]);
      if (err.response?.status !== 404) toastError(msg);
    } finally {
      setLoading(false);
    }
  }, [productId]);

  useEffect(() => {
    if (!hasPermission(user, 'SHOWROOM')) return;
    fetch();
  }, [user, fetch, productId]);

  return { movements, loading, error, refetch: fetch };
};
