import React, { useMemo, useState } from 'react';
import { Plus, Search, X } from 'lucide-react';
import { usePatientProfiles, useCreatePatientProfile, useUpdatePatientProfile, useDeletePatientProfile } from '../hooks';
import { formatDate } from '../helpers';

const EMPTY_FORM = { employee_id: '', medical_record_number: '', blood_type: '', rhesus: '', allergy_note: '', emergency_contact_name: '', emergency_contact_phone: '' };

const Patients = () => {
  const { data, isLoading } = usePatientProfiles({ limit: 200 });
  const createPatient = useCreatePatientProfile();
  const updatePatient = useUpdatePatientProfile();
  const deletePatient = useDeletePatientProfile();

  const [q, setQ] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);

  const list = useMemo(() => {
    const p = Array.isArray(data) ? data : data?.data || data?.items || [];
    return p;
  }, [data]);

  const filtered = useMemo(() =>
    list.filter(p => !q || `${p.employee_name || ''} ${p.medical_record_number || ''}`.toLowerCase().includes(q.toLowerCase())), [list, q]);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const reset = () => { setForm(EMPTY_FORM); setEditingId(null); setShowForm(false); };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!form.employee_id || !form.medical_record_number) return;
    if (editingId) {
      updatePatient.mutate({ id: editingId, ...form }, { onSuccess: reset });
    } else {
      createPatient.mutate(form, { onSuccess: reset });
    }
  };

  const startEdit = (p) => {
    setForm({
      employee_id: p.employee_id,
      medical_record_number: p.medical_record_number,
      blood_type: p.blood_type || '',
      rhesus: p.rhesus || '',
      allergy_note: p.allergy_note || '',
      emergency_contact_name: p.emergency_contact_name || '',
      emergency_contact_phone: p.emergency_contact_phone || '',
    });
    setEditingId(p.id);
    setShowForm(true);
  };

  const fc = 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500';

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-5xl'>
      <div className='flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3'>
        <div>
          <h1 className='text-xl font-semibold text-slate-800'>Pasien</h1>
          <p className='text-slate-500 text-sm'>Master data pasien (dihubungkan ke data karyawan).</p>
        </div>
        <button onClick={() => { reset(); setShowForm(s => !s); }} className='inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 self-start'>
          <Plus className='w-4 h-4' /> {showForm ? 'Tutup' : 'Tambah Pasien'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm grid grid-cols-2 md:grid-cols-3 gap-3'>
          <div className='col-span-2 md:col-span-1'>
            <label className='block text-xs text-slate-500 mb-0.5'>ID Karyawan</label>
            <input value={form.employee_id} onChange={(e) => set('employee_id', e.target.value)} className={fc} placeholder='1' required />
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>No. RM</label>
            <input value={form.medical_record_number} onChange={(e) => set('medical_record_number', e.target.value)} className={fc} placeholder='RM-001' required />
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>Gol. Darah</label>
            <select value={form.blood_type} onChange={(e) => set('blood_type', e.target.value)} className={fc}>
              <option value=''>—</option>
              <option value='A'>A</option><option value='B'>B</option><option value='AB'>AB</option><option value='O'>O</option>
            </select>
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>Rhesus</label>
            <select value={form.rhesus} onChange={(e) => set('rhesus', e.target.value)} className={fc}>
              <option value=''>—</option>
              <option value='POSITIVE'>+</option><option value='NEGATIVE'>-</option>
            </select>
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>Alergi</label>
            <input value={form.allergy_note} onChange={(e) => set('allergy_note', e.target.value)} className={fc} />
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>Kontak Darurat</label>
            <input value={form.emergency_contact_name} onChange={(e) => set('emergency_contact_name', e.target.value)} className={fc} />
          </div>
          <div>
            <label className='block text-xs text-slate-500 mb-0.5'>No. Kontak</label>
            <input value={form.emergency_contact_phone} onChange={(e) => set('emergency_contact_phone', e.target.value)} className={fc} />
          </div>
          <div className='col-span-full flex gap-2'>
            <button type='submit' disabled={createPatient.isPending || updatePatient.isPending}
              className='px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'>
              {createPatient.isPending || updatePatient.isPending ? 'Menyimpan…' : editingId ? 'Update' : 'Simpan'}
            </button>
            <button type='button' onClick={reset} className='px-4 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100'>Batal</button>
          </div>
        </form>
      )}

      <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm space-y-4'>
        <div className='relative'>
          <Search className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400' />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder='Cari pasien…' className='w-full border border-slate-300 rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500' />
        </div>

        {isLoading ? (
          <div className='h-24 bg-slate-100 rounded animate-pulse' />
        ) : filtered.length === 0 ? (
          <p className='text-slate-500 text-sm py-4'>Belum ada data pasien.</p>
        ) : (
          <div className='overflow-x-auto'>
            <table className='w-full text-sm'>
              <thead className='text-left text-slate-500 border-b border-slate-200'>
                <tr><th className='py-2'>No. RM</th><th>Nama</th><th>Gol. Darah</th><th>Rhesus</th><th>Alergi</th><th>Dibuat</th><th></th></tr>
              </thead>
              <tbody>
                {filtered.map((p) => (
                  <tr key={p.id} className='border-b border-slate-100 hover:bg-slate-50'>
                    <td className='py-2 font-medium'>{p.medical_record_number}</td>
                    <td>{p.employee_name || '—'}</td>
                    <td>{p.blood_type || '—'}</td>
                    <td>{p.rhesus === 'POSITIVE' ? '+' : p.rhesus === 'NEGATIVE' ? '-' : '—'}</td>
                    <td className='max-w-[150px] truncate text-slate-500'>{p.allergy_note || '—'}</td>
                    <td className='text-slate-400 text-xs'>{p.created_at ? formatDate(p.created_at) : '—'}</td>
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

export default Patients;
