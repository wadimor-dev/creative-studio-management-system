import React, { useMemo, useState } from 'react';
import { Plus, X, Pill, CheckCircle2 } from 'lucide-react';
import { validateMedicalRecord } from '../helpers';

const emptyItem = { medicine_id: '', qty: 1 };
const inputCls =
  'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500';

const SOAP = [
  { key: 'subjective', label: 'Subjective', hint: 'Keluhan pasien' },
  { key: 'objective', label: 'Objective', hint: 'Hasil pemeriksaan' },
  { key: 'assessment', label: 'Assessment', hint: 'Diagnosis' },
  { key: 'plan', label: 'Plan', hint: 'Tindakan / anjuran' },
];

const MedicalRecordForm = ({ visit, medicines = [], onSubmit, submitting }) => {
  const [soap, setSoap] = useState({
    subjective: visit?.complaint || '', // prefilled dari keluhan kunjungan
    objective: '',
    assessment: '',
    plan: '',
  });
  const [items, setItems] = useState([]);
  const [errors, setErrors] = useState([]);

  const setField = (k, v) => setSoap((s) => ({ ...s, [k]: v }));
  const addItem = () => setItems((it) => [...it, { ...emptyItem }]);
  const updateItem = (i, k, v) =>
    setItems((it) =>
      it.map((row, idx) => (idx === i ? { ...row, [k]: v } : row)),
    );
  const removeItem = (i) => setItems((it) => it.filter((_, idx) => idx !== i));

  const selectedCount = useMemo(
    () => items.filter((it) => it.medicine_id).length,
    [items],
  );

  const submit = (e) => {
    e.preventDefault();
    const cleanItems = items
      .filter((it) => it.medicine_id)
      .map((it) => ({
        medicine_id: Number(it.medicine_id),
        qty: Number(it.qty),
      }));
    const errs = validateMedicalRecord({ items: cleanItems }, medicines);
    setErrors(errs);
    if (errs.length) return;
    onSubmit?.({ ...soap, items: cleanItems });
  };

  return (
    <form onSubmit={submit} className='space-y-4'>
      {errors.length > 0 && (
        <div className='bg-red-50 border border-red-200 rounded-lg p-2.5'>
          <ul className='text-red-600 text-sm list-disc pl-5'>
            {errors.map((er, i) => (
              <li key={i}>{er}</li>
            ))}
          </ul>
        </div>
      )}

      {/* SOAP */}
      <div className='grid sm:grid-cols-2 gap-3'>
        {SOAP.map(({ key, label, hint }) => (
          <div key={key}>
            <label className='block text-sm mb-1 text-slate-700 font-medium'>
              {label}{' '}
              <span className='text-slate-400 font-normal'>· {hint}</span>
            </label>
            <textarea
              value={soap[key]}
              onChange={(e) => setField(key, e.target.value)}
              rows={3}
              className={inputCls}
            />
          </div>
        ))}
      </div>

      {/* Obat */}
      <div className='border-t border-slate-100 pt-3'>
        <div className='flex items-center justify-between mb-2'>
          <label className='text-sm font-medium text-slate-700 flex items-center gap-1.5'>
            <Pill className='w-4 h-4 text-brand-600' /> Obat diberikan
            {selectedCount > 0 && (
              <span className='text-xs text-slate-400'>({selectedCount})</span>
            )}
          </label>
          <button
            type='button'
            onClick={addItem}
            className='inline-flex items-center gap-1 text-brand-600 text-sm hover:underline'
          >
            <Plus className='w-3.5 h-3.5' /> Tambah obat
          </button>
        </div>

        {items.length === 0 && (
          <p className='text-slate-400 text-sm bg-slate-50 border border-dashed border-slate-200 rounded-lg p-3 text-center'>
            Belum ada obat. Klik “Tambah obat” bila pasien perlu obat.
          </p>
        )}

        <div className='space-y-2'>
          {items.map((it, i) => {
            const med = medicines.find((m) => m.id === Number(it.medicine_id));
            const qty = Number(it.qty) || 0;
            const over = med && qty > med.stock;
            const after = med ? med.stock - qty : null;
            return (
              <div
                key={i}
                className='flex flex-wrap sm:flex-nowrap gap-2 items-center bg-slate-50 rounded-lg p-2'
              >
                <select
                  value={it.medicine_id}
                  onChange={(e) => updateItem(i, 'medicine_id', e.target.value)}
                  className='flex-1 min-w-[140px] border border-slate-300 rounded-lg px-2 py-1.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-brand-500'
                >
                  <option value=''>— pilih obat —</option>
                  {medicines.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.name} (stok {m.stock})
                    </option>
                  ))}
                </select>
                <input
                  type='number'
                  min={1}
                  value={it.qty}
                  onChange={(e) => updateItem(i, 'qty', e.target.value)}
                  className={`w-20 border rounded-lg px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 ${over ? 'border-red-500' : 'border-slate-300'}`}
                />
                <div className='text-xs w-24 shrink-0'>
                  {med ? (
                    over ? (
                      <span className='text-red-600 font-medium'>
                        &gt; stok ({med.stock})
                      </span>
                    ) : (
                      <span className='text-slate-500'>
                        sisa: {after} {med.unit}
                      </span>
                    )
                  ) : (
                    <span className='text-slate-300'>—</span>
                  )}
                </div>
                <button
                  type='button'
                  onClick={() => removeItem(i)}
                  className='text-slate-400 hover:text-red-600'
                >
                  <X className='w-4 h-4' />
                </button>
              </div>
            );
          })}
        </div>
      </div>

      <button
        type='submit'
        disabled={submitting}
        className='w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'
      >
        <CheckCircle2 className='w-4 h-4' />
        {submitting ? 'Menyimpan…' : 'Simpan & Selesaikan Kunjungan'}
      </button>
    </form>
  );
};

export default MedicalRecordForm;
