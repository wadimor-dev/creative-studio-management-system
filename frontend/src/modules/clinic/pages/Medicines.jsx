import React, { useMemo, useState, useEffect } from 'react';
import { Pill, AlertTriangle } from 'lucide-react';
import api from '../../../api/axios';
import { isLowStock } from '../helpers';

const Medicines = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState('');
  const [onlyLow, setOnlyLow] = useState(false);

  useEffect(() => {
    api.get('/inventory/items?limit=200').then(r => {
      const d = r.data;
      setItems(Array.isArray(d) ? d : d?.data || d?.items || []);
    }).finally(() => setLoading(false));
  }, []);

  const list = items;
  const lowCount = useMemo(() => list.filter(isLowStock).length, [list]);
  const totalUnit = useMemo(() => list.reduce((a, m) => a + (m.stock || 0), 0), [list]);

  const filtered = useMemo(() =>
    list.filter((m) => {
      const okQ = !q || `${m.name || ''} ${m.sku || m.code || ''}`.toLowerCase().includes(q.toLowerCase());
      const okLow = !onlyLow || isLowStock(m);
      return okQ && okLow;
    }), [list, q, onlyLow]);

  const StatChip = ({ icon: Icon, label, value, accent }) => (
    <div className='flex items-center gap-3 bg-white border border-slate-200 rounded-xl p-3 shadow-sm'>
      <div className={`w-9 h-9 rounded-lg grid place-items-center ${accent}`}>
        <Icon className='w-4 h-4' />
      </div>
      <div>
        <div className='text-lg font-bold text-slate-800 leading-tight'>{value}</div>
        <div className='text-xs text-slate-500'>{label}</div>
      </div>
    </div>
  );

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-5xl'>
      <div>
        <h1 className='text-xl font-semibold text-slate-800'>Obat &amp; Stok</h1>
        <p className='text-slate-500 text-sm'>Data obat bersumber dari master inventory.</p>
      </div>

      <div className='grid grid-cols-2 sm:grid-cols-3 gap-3'>
        <StatChip icon={Pill} label='Jenis obat' value={list.length} accent='bg-brand-100 text-brand-700' />
        <StatChip icon={AlertTriangle} label='Stok menipis' value={lowCount} accent='bg-red-100 text-red-700' />
        <StatChip icon={Pill} label='Total unit' value={totalUnit} accent='bg-green-100 text-green-700' />
      </div>

      <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm space-y-4'>
        <div className='flex flex-col sm:flex-row sm:items-center gap-3'>
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder='Cari nama / kode obat…' className='flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500' />
          <label className='inline-flex items-center gap-2 text-sm text-slate-600 select-none'>
            <input type='checkbox' checked={onlyLow} onChange={(e) => setOnlyLow(e.target.checked)} className='rounded border-slate-300' />
            Hanya stok menipis
          </label>
        </div>

        {loading ? (
          <div className='h-24 bg-slate-100 rounded animate-pulse' />
        ) : !filtered.length ? (
          <p className='text-slate-500 text-sm py-4'>Belum ada data obat.</p>
        ) : (
          <>
            <ul className='space-y-2 md:hidden'>
              {filtered.map((m) => {
                const low = isLowStock(m);
                return (
                  <li key={m.id} className={`border rounded-lg p-3 ${low ? 'border-red-200 bg-red-50' : 'border-slate-200'}`}>
                    <div className='flex justify-between items-start'>
                      <div className='min-w-0'>
                        <div className='font-medium text-slate-800 truncate'>{m.name}</div>
                        <div className='text-xs text-slate-500'>{m.sku || m.code} · min {m.min_stock || 0}</div>
                      </div>
                      <div className='text-right shrink-0'>
                        <div className='font-semibold text-slate-800'>{m.stock || 0} {m.unit?.name || ''}</div>
                        {low ? <span className='text-red-600 text-xs font-medium'>Menipis</span> : <span className='text-green-600 text-xs'>Aman</span>}
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
            <div className='hidden md:block overflow-x-auto'>
              <table className='w-full text-sm min-w-[500px]'>
                <thead className='text-left text-slate-500 border-b border-slate-200'>
                  <tr><th className='py-2'>Kode</th><th>Nama</th><th>Stok</th><th>Min</th><th>Status</th></tr>
                </thead>
                <tbody>
                  {filtered.map((m) => {
                    const low = isLowStock(m);
                    return (
                      <tr key={m.id} className={`border-b border-slate-100 ${low ? 'bg-red-50/50' : ''}`}>
                        <td className='py-2 text-slate-600'>{m.sku || m.code}</td>
                        <td className='text-slate-800'>{m.name}</td>
                        <td className='text-slate-700 font-medium'>{m.stock || 0} {m.unit?.name || ''}</td>
                        <td className='text-slate-600'>{m.min_stock || 0}</td>
                        <td>{low ? <span className='text-red-600 font-medium'>Menipis</span> : <span className='text-green-600'>Aman</span>}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Medicines;
