import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, FileText } from 'lucide-react';
import {
  useEmployees,
  useVisits,
  useRegisterVisit,
  useUpdateVisitStatus,
} from '../hooks';
import { RegisterVisitForm, StatusBadge } from '../components';
import EmployeeImportExcel from '../components/EmployeeImportExcel';
import { CLINIC_ROUTES, VISIT_STATUS, VISIT_STATUS_LABEL } from '../constants';
import { formatTime } from '../helpers';

const FILTERS = [
  { key: 'ALL', label: 'Semua' },
  { key: VISIT_STATUS.WAITING, label: VISIT_STATUS_LABEL.WAITING },
  { key: VISIT_STATUS.IN_PROGRESS, label: VISIT_STATUS_LABEL.IN_PROGRESS },
  { key: VISIT_STATUS.COMPLETED, label: VISIT_STATUS_LABEL.COMPLETED },
];

const WORKFLOW = ['Daftar', 'Antrian', 'Diperiksa', 'Rekam Medis', 'Selesai'];

const Visits = () => {
  const navigate = useNavigate();
  const employees = useEmployees();
  const visits = useVisits();
  const registerVisit = useRegisterVisit();
  const updateStatus = useUpdateVisitStatus();

  const [filter, setFilter] = useState('ALL');
  const [q, setQ] = useState('');
  const [lastReg, setLastReg] = useState(null);

  const list = visits.data || [];

  const counts = useMemo(() => {
    const c = { ALL: list.length };
    for (const v of list) c[v.status] = (c[v.status] || 0) + 1;
    return c;
  }, [list]);

  const filtered = useMemo(
    () =>
      list.filter((v) => {
        const okStatus = filter === 'ALL' || v.status === filter;
        const okQ =
          !q ||
          `${v.employee_name} ${v.visit_no}`
            .toLowerCase()
            .includes(q.toLowerCase());
        return okStatus && okQ;
      }),
    [list, filter, q],
  );

  const handleRegister = (payload, reset) =>
    registerVisit.mutate(payload, {
      onSuccess: (res) => {
        setLastReg(res);
        reset();
      },
    });

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-6xl'>
      {/* Header + workflow stepper */}
      <div>
        <h1 className='text-xl font-semibold text-slate-800'>Kunjungan</h1>
        <p className='text-slate-500 text-sm'>
          Daftarkan karyawan berobat lalu pantau alurnya sampai selesai.
        </p>
        <div className='mt-3 flex items-center gap-1.5 flex-wrap text-xs'>
          {WORKFLOW.map((step, i) => (
            <React.Fragment key={step}>
              <span className='px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 font-medium'>
                {i + 1}. {step}
              </span>
              {i < WORKFLOW.length - 1 && (
                <ArrowRight className='w-3 h-3 text-slate-300' />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className='grid md:grid-cols-3 gap-4 md:gap-6'>
        {/* Kiri: form + kartu sukses */}
        <div className='md:col-span-1 space-y-4'>
          {/* ⬇️ KARTU FORM "Daftar Kunjungan Baru" — tombol Import Excel di kanan judul */}
          <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <div className='flex items-center justify-between mb-3'>
              <h2 className='font-semibold text-slate-800'>
                Daftar Kunjungan Baru
              </h2>
              <EmployeeImportExcel />
            </div>
            <RegisterVisitForm
              employees={employees.data || []}
              submitting={registerVisit.isPending}
              onSubmit={handleRegister}
            />
          </div>

          {lastReg && (
            <div className='bg-green-50 border border-green-200 rounded-xl p-4 shadow-sm'>
              <div className='flex items-center gap-2 text-green-700 font-medium'>
                <span className='w-5 h-5 rounded-full bg-green-600 text-white grid place-items-center text-xs'>
                  ✓
                </span>
                Kunjungan terdaftar
              </div>
              <div className='mt-2 flex items-center gap-3'>
                <div className='w-14 h-14 rounded-xl bg-green-600 text-white grid place-items-center'>
                  <div className='text-center leading-none'>
                    <div className='text-[10px]'>ANTRIAN</div>
                    <div className='text-xl font-bold'>#{lastReg.queue_no}</div>
                  </div>
                </div>
                <div className='text-sm text-slate-600'>
                  <div className='font-medium text-slate-800'>
                    {lastReg.visit?.employee_name}
                  </div>
                  <div>{lastReg.visit?.visit_no}</div>
                </div>
              </div>
              <button
                onClick={() => navigate(CLINIC_ROUTES.queue)}
                className='mt-3 w-full inline-flex items-center justify-center gap-1 text-green-700 text-sm hover:underline'
              >
                Lihat Antrian <ArrowRight className='w-3.5 h-3.5' />
              </button>
            </div>
          )}
        </div>

        {/* Kanan: cari + filter + daftar */}
        <div className='md:col-span-2'>
          <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            {/* Search (tanpa ikon, aman) */}
            <div className='mb-4'>
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder='🔍  Cari nama / no. kunjungan…'
                className='w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500'
              />
            </div>

            {/* Filter tabs */}
            <div className='flex gap-1.5 flex-wrap mb-4'>
              {FILTERS.map((f) => (
                <button
                  key={f.key}
                  onClick={() => setFilter(f.key)}
                  className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${
                    filter === f.key
                      ? 'bg-brand-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {f.label}
                  <span
                    className={`ml-1.5 ${filter === f.key ? 'text-white/80' : 'text-slate-400'}`}
                  >
                    {counts[f.key] || 0}
                  </span>
                </button>
              ))}
            </div>

            {/* Daftar kunjungan */}
            {visits.isLoading ? (
              <div className='space-y-2'>
                {Array.from({ length: 4 }).map((_, i) => (
                  <div
                    key={i}
                    className='h-16 rounded-lg bg-slate-100 animate-pulse'
                  />
                ))}
              </div>
            ) : filtered.length === 0 ? (
              <div className='text-center py-10 text-slate-400 text-sm'>
                Tidak ada kunjungan yang cocok.
              </div>
            ) : (
              <ul className='space-y-2'>
                {filtered.map((v) => (
                  <li
                    key={v.id}
                    className='border border-slate-200 rounded-lg p-3 flex flex-col sm:flex-row sm:items-center gap-3 hover:border-slate-300 transition'
                  >
                    <div className='flex items-center gap-3 flex-1 min-w-0'>
                      <span className='w-10 h-10 rounded-lg bg-brand-50 text-brand-700 font-bold grid place-items-center text-sm shrink-0'>
                        #{v.queue_no}
                      </span>
                      <div className='min-w-0'>
                        <div className='font-medium text-slate-800 truncate'>
                          {v.employee_name}
                        </div>
                        <div className='text-xs text-slate-500 truncate'>
                          {v.complaint}
                        </div>
                        <div className='text-xs text-slate-400 mt-0.5'>
                          {v.visit_no} · {formatTime(v.created_at)}
                        </div>
                      </div>
                    </div>
                    <div className='flex items-center justify-between sm:justify-end gap-2'>
                      <StatusBadge status={v.status} />
                      {v.status === VISIT_STATUS.WAITING && (
                        <button
                          onClick={() =>
                            updateStatus.mutate({
                              id: v.id,
                              status: VISIT_STATUS.IN_PROGRESS,
                            })
                          }
                          className='inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-brand-600 text-white text-xs font-medium hover:bg-brand-700'
                        >
                          Panggil
                        </button>
                      )}
                      {v.status === VISIT_STATUS.IN_PROGRESS && (
                        <button
                          onClick={() => navigate(CLINIC_ROUTES.medicalRecords)}
                          className='inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-slate-800 text-white text-xs font-medium hover:bg-slate-900'
                        >
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
