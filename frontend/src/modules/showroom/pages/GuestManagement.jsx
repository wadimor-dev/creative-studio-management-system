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

import { useShowroomGuestReleases } from '../../../hooks/useShowroomV2';
import { showroomService } from '../../../api/services/showroomService';
import { PURPOSE_OPTIONS } from '../constants';
import { formatDate, getInitialGuestReleaseForm } from '../helpers';
import { Plus, Check } from 'lucide-react';

const GuestManagement = () => {
  const [filter, setFilter] = useState('all');
  const [showForm, setShowForm] = useState(false);
  const { releases, loading, approve } = useShowroomGuestReleases(
    filter === 'all' ? null : filter
  );

  const filterTabs = [
    { value: 'all', label: 'Semua' },
    { value: 'pending', label: 'Menunggu' },
    { value: 'approved', label: 'Disetujui' },
  ];

  const columns = [
    { header: 'ID', accessor: 'id', cell: (row) => <span className="font-mono text-xs text-slate-500">GR-{String(row.id).padStart(4, '0')}</span> },
    {
      header: 'Produk', accessor: 'product',
      cell: (row) => (
        <div>
          <p className="font-medium text-slate-900">{row.product?.display_name}</p>
          <p className="text-xs text-slate-500">{row.product?.sku}</p>
        </div>
      ),
    },
    { header: 'Qty', accessor: 'quantity', className: 'text-right' },
    { header: 'Tamu', accessor: 'guest_name' },
    { header: 'Perusahaan', accessor: 'guest_company', cell: (row) => row.guest_company || '-' },
    { header: 'Purpose', accessor: 'purpose' },
    { header: 'Tgl Release', accessor: 'release_date', cell: (row) => formatDate(row.release_date) },
    {
      header: 'Disetujui', accessor: 'approved_by',
      cell: (row) => row.approved_by
        ? <Badge variant="success" size="sm">{row.approved_by.username}</Badge>
        : <Badge variant="warning" size="sm">Menunggu</Badge>,
    },
    {
      header: 'Aksi', accessor: 'actions',
      cell: (row) => (
        !row.approved_by && (
          <Button size="xs" onClick={() => approve(row.id)}>
            <Check className="mr-1 h-3 w-3" /> Approve
          </Button>
        )
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Manajemen Tamu"
        description="Release sample ke tamu dengan approval workflow"
        actions={
          <Button onClick={() => setShowForm(true)} size="sm">
            <Plus className="mr-1 h-4 w-4" /> Release ke Tamu
          </Button>
        }
      />

      <FilterTabs tabs={filterTabs} active={filter} onChange={setFilter} />

      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={releases} columns={columns} isLoading={loading} />
      </div>

      {showForm && <GuestReleaseForm isOpen={showForm} onClose={() => setShowForm(false)} />}
    </div>
  );
};

const GuestReleaseForm = ({ isOpen, onClose }) => {
  const [form, setForm] = useState(getInitialGuestReleaseForm());
  const [submitting, setSubmitting] = useState(false);
  const [locations, setLocations] = useState([]);
  const [products, setProducts] = useState([]);

  React.useEffect(() => {
    showroomService.getLocations().then((res) => {
      if (res.success) setLocations(res.data);
    }).catch(() => {
      setLocations([{ id: 1, name: 'Showroom Utama' }]);
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
      await showroomService.createGuestRelease({ ...form, product_id: Number(form.product_id), quantity: Number(form.quantity) });
      onClose();
    } catch { } finally { setSubmitting(false); }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Release Sample ke Tamu">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={products} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Lokasi</label>
          <SearchableSelect options={locationOptions} value={form.location_id} onChange={(v) => setForm({ ...form, location_id: v })} placeholder="Cari lokasi..." />
        </div>
        <Input label="Quantity" type="number" placeholder="Masukkan jumlah" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
        <Input label="Nama Tamu" placeholder="Masukkan nama tamu" value={form.guest_name} onChange={(e) => setForm({ ...form, guest_name: e.target.value })} required />
        <Input label="Perusahaan" placeholder="Masukkan nama perusahaan" value={form.guest_company} onChange={(e) => setForm({ ...form, guest_company: e.target.value })} />
        <Select label="Purpose" value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} options={[{ value: '', label: 'Pilih' }, ...PURPOSE_OPTIONS]} />
        <Input label="Tgl Release" type="date" value={form.release_date} onChange={(e) => setForm({ ...form, release_date: e.target.value })} required />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

export default GuestManagement;
