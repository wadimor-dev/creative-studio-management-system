import {
  TYPE_LABEL,
  STATUS_LABEL,
  BORROWING_STATUS,
  OPNAME_STATUS,
  MAINTENANCE_TYPE_LABEL,
} from '../constants';

export const formatDate = (dateString) => {
  if (!dateString) return '-';
  try {
    return new Date(dateString).toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  } catch {
    return dateString;
  }
};

export const formatDateFull = (dateString) => {
  if (!dateString) return '-';
  try {
    return new Date(dateString).toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  } catch {
    return dateString;
  }
};

export const formatDateInput = (dateString) => {
  if (!dateString) return '';
  try {
    return new Date(dateString).toISOString().split('T')[0];
  } catch {
    return '';
  }
};

export const getTodayDate = () => {
  return new Date().toISOString().split('T')[0];
};

export const formatMovementType = (type) => {
  return TYPE_LABEL[type] || type;
};

export const formatStatus = (status) => {
  return STATUS_LABEL[status] || status;
};

export const formatQuantity = (quantity, type) => {
  const prefix = type === 'HANDOVER' || type === 'RETURN' || type === 'ADJUSTMENT' ? '+' : '';
  return `${prefix}${quantity}`;
};

export const formatMaintenanceType = (type) => {
  return MAINTENANCE_TYPE_LABEL[type] || type;
};

export const isOverdueBorrowing = (borrowing) => {
  if (borrowing.status !== BORROWING_STATUS.BORROWED) return false;
  if (!borrowing.expected_return_date) return false;
  return new Date(borrowing.expected_return_date) < new Date();
};

export const isPendingApproval = (item, statusField = 'status') => {
  const status = item[statusField];
  return status === BORROWING_STATUS.PENDING || status === OPNAME_STATUS.DRAFT;
};

export const getInitialHandoverForm = () => ({
  product_id: '',
  quantity: '',
  location_id: '',
  storage_location_id: '',
  purpose: '',
  notes: '',
});

export const getInitialTransferForm = () => ({
  product_id: '',
  from_location_id: '',
  to_location_id: '',
  from_storage_location_id: '',
  to_storage_location_id: '',
  quantity: '',
  purpose: '',
  notes: '',
});

export const getInitialBorrowForm = () => ({
  product_id: '',
  from_location_id: '',
  borrower_name: '',
  borrower_location_id: '',
  quantity: '',
  purpose: '',
  borrow_date: getTodayDate(),
  expected_return_date: '',
  notes: '',
});

export const getInitialGuestReleaseForm = () => ({
  product_id: '',
  location_id: '',
  quantity: '',
  guest_name: '',
  guest_company: '',
  purpose: '',
  release_date: getTodayDate(),
  notes: '',
});

export const getInitialOpnameForm = () => ({
  name: '',
  location_id: '',
  notes: '',
});

export const getInitialRestockForm = () => ({
  product_id: '',
  location_id: '',
  minimum_quantity: '',
  current_quantity: '',
  requested_quantity: '',
  notes: '',
});

export const getInitialMaintenanceForm = () => ({
  product_id: '',
  location_id: '',
  maintenance_type: 'LAUNDRY',
  quantity: '',
  notes: '',
});

export const getInitialReservationForm = () => ({
  product_id: '',
  quantity: '',
  purpose: '',
  reserved_from: getTodayDate(),
  reserved_until: '',
  notes: '',
});

export const getInitialStockInForm = () => ({
  product: '',
  quantity: '',
  supplier: '',
  location: '',
  date: new Date().toISOString().split('T')[0],
  reference: '',
  notes: '',
});

export const getInitialStockOutForm = () => ({
  product: '',
  quantity: '',
  customer: '',
  location: '',
  date: new Date().toISOString().split('T')[0],
  reference: '',
  reason: '',
  notes: '',
});

export const getMovementSummary = (movements) => {
  const summary = {};
  movements.forEach((m) => {
    const type = m.type || m.movement_type;
    if (!summary[type]) {
      summary[type] = { count: 0, totalQuantity: 0 };
    }
    summary[type].count += 1;
    summary[type].totalQuantity += m.quantity;
  });
  return summary;
};
