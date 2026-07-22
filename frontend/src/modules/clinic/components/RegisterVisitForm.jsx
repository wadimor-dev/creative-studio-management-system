import React, { useState } from 'react';
import { validateRegisterVisit } from '../helpers';

const inputCls =
  'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500';

const RegisterVisitForm = ({ employees = [], onSubmit, submitting }) => {
  const [employeeId, setEmployeeId] = useState('');
  const [complaint, setComplaint] = useState('');
  const [errors, setErrors] = useState([]);

  const activeEmployees = employees.filter((e) => e.is_active);
  const selected = employees.find((e) => e.id === Number(employeeId));

  const submit = (e) => {
    e.preventDefault();
    const payload = {
      employee_id: employeeId ? Number(employeeId) : null,
      complaint,
    };
    const errs = validateRegisterVisit(payload);
    setErrors(errs);
    if (errs.length) return;
    onSubmit?.(payload, () => {
      setEmployeeId('');
      setComplaint('');
    });
  };

  return (
    <form onSubmit={submit} className='space-y-3'>
      {errors.length > 0 && (
        <div className='bg-red-50 border border-red-200 rounded-lg p-2.5'>
          <ul className='text-red-600 text-sm list-disc pl-5'>
            {errors.map((er, i) => (
              <li key={i}>{er}</li>
            ))}
          </ul>
        </div>
      )}
      <div>
        <label className='block text-sm mb-1 text-slate-600'>Karyawan</label>
        <select
          value={employeeId}
          onChange={(e) => setEmployeeId(e.target.value)}
          className={inputCls}
        >
          <option value=''>— pilih karyawan —</option>
          {activeEmployees.map((e) => (
            <option key={e.id} value={e.id}>
              {e.employee_no} — {e.full_name}
            </option>
          ))}
        </select>
        {selected && (
          <div className='mt-2 flex items-center gap-2 text-xs'>
            <span className='px-2 py-0.5 rounded-full bg-brand-50 text-brand-700 font-medium'>
              {selected.department || 'Tanpa departemen'}
            </span>
            <span className='text-slate-400'>No. {selected.employee_no}</span>
          </div>
        )}
      </div>
      <div>
        <label className='block text-sm mb-1 text-slate-600'>Keluhan</label>
        <textarea
          value={complaint}
          onChange={(e) => setComplaint(e.target.value)}
          rows={3}
          className={inputCls}
          placeholder='Contoh: Pusing & demam sejak pagi'
        />
      </div>
      <button
        type='submit'
        disabled={submitting}
        className='w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'
      >
        {submitting ? 'Mendaftar…' : 'Daftar Kunjungan'}
      </button>
    </form>
  );
};

export default RegisterVisitForm;
