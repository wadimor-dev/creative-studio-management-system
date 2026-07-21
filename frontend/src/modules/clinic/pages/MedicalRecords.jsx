import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, FileText, ArrowRight, User } from 'lucide-react';
import { useVisits, useMedicines, useCompleteMedicalRecord } from '../hooks';
import { MedicalRecordForm } from '../components';
import { CLINIC_ROUTES, VISIT_STATUS } from '../constants';
import { formatTime } from '../helpers';

const MedicalRecords = () => {
  const navigate = useNavigate();
  const visits = useVisits();
  const medicines = useMedicines();
  const completeRecord = useCompleteMedicalRecord();
  const [selectedId, setSelectedId] = useState(null);

  const inProgress = (visits.data || []).filter(
    (v) => v.status === VISIT_STATUS.IN_PROGRESS,
  );
  const selected = inProgress.find((v) => v.id === selectedId) || null;

  const handleSubmit = (payload) => {
    completeRecord.mutate(
      { recordId: selected.medical_record_id, payload },
      { onSuccess: () => setSelectedId(null) },
    );
  };

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-6xl'>
      <div>
        <h1 className='text-xl font-semibold text-slate-800'>Rekam Medis</h1>
        <p className='text-slate-500 text-sm'>
          Isi catatan SOAP &amp; obat untuk pasien yang sedang diperiksa.
          Menyimpan akan mengurangi stok obat dan menyelesaikan kunjungan.
        </p>
      </div>

      <div className='grid md:grid-cols-3 gap-4 md:gap-6'>
        {/* Kiri: pasien diperiksa */}
        <div className='md:col-span-1'>
          <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <div className='flex items-center justify-between mb-3'>
              <h2 className='font-semibold text-slate-800'>Sedang Diperiksa</h2>
              <span className='text-xs px-2 py-0.5 rounded-full bg-brand-50 text-brand-700 font-medium'>
                {inProgress.length}
              </span>
            </div>
            {visits.isLoading ? (
              <div className='space-y-2'>
                {Array.from({ length: 3 }).map((_, i) => (
                  <div
                    key={i}
                    className='h-16 rounded-lg bg-slate-100 animate-pulse'
                  />
                ))}
              </div>
            ) : inProgress.length === 0 ? (
              <div className='text-center py-8 text-slate-400'>
                <Clock className='w-9 h-9 mx-auto mb-2 opacity-40' />
                <p className='text-sm'>Belum ada pasien diperiksa.</p>
                <button
                  onClick={() => navigate(CLINIC_ROUTES.queue)}
                  className='mt-2 inline-flex items-center gap-1 text-brand-600 text-sm hover:underline'
                >
                  Panggil dari Antrian <ArrowRight className='w-3.5 h-3.5' />
                </button>
              </div>
            ) : (
              <ul className='space-y-2'>
                {inProgress.map((v) => (
                  <li key={v.id}>
                    <button
                      onClick={() => setSelectedId(v.id)}
                      className={`w-full text-left border rounded-lg p-3 transition ${
                        selectedId === v.id
                          ? 'border-brand-500 bg-brand-50 ring-1 ring-brand-500'
                          : 'border-slate-200 hover:bg-slate-50'
                      }`}
                    >
                      <div className='flex items-center gap-2'>
                        <span className='w-8 h-8 rounded-lg bg-white border border-slate-200 text-brand-700 font-bold grid place-items-center text-sm shrink-0'>
                          #{v.queue_no}
                        </span>
                        <div className='min-w-0'>
                          <div className='font-medium text-slate-800 truncate'>
                            {v.employee_name}
                          </div>
                          <div className='text-xs text-slate-500 truncate'>
                            {v.complaint}
                          </div>
                        </div>
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        {/* Kanan: form rekam medis */}
        <div className='md:col-span-2'>
          {selected ? (
            <div className='bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden'>
              {/* Header pasien */}
              <div className='bg-gradient-to-r from-slate-800 to-slate-900 text-white p-4 md:p-5'>
                <div className='flex items-center gap-3'>
                  <span className='w-11 h-11 rounded-xl bg-white/15 grid place-items-center font-bold'>
                    #{selected.queue_no}
                  </span>
                  <div className='min-w-0'>
                    <div className='font-semibold truncate flex items-center gap-2'>
                      <User className='w-4 h-4' /> {selected.employee_name}
                    </div>
                    <div className='text-slate-300 text-sm'>
                      {selected.visit_no} · masuk{' '}
                      {formatTime(selected.created_at)}
                    </div>
                  </div>
                </div>
                {selected.complaint && (
                  <div className='mt-3 text-sm bg-white/10 rounded-lg px-3 py-2'>
                    <span className='text-slate-300'>Keluhan: </span>
                    {selected.complaint}
                  </div>
                )}
              </div>
              {/* Form (remount per pasien via key → state bersih) */}
              <div className='p-4 md:p-5'>
                <MedicalRecordForm
                  key={selected.id}
                  visit={selected}
                  medicines={medicines.data || []}
                  submitting={completeRecord.isPending}
                  onSubmit={handleSubmit}
                />
              </div>
            </div>
          ) : (
            <div className='bg-white border border-dashed border-slate-300 rounded-xl p-10 text-center text-slate-400'>
              <FileText className='w-10 h-10 mx-auto mb-2 opacity-40' />
              <p className='text-sm'>
                Pilih pasien di kiri untuk mulai mengisi rekam medis.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MedicalRecords;
