import React, { useState, useEffect } from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Badge from '../../../components/common/Badge';
import Button from '../../../components/common/Button';
import Modal from '../../../components/common/Modal';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import SearchableSelect from '../../../components/common/SearchableSelect';
import DataTable from '../../../components/common/DataTable';
import FilterTabs from '../../../components/common/FilterTabs';
import { useShowroomStockControl } from '../../../hooks/useShowroomV2';
import { showroomService } from '../../../api/services/showroomService';
import { OPNAME_STATUS, RESTOCK_STATUS, STATUS_VARIANT, STATUS_LABEL, MAINTENANCE_TYPE, MAINTENANCE_TYPE_LABEL } from '../constants';
import { formatDate, getInitialOpnameForm, getInitialRestockForm, getInitialMaintenanceForm, getInitialReservationForm } from '../helpers';
import { Plus, ClipboardCheck, RefreshCw, Wrench, Calendar } from 'lucide-react';

const TABS = [
  { value: 'opname', label: 'Stock Opname', icon: ClipboardCheck },
  { value: 'restock', label: 'Restock Request', icon: RefreshCw },
  { value: 'maintenance', label: 'Maintenance', icon: Wrench },
  { value: 'reservation', label: 'Reservasi', icon: Calendar },
];

const StockControl = () => {
  const [activeTab, setActiveTab] = useState('opname');
  const {
    opnameSessions, restockRequests, maintenance, reservations, loading,
    createOpname, completeOpname, approveOpname,
    createRestock, approveRestock,
    createMaintenance, createReservation,
  } = useShowroomStockControl();

  return (
    <div className="space-y-6">
      <PageHeader title="Kontrol Stok" description="Opname, restock, maintenance, reservasi" />

      <FilterTabs tabs={TABS} active={activeTab} onChange={setActiveTab} />

      {activeTab === 'opname' && <OpnameTab data={opnameSessions} loading={loading} onCreate={createOpname} onComplete={completeOpname} onApprove={approveOpname} />}
      {activeTab === 'restock' && <RestockTab data={restockRequests} loading={loading} onCreate={createRestock} onApprove={approveRestock} />}
      {activeTab === 'maintenance' && <MaintenanceTab data={maintenance} loading={loading} onCreate={createMaintenance} />}
      {activeTab === 'reservation' && <ReservationTab data={reservations} loading={loading} onCreate={createReservation} />}
    </div>
  );
};

const OpnameTab = ({ data, loading, onCreate, onComplete, onApprove }) => {
  const [showForm, setShowForm] = useState(false);
  const columns = [
    { header: 'ID', accessor: 'id', cell: (row) => <span className="font-mono text-xs text-slate-500">OPN-{String(row.id).padStart(4, '0')}</span> },
    { header: 'Nama', accessor: 'name' },
    { header: 'Lokasi', accessor: 'location', cell: (row) => row.location?.name || '-' },
    { header: 'Status', accessor: 'status', cell: (row) => <Badge variant={STATUS_VARIANT[row.status]}>{STATUS_LABEL[row.status]}</Badge> },
    { header: 'Dibuat', accessor: 'created_at', cell: (row) => formatDate(row.created_at) },
    {
      header: 'Aksi', accessor: 'actions',
      cell: (row) => (
        <div className="flex gap-1">
          {row.status === OPNAME_STATUS.DRAFT && (
            <Button size="xs" onClick={() => onComplete(row.id)}>Selesai</Button>
          )}
          {row.status === OPNAME_STATUS.COMPLETED && (
            <Button size="xs" onClick={() => onApprove(row.id)}>Approve</Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <>
      <div className="flex justify-end">
        <Button onClick={() => setShowForm(true)} size="sm"><Plus className="mr-1 h-4 w-4" /> Sesi Opname</Button>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={data} columns={columns} isLoading={loading} />
      </div>
      {showForm && <OpnameForm isOpen={showForm} onClose={() => setShowForm(false)} onSubmit={onCreate} />}
    </>
  );
};

const RestockTab = ({ data, loading, onCreate, onApprove }) => {
  const [showForm, setShowForm] = useState(false);
  const columns = [
    { header: 'ID', accessor: 'id', cell: (row) => <span className="font-mono text-xs text-slate-500">RSK-{String(row.id).padStart(4, '0')}</span> },
    { header: 'Produk', accessor: 'product', cell: (row) => <span className="text-slate-900">{row.product?.display_name}</span> },
    { header: 'Lokasi', accessor: 'location', cell: (row) => row.location?.name },
    { header: 'Min', accessor: 'minimum_quantity', className: 'text-right' },
    { header: 'Saat Ini', accessor: 'current_quantity', className: 'text-right' },
    { header: 'Diminta', accessor: 'requested_quantity', className: 'text-right' },
    { header: 'Status', accessor: 'status', cell: (row) => <Badge variant={STATUS_VARIANT[row.status]}>{STATUS_LABEL[row.status]}</Badge> },
    {
      header: 'Aksi', accessor: 'actions',
      cell: (row) => row.status === RESTOCK_STATUS.PENDING && (
        <Button size="xs" onClick={() => onApprove(row.id)}>Approve</Button>
      ),
    },
  ];

  return (
    <>
      <div className="flex justify-end">
        <Button onClick={() => setShowForm(true)} size="sm"><Plus className="mr-1 h-4 w-4" /> Request Restock</Button>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={data} columns={columns} isLoading={loading} />
      </div>
      {showForm && <RestockForm isOpen={showForm} onClose={() => setShowForm(false)} onSubmit={onCreate} />}
    </>
  );
};

const MaintenanceTab = ({ data, loading, onCreate }) => {
  const [showForm, setShowForm] = useState(false);
  const columns = [
    { header: 'ID', accessor: 'id', cell: (row) => <span className="font-mono text-xs text-slate-500">MNT-{String(row.id).padStart(4, '0')}</span> },
    { header: 'Produk', accessor: 'product', cell: (row) => row.product?.display_name },
    { header: 'Tipe', accessor: 'maintenance_type', cell: (row) => MAINTENANCE_TYPE_LABEL[row.maintenance_type] || row.maintenance_type },
    { header: 'Qty', accessor: 'quantity', className: 'text-right' },
    { header: 'Status', accessor: 'status', cell: (row) => <Badge variant={STATUS_VARIANT[row.status]}>{STATUS_LABEL[row.status]}</Badge> },
    { header: 'Dibuat', accessor: 'created_at', cell: (row) => formatDate(row.created_at) },
  ];

  return (
    <>
      <div className="flex justify-end">
        <Button onClick={() => setShowForm(true)} size="sm"><Plus className="mr-1 h-4 w-4" /> Maintenance</Button>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={data} columns={columns} isLoading={loading} />
      </div>
      {showForm && <MaintenanceForm isOpen={showForm} onClose={() => setShowForm(false)} onSubmit={onCreate} />}
    </>
  );
};

const ReservationTab = ({ data, loading, onCreate }) => {
  const [showForm, setShowForm] = useState(false);
  const columns = [
    { header: 'ID', accessor: 'id', cell: (row) => <span className="font-mono text-xs text-slate-500">RSV-{String(row.id).padStart(4, '0')}</span> },
    { header: 'Produk', accessor: 'product', cell: (row) => row.product?.display_name },
    { header: 'Qty', accessor: 'quantity', className: 'text-right' },
    { header: 'Purpose', accessor: 'purpose' },
    { header: 'Dari', accessor: 'reserved_from', cell: (row) => formatDate(row.reserved_from) },
    { header: 'Sampai', accessor: 'reserved_until', cell: (row) => formatDate(row.reserved_until) },
    { header: 'Status', accessor: 'status', cell: (row) => <Badge variant={STATUS_VARIANT[row.status]}>{STATUS_LABEL[row.status]}</Badge> },
  ];

  return (
    <>
      <div className="flex justify-end">
        <Button onClick={() => setShowForm(true)} size="sm"><Plus className="mr-1 h-4 w-4" /> Reservasi</Button>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={data} columns={columns} isLoading={loading} />
      </div>
      {showForm && <ReservationForm isOpen={showForm} onClose={() => setShowForm(false)} onSubmit={onCreate} />}
    </>
  );
};

const OpnameForm = ({ isOpen, onClose, onSubmit }) => {
  const [form, setForm] = useState(getInitialOpnameForm());
  const [submitting, setSubmitting] = useState(false);
  const handleSubmit = async (e) => { e.preventDefault(); setSubmitting(true); try { await onSubmit(form); onClose(); } catch {} finally { setSubmitting(false); } };
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Sesi Opname Baru">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Nama Sesi" placeholder="Contoh: Opname Q1 2026" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

const useProductOptions = () => {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    showroomService.getProducts().then((res) => {
      if (res.success) {
        setProducts(res.data.map((p) => ({ value: String(p.id), label: p.display_name, subLabel: p.sku })));
      }
    }).catch(() => {});
  }, []);
  return products;
};

const useLocationOptions = () => {
  const [locations, setLocations] = useState([]);
  useEffect(() => {
    showroomService.getLocations().then((res) => {
      if (res.success) {
        setLocations(res.data.map((l) => ({ value: String(l.id), label: l.name })));
      }
    }).catch(() => {});
  }, []);
  return locations;
};

const RestockForm = ({ isOpen, onClose, onSubmit }) => {
  const [form, setForm] = useState(getInitialRestockForm());
  const [submitting, setSubmitting] = useState(false);
  const productOptions = useProductOptions();
  const locationOptions = useLocationOptions();
  const handleSubmit = async (e) => { e.preventDefault(); setSubmitting(true); try { await onSubmit({ ...form, product_id: Number(form.product_id), location_id: Number(form.location_id), minimum_quantity: Number(form.minimum_quantity), current_quantity: Number(form.current_quantity), requested_quantity: Number(form.requested_quantity) }); onClose(); } catch {} finally { setSubmitting(false); } };
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Request Restock">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={productOptions} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Lokasi</label>
          <SearchableSelect options={locationOptions} value={form.location_id} onChange={(v) => setForm({ ...form, location_id: v })} placeholder="Cari lokasi..." />
        </div>
        <Input label="Minimum Qty" type="number" placeholder="Stok minimum" value={form.minimum_quantity} onChange={(e) => setForm({ ...form, minimum_quantity: e.target.value })} required />
        <Input label="Qty Saat Ini" type="number" placeholder="Stok saat ini" value={form.current_quantity} onChange={(e) => setForm({ ...form, current_quantity: e.target.value })} required />
        <Input label="Qty Diminta" type="number" placeholder="Jumlah yang diminta" value={form.requested_quantity} onChange={(e) => setForm({ ...form, requested_quantity: e.target.value })} required />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

const MaintenanceForm = ({ isOpen, onClose, onSubmit }) => {
  const [form, setForm] = useState(getInitialMaintenanceForm());
  const [submitting, setSubmitting] = useState(false);
  const productOptions = useProductOptions();
  const handleSubmit = async (e) => { e.preventDefault(); setSubmitting(true); try { await onSubmit({ ...form, product_id: Number(form.product_id), quantity: Number(form.quantity) }); onClose(); } catch {} finally { setSubmitting(false); } };
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Maintenance Baru">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={productOptions} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <Select label="Tipe" value={form.maintenance_type} onChange={(e) => setForm({ ...form, maintenance_type: e.target.value })} options={Object.entries(MAINTENANCE_TYPE).map(([k, v]) => ({ value: v, label: MAINTENANCE_TYPE_LABEL[v] }))} />
        <Input label="Quantity" type="number" placeholder="Masukkan jumlah" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

const ReservationForm = ({ isOpen, onClose, onSubmit }) => {
  const [form, setForm] = useState(getInitialReservationForm());
  const [submitting, setSubmitting] = useState(false);
  const productOptions = useProductOptions();
  const handleSubmit = async (e) => { e.preventDefault(); setSubmitting(true); try { await onSubmit({ ...form, product_id: Number(form.product_id), quantity: Number(form.quantity) }); onClose(); } catch {} finally { setSubmitting(false); } };
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Reservasi Sample">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={productOptions} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <Input label="Quantity" type="number" placeholder="Masukkan jumlah" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
        <Textarea label="Purpose" placeholder="Tujuan reservasi..." value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} />
        <Input label="Dari Tanggal" type="date" value={form.reserved_from} onChange={(e) => setForm({ ...form, reserved_from: e.target.value })} required />
        <Input label="Sampai Tanggal" type="date" value={form.reserved_until} onChange={(e) => setForm({ ...form, reserved_until: e.target.value })} required />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

export default StockControl;
