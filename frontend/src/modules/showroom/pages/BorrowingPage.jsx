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

import { useShowroomBorrowings } from '../../../hooks/useShowroomV2';
import { showroomService } from '../../../api/services/showroomService';
import { BORROWING_STATUS, BORROWING_STATUS_FILTER, STATUS_VARIANT, STATUS_LABEL, PURPOSE_OPTIONS } from '../constants';
import { formatDate, isOverdueBorrowing, getInitialBorrowForm } from '../helpers';
import { Plus, Check, X } from 'lucide-react';

const BorrowingPage = () => {
  const [statusFilter, setStatusFilter] = useState('all');
  const [showForm, setShowForm] = useState(false);
  const { borrowings, loading, approve, cancel } = useShowroomBorrowings(statusFilter === 'all' ? null : statusFilter);

  const filterTabs = BORROWING_STATUS_FILTER.map((f) => ({ ...f, value: f.value === 'all' ? 'all' : f.value }));

  const columns = [
    { header: 'ID', accessor: 'id', cell: (row) => <span className="font-mono text-xs text-slate-500">BRW-{String(row.id).padStart(4, '0')}</span> },
    {
      header: 'Produk', accessor: 'product',
      cell: (row) => (
        <div>
          <p className="font-medium text-slate-900">{row.product?.display_name}</p>
          <p className="text-xs text-slate-500">{row.product?.sku}</p>
        </div>
      ),
    },
    { header: 'Peminjam', accessor: 'borrower_name' },
    { header: 'Qty', accessor: 'quantity', className: 'text-right' },
    { header: 'Purpose', accessor: 'purpose' },
    { header: 'Tgl Pinjam', accessor: 'borrow_date', cell: (row) => formatDate(row.borrow_date) },
    {
      header: 'Tgl Kembali', accessor: 'expected_return_date',
      cell: (row) => {
        const overdue = isOverdueBorrowing(row);
        return (
          <span className={overdue ? 'font-semibold text-red-600' : ''}>
            {formatDate(row.expected_return_date)}
            {overdue && <span className="ml-1 text-xs text-red-500">(Overdue)</span>}
          </span>
        );
      },
    },
    {
      header: 'Status', accessor: 'status',
      cell: (row) => <Badge variant={STATUS_VARIANT[row.status] || 'secondary'}>{STATUS_LABEL[row.status] || row.status}</Badge>,
    },
    {
      header: 'Aksi', accessor: 'actions',
      cell: (row) => (
        <div className="flex gap-1">
          {row.status === BORROWING_STATUS.PENDING && (
            <Button size="xs" onClick={() => approve(row.id)}>
              <Check className="mr-1 h-3 w-3" /> Approve
            </Button>
          )}
          {[BORROWING_STATUS.PENDING, BORROWING_STATUS.BORROWED].includes(row.status) && (
            <Button size="xs" variant="danger" onClick={() => cancel(row.id)}>
              <X className="mr-1 h-3 w-3" /> Batal
            </Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Peminjaman"
        description="Tracking peminjaman sample internal"
        actions={
          <Button onClick={() => setShowForm(true)} size="sm">
            <Plus className="mr-1 h-4 w-4" /> Pinjam Sample
          </Button>
        }
      />

      <FilterTabs tabs={filterTabs} active={statusFilter} onChange={setStatusFilter} />

      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={borrowings} columns={columns} isLoading={loading} />
      </div>

      {showForm && <BorrowForm isOpen={showForm} onClose={() => setShowForm(false)} />}
    </div>
  );
};

const BorrowForm = ({ isOpen, onClose }) => {
  const [form, setForm] = useState(getInitialBorrowForm());
  const [submitting, setSubmitting] = useState(false);
  const [locations, setLocations] = useState([]);
  const [products, setProducts] = useState([]);

  React.useEffect(() => {
    showroomService.getLocations().then((res) => {
      if (res.success) setLocations(res.data);
    }).catch(() => {
      setLocations([{ id: 1, name: 'Showroom Utama' }, { id: 2, name: 'Display Area' }]);
    });
    showroomService.getProducts().then((res) => {
      if (res.success) {
        setProducts(res.data.map((p) => ({ value: String(p.id), label: p.display_name, subLabel: p.sku })));
      }
    }).catch(() => {});
  }, []);

  const locationOptions = locations.map((l) => ({ value: String(l.id), label: l.name }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await showroomService.createBorrowing({ ...form, product_id: Number(form.product_id), quantity: Number(form.quantity) });
      onClose();
    } catch { } finally { setSubmitting(false); }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Pinjam Sample">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={products} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Dari Lokasi</label>
          <SearchableSelect options={locationOptions} value={form.from_location_id} onChange={(v) => setForm({ ...form, from_location_id: v })} placeholder="Cari lokasi..." />
        </div>
        <Input label="Nama Peminjam" placeholder="Masukkan nama peminjam" value={form.borrower_name} onChange={(e) => setForm({ ...form, borrower_name: e.target.value })} required />
        <Input label="Quantity" type="number" placeholder="Masukkan jumlah" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
        <Select label="Purpose" value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} options={[{ value: '', label: 'Pilih' }, ...PURPOSE_OPTIONS]} />
        <Input label="Tgl Pinjam" type="date" value={form.borrow_date} onChange={(e) => setForm({ ...form, borrow_date: e.target.value })} required />
        <Input label="Est. Tgl Kembali" type="date" value={form.expected_return_date} onChange={(e) => setForm({ ...form, expected_return_date: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

export default BorrowingPage;
