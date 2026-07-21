import React, { useMemo, useState } from 'react';
import { Pill, Plus, AlertTriangle } from 'lucide-react';
import {
  useMedicines,
  useCreateMedicine,
  useAdjustMedicineStock,
} from '../hooks';
import { MedicineStockTable } from '../components';
import { isLowStock } from '../helpers';

const EMPTY = { code: '', name: '', unit: 'tablet', stock: 0, min_stock: 10 };
const inputCls =
  'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500';

const StatChip = ({ icon: Icon, label, value, accent }) => (
  <div className='flex items-center gap-3 bg-white border border-slate-200 rounded-xl p-3 shadow-sm'>
    <div className={`w-9 h-9 rounded-lg grid place-items-center ${accent}`}>
      <Icon className='w-4 h-4' />
    </div>
    <div>
      <div className='text-lg font-bold text-slate-800 leading-tight'>
        {value}
      </div>
      <div className='text-xs text-slate-500'>{label}</div>
    </div>
  </div>
);

const Medicines = () => {
  const medicines = useMedicines();
  const createMedicine = useCreateMedicine();
  const adjustStock = useAdjustMedicineStock();

  const [form, setForm] = useState(EMPTY);
  const [showForm, setShowForm] = useState(false);
  const [q, setQ] = useState('');
  const [onlyLow, setOnlyLow] = useState(false);

  const list = medicines.data || [];
  const lowCount = useMemo(() => list.filter(isLowStock).length, [list]);
  const totalUnit = useMemo(
    () => list.reduce((a, m) => a + (m.stock || 0), 0),
    [list],
  );

  const filtered = useMemo(
    () =>
      list.filter((m) => {
        const okQ =
          !q || `${m.name} ${m.code}`.toLowerCase().includes(q.toLowerCase());
        const okLow = !onlyLow || isLowStock(m);
        return okQ && okLow;
      }),
    [list, q, onlyLow],
  );

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }));
  const submit = (e) => {
    e.preventDefault();
    if (!form.name.trim()) return;
    createMedicine.mutate(
      { ...form, stock: Number(form.stock), min_stock: Number(form.min_stock) },
      {
        onSuccess: () => {
          setForm(EMPTY);
          setShowForm(false);
        },
      },
    );
  };

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-5xl'>
      {/* Header */}
      <div className='flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3'>
        <div>
          <h1 className='text-xl font-semibold text-slate-800'>
            Obat &amp; Stok
          </h1>
          <p className='text-slate-500 text-sm'>
            Kelola master obat klinik dan sesuaikan stok saat restock atau
            koreksi.
          </p>
        </div>
        <button
          onClick={() => setShowForm((s) => !s)}
          className='inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 self-start'
        >
          <Plus className='w-4 h-4' /> {showForm ? 'Tutup Form' : 'Tambah Obat'}
        </button>
      </div>

      {/* Ringkasan */}
      <div className='grid grid-cols-2 sm:grid-cols-3 gap-3'>
        <StatChip
          icon={Pill}
          label='Jenis obat'
          value={list.length}
          accent='bg-brand-100 text-brand-700'
        />
        <StatChip
          icon={AlertTriangle}
          label='Stok menipis'
          value={lowCount}
          accent='bg-red-100 text-red-700'
        />
        <StatChip
          icon={Pill}
          label='Total unit'
          value={totalUnit}
          accent='bg-green-100 text-green-700'
        />
      </div>

      {/* Form tambah (collapsible) */}
      {showForm && (
        <form
          onSubmit={submit}
          className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm grid grid-cols-2 md:grid-cols-6 gap-3 items-end'
        >
          <div>
            <label className='block text-xs mb-1 text-slate-600'>Kode</label>
            <input
              value={form.code}
              onChange={(e) => set('code', e.target.value)}
              className={inputCls}
              placeholder='OBT-001'
            />
          </div>
          <div className='col-span-2'>
            <label className='block text-xs mb-1 text-slate-600'>
              Nama obat
            </label>
            <input
              value={form.name}
              onChange={(e) => set('name', e.target.value)}
              className={inputCls}
              placeholder='Paracetamol'
            />
          </div>
          <div>
            <label className='block text-xs mb-1 text-slate-600'>Satuan</label>
            <input
              value={form.unit}
              onChange={(e) => set('unit', e.target.value)}
              className={inputCls}
            />
          </div>
          <div>
            <label className='block text-xs mb-1 text-slate-600'>
              Stok awal
            </label>
            <input
              type='number'
              min={0}
              value={form.stock}
              onChange={(e) => set('stock', e.target.value)}
              className={inputCls}
            />
          </div>
          <div>
            <label className='block text-xs mb-1 text-slate-600'>
              Min. stok
            </label>
            <input
              type='number'
              min={0}
              value={form.min_stock}
              onChange={(e) => set('min_stock', e.target.value)}
              className={inputCls}
            />
          </div>
          <button
            type='submit'
            disabled={createMedicine.isPending}
            className='col-span-2 md:col-span-6 px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'
          >
            {createMedicine.isPending ? 'Menyimpan…' : 'Simpan Obat'}
          </button>
        </form>
      )}

      {/* Toolbar + tabel */}
      <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm space-y-4'>
        <div className='flex flex-col sm:flex-row sm:items-center gap-3'>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder='🔍  Cari nama / kode obat…'
            className='flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500'
          />
          <label className='inline-flex items-center gap-2 text-sm text-slate-600 select-none'>
            <input
              type='checkbox'
              checked={onlyLow}
              onChange={(e) => setOnlyLow(e.target.checked)}
              className='rounded border-slate-300'
            />
            Hanya stok menipis
          </label>
        </div>

        {medicines.isLoading ? (
          <div className='h-24 bg-slate-100 rounded animate-pulse' />
        ) : (
          <MedicineStockTable
            medicines={filtered}
            onAdjust={(m, delta) => adjustStock.mutate({ id: m.id, delta })}
          />
        )}
      </div>
    </div>
  );
};

export default Medicines;
