import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, FileText, Search } from 'lucide-react';
import { useVisits, usePatientProfiles, useCreateVisit, useCreateQueue, useStartServingVisit } from '../hooks';
import { StatusBadge } from '../components';
import { CLINIC_ROUTES, VISIT_STATUS, VISIT_STATUS_LABEL, VISIT_TYPE, VISIT_TYPE_LABEL } from '../constants';
import { formatTime, visitStatusLabel, visitStatusBadge } from '../helpers';

const FILTERS = [
  { key: 'ALL', label: 'Semua' },
  { key: VISIT_STATUS.CHECKIN, label: VISIT_STATUS_LABEL.CHECKIN },
  { key: VISIT_STATUS.SERVING, label: VISIT_STATUS_LABEL.SERVING },
  { key: VISIT_STATUS.FINISHED, label: VISIT_STATUS_LABEL.FINISHED },
];

const Visits = () => {
  const navigate = useNavigate();
  const { data: visitsData, isLoading } = useVisits({ limit: 100 });
  const { data: patientsData } = usePatientProfiles({ limit: 200 });
  const createVisit = useCreateVisit();
  const createQueue = useCreateQueue();
  const startServing = useStartServingVisit();

  const [filter, setFilter] = useState('ALL');
  const [q, setQ] = useState('');
  const [patientId, setPatientId] = useState('');
  const [complaint, setComplaint] = useState('');
  const [visitType, setVisitType] = useState(VISIT_TYPE.REGULAR);
  const [lastCreated, setLastCreated] = useState(null);

  const list = useMemo(() => {
    const v = Array.isArray(visitsData) ? visitsData : visitsData?.data || visitsData?.items || [];
    return v;
  }, [visitsData]);

  const patients = useMemo(() => {
    const p = Array.isArray(patientsData) ? patientsData : patientsData?.data || patientsData?.items || [];
    return p;
  }, [patientsData]);

  const counts = useMemo(() => {
    const c = { ALL: list.length };
    for (const v of list) c[v.visit_status] = (c[v.visit_status] || 0) + 1;
    return c;
  }, [list]);

  const filtered = useMemo(() =>
    list.filter((v) => {
      const okStatus = filter === 'ALL' || v.visit_status === filter;
      const okQ = !q || `${v.patient_name || ''} ${v.visit_number || ''}`.toLowerCase().includes(q.toLowerCase());
      return okStatus && okQ;
    }), [list, filter, q]);

  const selectedPatient = patients.find(p => p.id === patientId);

  const handleRegister = () => {
    if (!patientId) return;
    const today = new Date().toISOString().slice(0, 10);
    const queueNum = String(Date.now()).slice(-4);
    createQueue.mutate(
      { queue_number: queueNum, queue_date: today },
      {
        onSuccess: (queueRes) => {
          const queueId = queueRes?.id || queueRes?.data?.id;
          createVisit.mutate(
            { patient_profile_id: patientId, queue_id: queueId, visit_type: visitType, complaint },
            {
              onSuccess: (res) => {
                setLastCreated(res?.data || res);
                setPatientId('');
                setComplaint('');
                setVisitType(VISIT_TYPE.REGULAR);
              },
            }
          );
        },
      }
    );
  };

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-6xl'>
      <div>
        <h1 className='text-xl font-semibold text-slate-800'>Kunjungan</h1>
        <p className='text-slate-500 text-sm'>Daftarkan pasien, kelola antrian, dan pantau status kunjungan.</p>
      </div>

      <div className='grid md:grid-cols-3 gap-4 md:gap-6'>
        <div className='md:col-span-1 space-y-4'>
          <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <h2 className='font-semibold text-slate-800 mb-3'>Daftar Kunjungan Baru</h2>
            <div className='space-y-3'>
              <div>
                <label className='block text-sm mb-1 text-slate-600'>Pasien</label>
                <select value={patientId} onChange={(e) => setPatientId(e.target.value)}
                  className='w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500'>
                  <option value=''>— pilih pasien —</option>
                  {patients.map((p) => (
                    <option key={p.id} value={p.id}>{p.employee_name || p.medical_record_number}</option>
                  ))}
                </select>
                {selectedPatient && (
                  <div className='mt-1 text-xs text-slate-500'>RM: {selectedPatient.medical_record_number}</div>
                )}
              </div>
              <div>
                <label className='block text-sm mb-1 text-slate-600'>Jenis</label>
                <select value={visitType} onChange={(e) => setVisitType(e.target.value)}
                  className='w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500'>
                  {Object.entries(VISIT_TYPE_LABEL).map(([k, v]) => (
                    <option key={k} value={k}>{v}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className='block text-sm mb-1 text-slate-600'>Keluhan</label>
                <textarea value={complaint} onChange={(e) => setComplaint(e.target.value)}
                  rows={3} className='w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500'
                  placeholder='Contoh: Demam & batuk sejak 2 hari' />
              </div>
              <button onClick={handleRegister} disabled={!patientId || createQueue.isPending || createVisit.isPending}
                className='w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'>
                {createQueue.isPending || createVisit.isPending ? 'Mendaftar…' : 'Daftar Kunjungan'}
              </button>
            </div>
          </div>

          {lastCreated && (
            <div className='bg-green-50 border border-green-200 rounded-xl p-4 shadow-sm'>
              <div className='flex items-center gap-2 text-green-700 font-medium'>
                <span className='w-5 h-5 rounded-full bg-green-600 text-white grid place-items-center text-xs'>✓</span>
                Kunjungan terdaftar
              </div>
              <div className='mt-2 text-sm text-slate-600'>
                <div className='font-medium text-slate-800'>{lastCreated.patient_name || lastCreated.visit_number}</div>
                <div>{lastCreated.visit_number}</div>
              </div>
            </div>
          )}
        </div>

        <div className='md:col-span-2'>
          <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <div className='mb-4 relative'>
              <Search className='absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400' />
              <input value={q} onChange={(e) => setQ(e.target.value)}
                placeholder='Cari pasien / no. kunjungan…'
                className='w-full border border-slate-300 rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500' />
            </div>

            <div className='flex gap-1.5 flex-wrap mb-4'>
              {FILTERS.map((f) => (
                <button key={f.key} onClick={() => setFilter(f.key)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${filter === f.key ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}`}>
                  {f.label}
                  <span className={`ml-1.5 ${filter === f.key ? 'text-white/80' : 'text-slate-400'}`}>{counts[f.key] || 0}</span>
                </button>
              ))}
            </div>

            {isLoading ? (
              <div className='space-y-2'>{Array.from({ length: 4 }).map((_, i) => <div key={i} className='h-16 rounded-lg bg-slate-100 animate-pulse' />)}</div>
            ) : filtered.length === 0 ? (
              <div className='text-center py-10 text-slate-400 text-sm'>Tidak ada kunjungan yang cocok.</div>
            ) : (
              <ul className='space-y-2'>
                {filtered.map((v) => (
                  <li key={v.id} className='border border-slate-200 rounded-lg p-3 flex flex-col sm:flex-row sm:items-center gap-3 hover:border-slate-300 transition cursor-pointer'
                    onClick={() => navigate(CLINIC_ROUTES.visitDetail(v.id))}>
                    <div className='flex items-center gap-3 flex-1 min-w-0'>
                      <div className='w-10 h-10 rounded-lg bg-brand-50 text-brand-700 font-bold grid place-items-center text-sm shrink-0'>
                        #{v.queue_number || '—'}
                      </div>
                      <div className='min-w-0'>
                        <div className='font-medium text-slate-800 truncate'>{v.patient_name || 'Pasien'}</div>
                        {v.complaint && <div className='text-xs text-slate-500 truncate'>{v.complaint}</div>}
                        <div className='text-xs text-slate-400 mt-0.5'>{v.visit_number} · {formatTime(v.visit_date)}</div>
                      </div>
                    </div>
                    <div className='flex items-center justify-between sm:justify-end gap-2'>
                      <StatusBadge label={visitStatusLabel(v.visit_status)} className={visitStatusBadge(v.visit_status)} />
                      {v.visit_status === VISIT_STATUS.SERVING && (
                        <button onClick={(e) => { e.stopPropagation(); navigate(CLINIC_ROUTES.medicalRecords); }}
                          className='inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-800 text-white text-xs font-medium hover:bg-slate-900'>
                          <FileText className='w-3.5 h-3.5' /> Rekam Medis
                        </button>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Visits;
