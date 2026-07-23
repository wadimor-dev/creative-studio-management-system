import React, { useMemo, useState } from 'react';
import { Plus, Search } from 'lucide-react';
import { useHCProfessionals, useCreateHCProfessional, useUpdateHCProfessional, useDeleteHCProfessional } from '../hooks';
import { PROFESSION_LABEL } from '../constants';

const EMPTY = { employee_id: '', profession: 'DOCTOR', specialization: '', license_number: '' };

const HealthcareProfessionals = () => {
  const { data, isLoading } = useHCProfessionals({ limit: 200 });
  const create = useCreateHCProfessional();
  const update = useUpdateHCProfessional();
  const remove = useDeleteHCProfessional();

  const [q, setQ] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);

  const list = useMemo(() => {
    const p = Array.isArray(data) ? data : data?.data || data?.items || [];
    return p;
  }, [data]);

  const filtered = useMemo(() =>
    list.filter(p => !q || (p.employee_name || '').toLowerCase().includes(q.toLowerCase())), [list, q]);

  const reset = () => { setForm(EMPTY); setEditingId(null); setShowForm(false); };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.employee_id) return;
    if (editingId) {
      update.mutate({ id: editingId, ...form }, { onSuccess: reset });
    } else {
      create.mutate(form, { onSuccess: reset });
    }
  };

  const startEdit = (p) => {
    setForm({ employee_id: p.employee_id, profession: p.profession, specialization: p.specialization || '', license_number: p.license_number || '' });
    setEditingId(p.id);
    setShowForm(true);
  };

  const fc = 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500';

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-5xl'>
      <div className='flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3'>
        <div>
          <h1 className='text-xl font-semibold text-slate-800'>Tenaga Medis</h1>
          <p className='text-slate-500 text-sm'>Dokter, perawat, dan tenaga kesehatan lainnya.</p>
        </div>
        <button onClick={() => { reset(); setShowForm(s => !s); }} className='inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 self-start'>
          <Plus className='w-4 h-4' /> {showForm ? 'Tutup' : 'Tambah'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm grid grid-cols-2 md:grid-cols-4 gap-3'>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>ID Karyawan</label>
            <input value={form.employee_id} onChange={(e) => setForm(f => ({ ...f, employee_id: e.target.value }))} className={fc} required />
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>Profesi</label>
            <select value={form.profession} onChange={(e) => setForm(f => ({ ...f, profession: e.target.value }))} className={fc}>
              {Object.entries(PROFESSION_LABEL).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>Spesialisasi</label>
            <input value={form.specialization} onChange={(e) => setForm(f => ({ ...f, specialization: e.target.value }))} className={fc} />
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>No. Lisensi</label>
            <input value={form.license_number} onChange={(e) => setForm(f => ({ ...f, license_number: e.target.value }))} className={fc} />
          </div>
          <div className='col-span-full flex gap-2'>
            <button type='submit' disabled={create.isPending || update.isPending} className='px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'>
              {create.isPending || update.isPending ? 'Menyimpan…' : editingId ? 'Update' : 'Simpan'}
            </button>
            <button type='button' onClick={reset} className='px-4 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100'>Batal</button>
          </div>
        </form>
      )}

      <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm space-y-4'>
        <div className='relative'>
          <Search className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400' />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder='Cari tenaga medis…' className='w-full border border-slate-300 rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500' />
        </div>
        {isLoading ? (
          <div className='h-24 bg-slate-100 rounded animate-pulse' />
        ) : filtered.length === 0 ? (
          <p className='text-slate-500 text-sm py-4'>Belum ada data.</p>
        ) : (
          <div className='overflow-x-auto'>
            <table className='w-full text-sm'>
              <thead className='text-left text-slate-500 border-b border-slate-200'>
                <tr><th className='py-2'>Nama</th><th>Profesi</th><th>Spesialisasi</th><th>Lisensi</th><th></th></tr>
              </thead>
              <tbody>
                {filtered.map((p) => (
                  <tr key={p.id} className='border-b border-slate-100 hover:bg-slate-50'>
                    <td className='py-2 font-medium'>{p.employee_name || `ID ${p.employee_id}`}</td>
                    <td>{PROFESSION_LABEL[p.profession] || p.profession}</td>
                    <td className='text-slate-500'>{p.specialization || '—'}</td>
                    <td className='text-slate-500'>{p.license_number || '—'}</td>
                    <td className='text-right'>
                      <button onClick={() => startEdit(p)} className='text-brand-600 hover:underline text-xs'>Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default HealthcareProfessionals;
