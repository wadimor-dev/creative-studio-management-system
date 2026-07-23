import {
  VISIT_STATUS_LABEL, VISIT_STATUS_BADGE,
  QUEUE_STATUS_LABEL, QUEUE_STATUS_BADGE,
  RX_STATUS_LABEL, RX_STATUS_BADGE,
  LOW_STOCK_THRESHOLD,
} from '../constants';

export const formatDate = (v) =>
  !v ? '-' : new Date(v).toLocaleDateString('id-ID', {
    day: '2-digit', month: 'short', year: 'numeric',
  });

export const formatDateTime = (v) =>
  !v ? '-' : new Date(v).toLocaleString('id-ID', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });

export const formatTime = (v) =>
  !v ? '-' : new Date(v).toLocaleTimeString('id-ID', {
    hour: '2-digit', minute: '2-digit',
  });

export const calcAge = (birthDate) => {
  if (!birthDate) return null;
  const b = new Date(birthDate);
  const now = new Date();
  let age = now.getFullYear() - b.getFullYear();
  const m = now.getMonth() - b.getMonth();
  if (m < 0 || (m === 0 && now.getDate() < b.getDate())) age--;
  return age;
};

export const isToday = (v) => {
  if (!v) return false;
  return new Date(v).toDateString() === new Date().toDateString();
};

export const statusLabel = (s, map = VISIT_STATUS_LABEL) => map[s] || s;
export const statusBadge = (s, map = VISIT_STATUS_BADGE) => map[s] || 'bg-gray-100 text-gray-600';

export const visitStatusLabel = (s) => statusLabel(s, VISIT_STATUS_LABEL);
export const visitStatusBadge = (s) => statusBadge(s, VISIT_STATUS_BADGE);
export const queueStatusLabel = (s) => statusLabel(s, QUEUE_STATUS_LABEL);
export const queueStatusBadge = (s) => statusBadge(s, QUEUE_STATUS_BADGE);
export const rxStatusLabel = (s) => statusLabel(s, RX_STATUS_LABEL);
export const rxStatusBadge = (s) => statusBadge(s, RX_STATUS_BADGE);

export const isLowStock = (med) =>
  (med?.stock ?? 0) <= (med?.min_stock ?? LOW_STOCK_THRESHOLD);

export const groupBy = (arr, keyFn) =>
  (arr || []).reduce((acc, item) => {
    const k = keyFn(item);
    (acc[k] = acc[k] || []).push(item);
    return acc;
  }, {});
