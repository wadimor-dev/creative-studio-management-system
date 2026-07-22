import React, { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, Activity, ArrowRight, ClipboardList } from 'lucide-react';
import { useVisits, useUpdateVisitStatus } from '../hooks';
import { CLINIC_ROUTES, VISIT_STATUS } from '../constants';
import { formatTime } from '../helpers';

const waitMinutes = (iso) =>
  Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));

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

const QueueNo = ({ n, tone = 'slate' }) => (
  <div
    className={`w-12 h-12 rounded-xl grid place-items-center shrink-0 font-bold ${tone === 'brand-solid' ? 'bg-brand-600 text-white' : tone === 'brand' ? 'bg-brand-50 text-brand-700' : 'bg-slate-100 text-slate-700'}`}
  >
    <div className='text-center leading-none'>
      <div className='text-[9px] opacity-70'>NO</div>
      <div className='text-base'>{n}</div>
    </div>
  </div>
);

const Queue = () => {
  const navigate = useNavigate();
  const visits = useVisits();
  const updateStatus = useUpdateVisitStatus();

  const list = visits.data || [];
  const waiting = useMemo(
    () =>
      list
        .filter((v) => v.status === VISIT_STATUS.WAITING)
        .sort((a, b) => a.queue_no - b.queue_no),
    [list],
  );
  const inProgress = useMemo(
    () => list.filter((v) => v.status === VISIT_STATUS.IN_PROGRESS),
    [list],
  );
  const doneToday = useMemo(
    () => list.filter((v) => v.status === VISIT_STATUS.COMPLETED).length,
    [list],
  );

  const call = (v) =>
    updateStatus.mutate({ id: v.id, status: VISIT_STATUS.IN_PROGRESS });

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-6xl'>
      {/* Header */}
      <div className='rounded-xl bg-gradient-to-r from-slate-800 to-slate-900 text-white p-5 shadow-sm'>
        <h1 className='text-xl font-semibold'>Antrian</h1>
        <p className='text-slate-300 text-sm mt-1'>
          Panggil pasien sesuai urutan untuk mulai pemeriksaan.
        </p>
      </div>

      {/* Ringkasan */}
      <div className='grid grid-cols-3 gap-3'>
        <StatChip
          icon={Clock}
          label='Menunggu'
          value={waiting.length}
          accent='bg-amber-100 text-amber-700'
        />
        <StatChip
          icon={Activity}
          label='Diperiksa'
          value={inProgress.length}
          accent='bg-brand-100 text-brand-700'
        />
        <StatChip
          icon={ClipboardList}
          label='Selesai hari ini'
          value={doneToday}
          accent='bg-green-100 text-green-700'
        />
      </div>

      <div className='grid md:grid-cols-2 gap-4 md:gap-6'>
        {/* Menunggu */}
        <div className='bg-white border border-slate-200 rounded-xl shadow-sm'>
          <div className='flex items-center justify-between px-4 md:px-5 py-3 border-b border-slate-100'>
            <h2 className='font-semibold text-slate-800 flex items-center gap-2'>
              <Clock className='w-4 h-4 text-amber-600' /> Menunggu
            </h2>
            <span className='text-xs font-medium bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full'>
              {waiting.length}
            </span>
          </div>
          <div className='p-4 md:p-5'>
            {visits.isLoading ? (
              <div className='space-y-2'>
                {Array.from({ length: 3 }).map((_, i) => (
                  <div
                    key={i}
                    className='h-20 rounded-lg bg-slate-100 animate-pulse'
                  />
                ))}
              </div>
            ) : waiting.length === 0 ? (
              <div className='text-center py-10 text-slate-400 text-sm'>
                <Clock className='w-8 h-8 mx-auto mb-2 text-slate-300' />
                Tidak ada pasien menunggu.
              </div>
            ) : (
              <ul className='space-y-2.5'>
                {waiting.map((v, i) => {
                  const isNext = i === 0;
                  return (
                    <li
                      key={v.id}
                      className={`rounded-lg p-3 flex items-center gap-3 border transition ${
                        isNext
                          ? 'border-brand-500 bg-brand-50 ring-1 ring-brand-500'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <QueueNo
                        n={v.queue_no}
                        tone={isNext ? 'brand-solid' : 'slate'}
                      />
                      <div className='min-w-0 flex-1'>
                        {isNext && (
                          <span className='text-[10px] font-semibold text-brand-700 uppercase tracking-wide'>
                            Berikutnya
                          </span>
                        )}
                        <div className='font-medium text-slate-800 truncate'>
                          {v.employee_name}
                        </div>
                        <div className='text-xs text-slate-500 truncate'>
                          {v.complaint || 'Tanpa keluhan'}
                        </div>
                        <div className='text-[11px] text-slate-400 mt-0.5 flex items-center gap-1'>
                          <Clock className='w-3 h-3' /> menunggu{' '}
                          {waitMinutes(v.created_at)} mnt
                        </div>
                      </div>
                      <button
                        onClick={() => call(v)}
                        disabled={updateStatus.isPending}
                        className={`inline-flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium shrink-0 disabled:opacity-50 ${
                          isNext
                            ? 'bg-brand-600 text-white hover:bg-brand-700'
                            : 'bg-slate-800 text-white hover:bg-slate-900'
                        }`}
                      >
                        Panggil <ArrowRight className='w-3.5 h-3.5' />
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        </div>

        {/* Sedang diperiksa */}
        <div className='bg-white border border-slate-200 rounded-xl shadow-sm'>
          <div className='flex items-center justify-between px-4 md:px-5 py-3 border-b border-slate-100'>
            <h2 className='font-semibold text-slate-800 flex items-center gap-2'>
              <Activity className='w-4 h-4 text-brand-600' /> Sedang Diperiksa
            </h2>
            <span className='text-xs font-medium bg-brand-50 text-brand-700 px-2 py-0.5 rounded-full'>
              {inProgress.length}
            </span>
          </div>
          <div className='p-4 md:p-5'>
            {visits.isLoading ? (
              <div className='space-y-2'>
                {Array.from({ length: 2 }).map((_, i) => (
                  <div
                    key={i}
                    className='h-20 rounded-lg bg-slate-100 animate-pulse'
                  />
                ))}
              </div>
            ) : inProgress.length === 0 ? (
              <div className='text-center py-10 text-slate-400 text-sm'>
                <Activity className='w-8 h-8 mx-auto mb-2 text-slate-300' />
                Belum ada pasien yang diperiksa.
              </div>
            ) : (
              <ul className='space-y-2.5'>
                {inProgress.map((v) => (
                  <li
                    key={v.id}
                    className='rounded-lg p-3 flex items-center gap-3 border border-slate-200'
                  >
                    <QueueNo n={v.queue_no} tone='brand' />
                    <div className='min-w-0 flex-1'>
                      <div className='font-medium text-slate-800 truncate'>
                        {v.employee_name}
                      </div>
                      <div className='text-xs text-slate-500 truncate'>
                        {v.complaint || 'Tanpa keluhan'}
                      </div>
                      <div className='text-[11px] text-slate-400 mt-0.5'>
                        masuk {formatTime(v.created_at)}
                      </div>
                    </div>
                    <button
                      onClick={() => navigate(CLINIC_ROUTES.medicalRecords)}
                      className='inline-flex items-center gap-1 px-3 py-2 rounded-lg bg-slate-800 text-white text-sm font-medium hover:bg-slate-900 shrink-0'
                    >
                      Rekam Medis <ArrowRight className='w-3.5 h-3.5' />
                    </button>
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

export default Queue;
