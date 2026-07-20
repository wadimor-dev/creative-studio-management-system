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
import LoadingSpinner from '../../../components/common/LoadingSpinner';

import { useShowroomSampleStock } from '../../../hooks/useShowroomV2';
import { showroomService } from '../../../api/services/showroomService';
import { PURPOSE_OPTIONS } from '../constants';
import { getInitialHandoverForm, getInitialTransferForm } from '../helpers';
import { Package, ArrowUpDown, Plus, Wrench } from 'lucide-react';

const useStorageOptions = (locationId) => {
  const [options, setOptions] = useState([]);
  useEffect(() => {
    const params = locationId ? { location_id: locationId } : {};
    showroomService.getStorageLocations(params).then((res) => {
      if (res.success) {
        setOptions(res.data.map((s) => ({
          value: String(s.id),
          label: `${s.name} (${s.code})`,
          subLabel: s.path || s.storage_type,
        })));
      }
    }).catch(() => {});
  }, [locationId]);
  return options;
};

const Stock = () => {
  const [selectedLocation, setSelectedLocation] = useState('');
  const [activeForm, setActiveForm] = useState(null);
  const { stock, locations, loading, handover, transfer, adjust } = useShowroomSampleStock(selectedLocation || null);

  const columns = [
    {
      header: 'SKU', accessor: 'sku',
      cell: (row) => <span className="font-mono text-xs text-slate-500">{row.sku}</span>,
    },
    {
      header: 'Produk', accessor: 'product_name',
      cell: (row) => <span className="font-medium text-slate-900">{row.product_name}</span>,
    },
    {
      header: 'Total Qty', accessor: 'total_quantity', className: 'text-right',
      cell: (row) => <span className="font-semibold text-slate-900">{row.total_quantity}</span>,
    },
    {
      header: 'Lokasi', accessor: 'locations',
      cell: (row) => (
        <div className="flex flex-wrap gap-1">
          {row.locations?.map((loc, i) => (
            <Badge key={i} variant="info" size="sm">{loc.location_name}: {loc.quantity}</Badge>
          ))}
        </div>
      ),
    },
  ];

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Sample Management"
        description="Stock per produk & lokasi, handover, transfer, pinjam"
        actions={
          <div className="flex gap-2">
            <Button onClick={() => setActiveForm('handover')} size="sm">
              <Plus className="mr-1 h-4 w-4" /> Handover
            </Button>
            <Button onClick={() => setActiveForm('transfer')} variant="secondary" size="sm">
              <ArrowUpDown className="mr-1 h-4 w-4" /> Transfer
            </Button>
            <Button onClick={() => setActiveForm('adjust')} variant="secondary" size="sm">
              <Wrench className="mr-1 h-4 w-4" /> Adjust
            </Button>
          </div>
        }
      />

      <div className="flex items-center gap-4">
        <div className="w-64">
          <Select
            value={selectedLocation}
            onChange={(e) => setSelectedLocation(e.target.value)}
            options={[{ value: '', label: 'Semua Lokasi' }, ...locations.map((l) => ({ value: l.id, label: l.name }))]}
          />
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <DataTable data={stock} columns={columns} isLoading={loading} />
      </div>

      {activeForm === 'handover' && (
        <HandoverForm isOpen onClose={() => setActiveForm(null)} locations={locations} onSubmit={handover} />
      )}
      {activeForm === 'transfer' && (
        <TransferForm isOpen onClose={() => setActiveForm(null)} locations={locations} onSubmit={transfer} />
      )}
      {activeForm === 'adjust' && (
        <AdjustForm isOpen onClose={() => setActiveForm(null)} locations={locations} onSubmit={adjust} />
      )}
    </div>
  );
};

const useProductOptions = () => {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    showroomService.getProducts().then((res) => {
      if (res.success) {
        setProducts(res.data.map((p) => ({
          value: String(p.id),
          label: p.display_name,
          subLabel: p.sku,
        })));
      }
    }).catch(() => {});
  }, []);
  return products;
};

const HandoverForm = ({ isOpen, onClose, locations, onSubmit }) => {
  const [form, setForm] = useState(getInitialHandoverForm());
  const [submitting, setSubmitting] = useState(false);
  const productOptions = useProductOptions();
  const locationOptions = locations.map((l) => ({ value: String(l.id), label: l.name }));
  const storageOptions = useStorageOptions(form.location_id || null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit({
        ...form,
        product_id: Number(form.product_id),
        quantity: Number(form.quantity),
        storage_location_id: form.storage_location_id ? Number(form.storage_location_id) : undefined,
      });
      onClose();
    } catch { } finally { setSubmitting(false); }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Handover dari Inventory">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={productOptions} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <Input label="Quantity" type="number" placeholder="Masukkan jumlah" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Lokasi Tujuan</label>
          <SearchableSelect options={locationOptions} value={form.location_id} onChange={(v) => setForm({ ...form, location_id: v, storage_location_id: '' })} placeholder="Cari lokasi..." />
        </div>
        {form.location_id && storageOptions.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Storage Location <span className="text-slate-400">(opsional)</span></label>
            <SearchableSelect options={storageOptions} value={form.storage_location_id} onChange={(v) => setForm({ ...form, storage_location_id: v })} placeholder="Pilih rak/laci..." />
          </div>
        )}
        <Select label="Purpose" value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} options={[{ value: '', label: 'Pilih Purpose' }, ...PURPOSE_OPTIONS]} />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

const TransferForm = ({ isOpen, onClose, locations, onSubmit }) => {
  const [form, setForm] = useState(getInitialTransferForm());
  const [submitting, setSubmitting] = useState(false);
  const productOptions = useProductOptions();
  const locationOptions = locations.map((l) => ({ value: String(l.id), label: l.name }));
  const fromStorageOptions = useStorageOptions(form.from_location_id || null);
  const toStorageOptions = useStorageOptions(form.to_location_id || null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit({
        ...form,
        product_id: Number(form.product_id),
        quantity: Number(form.quantity),
        from_storage_location_id: form.from_storage_location_id ? Number(form.from_storage_location_id) : undefined,
        to_storage_location_id: form.to_storage_location_id ? Number(form.to_storage_location_id) : undefined,
      });
      onClose();
    } catch { } finally { setSubmitting(false); }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Transfer Antar Lokasi">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={productOptions} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Dari Lokasi</label>
          <SearchableSelect options={locationOptions} value={form.from_location_id} onChange={(v) => setForm({ ...form, from_location_id: v, from_storage_location_id: '' })} placeholder="Cari lokasi asal..." />
        </div>
        {form.from_location_id && fromStorageOptions.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Dari Storage <span className="text-slate-400">(opsional)</span></label>
            <SearchableSelect options={fromStorageOptions} value={form.from_storage_location_id} onChange={(v) => setForm({ ...form, from_storage_location_id: v })} placeholder="Pilih rak/laci asal..." />
          </div>
        )}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Ke Lokasi</label>
          <SearchableSelect options={locationOptions} value={form.to_location_id} onChange={(v) => setForm({ ...form, to_location_id: v, to_storage_location_id: '' })} placeholder="Cari lokasi tujuan..." />
        </div>
        {form.to_location_id && toStorageOptions.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Ke Storage <span className="text-slate-400">(opsional)</span></label>
            <SearchableSelect options={toStorageOptions} value={form.to_storage_location_id} onChange={(v) => setForm({ ...form, to_storage_location_id: v })} placeholder="Pilih rak/laci tujuan..." />
          </div>
        )}
        <Input label="Quantity" type="number" placeholder="Masukkan jumlah" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
        <Select label="Purpose" value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} options={[{ value: '', label: 'Pilih Purpose' }, ...PURPOSE_OPTIONS]} />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

const AdjustForm = ({ isOpen, onClose, locations, onSubmit }) => {
  const [form, setForm] = useState({ product_id: '', location_id: '', storage_location_id: '', adjustment: '', purpose: '', notes: '' });
  const [submitting, setSubmitting] = useState(false);
  const productOptions = useProductOptions();
  const locationOptions = locations.map((l) => ({ value: String(l.id), label: l.name }));
  const storageOptions = useStorageOptions(form.location_id || null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit({
        ...form,
        adjustment: Number(form.adjustment),
        quantity: Math.abs(Number(form.adjustment)),
        storage_location_id: form.storage_location_id ? Number(form.storage_location_id) : undefined,
      });
      onClose();
    } catch { } finally { setSubmitting(false); }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Penyesuaian Stok">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Produk</label>
          <SearchableSelect options={productOptions} value={form.product_id} onChange={(v) => setForm({ ...form, product_id: v })} placeholder="Cari produk..." />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Lokasi</label>
          <SearchableSelect options={locationOptions} value={form.location_id} onChange={(v) => setForm({ ...form, location_id: v, storage_location_id: '' })} placeholder="Cari lokasi..." />
        </div>
        {form.location_id && storageOptions.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Storage Location <span className="text-slate-400">(opsional)</span></label>
            <SearchableSelect options={storageOptions} value={form.storage_location_id} onChange={(v) => setForm({ ...form, storage_location_id: v })} placeholder="Pilih rak/laci..." />
          </div>
        )}
        <Input label="Adjustment (+/-)" type="number" placeholder="Masukkan angka (+/-)" value={form.adjustment} onChange={(e) => setForm({ ...form, adjustment: e.target.value })} required />
        <Textarea label="Purpose" placeholder="Tujuan penyesuaian..." value={form.purpose} onChange={(e) => setForm({ ...form, purpose: e.target.value })} />
        <Textarea label="Notes" placeholder="Catatan opsional..." value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Batal</Button>
          <Button type="submit" isLoading={submitting}>Simpan</Button>
        </div>
      </form>
    </Modal>
  );
};

export default Stock;
