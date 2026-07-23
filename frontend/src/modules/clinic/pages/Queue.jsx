import React, { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, Activity, ArrowRight, ClipboardList, User, CheckCircle } from 'lucide-react';
import { useQueues, useUpdateQueueStatus, useVisits, useStartServingVisit, useFinishVisit } from '../hooks';
import { CLINIC_ROUTES, QUEUE_STATUS } from '../constants';
import { formatTime, queueStatusLabel } from '../helpers';

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

const QueueNo = ({ n, tone = 'slate' }) => (
  <div className={`w-12 h-12 rounded-xl grid place-items-center shrink-0 font-bold ${tone === 'brand-solid' ? 'bg-brand-600 text-white' : tone === 'brand' ? 'bg-brand-50 text-brand-700' : 'bg-slate-100 text-slate-700'}`}>
    <div className='text-center leading-none'>
      <div className='text-[9px] opacity-70'>NO</div>
      <div className='text-base'>{n}</div>
    </div>
  </div>
);

const Queue = () => {
  const navigate = useNavigate();
  const { data: queuesData, isLoading } = useQueues({ limit: 50 });
  const updateQueueStatus = useUpdateQueueStatus();
  const startServing = useStartServingVisit();
  const finishVisit = useFinishVisit();
  const { data: visitsData } = useVisits({ limit: 50 });

  const allQueues = useMemo(() => {
    const q = Array.isArray(queuesData) ? queuesData : queuesData?.data || queuesData?.items || [];
    return q.filter(item => item.queue_date && new Date(item.queue_date).toDateString() === new Date().toDateString());
  }, [queuesData]);

  const allVisits = useMemo(() => {
    const v = Array.isArray(visitsData) ? visitsData : visitsData?.data || visitsData?.items || [];
    return v;
  }, [visitsData]);

  const waiting = useMemo(() => allQueues.filter(q => q.status === QUEUE_STATUS.WAITING).sort((a, b) => a.queue_number?.localeCompare?.(b.queue_number) || 0), [allQueues]);

  const serving = useMemo(() => {
    const qIds = allQueues.filter(q => q.status === QUEUE_STATUS.SERVING).map(q => q.id);
    return allVisits.filter(v => qIds.includes(v.queue_id));
  }, [allQueues, allVisits]);

  const doneToday = useMemo(() => allQueues.filter(q => q.status === QUEUE_STATUS.FINISHED).length, [allQueues]);

  const handleCall = (queue) => {
    const visit = allVisits.find(v => v.queue_id === queue.id);
    if (visit) {
      startServing.mutate(visit.id);
    } else {
      updateQueueStatus.mutate({ id: queue.id, status: QUEUE_STATUS.CALLING });
    }
  };

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-6xl'>
      <div className='rounded-xl bg-gradient-to-r from-slate-800 to-slate-900 text-white p-5 shadow-sm'>
        <h1 className='text-xl font-semibold'>Antrian</h1>
        <p className='text-slate-300 text-sm mt-1'>Panggil pasien sesuai urutan untuk mulai pemeriksaan.</p>
      </div>

      <div className='grid grid-cols-3 gap-3'>
        <StatChip icon={Clock} label='Menunggu' value={waiting.length} accent='bg-amber-100 text-amber-700' />
        <StatChip icon={Activity} label='Diperiksa' value={serving.length} accent='bg-brand-100 text-brand-700' />
        <StatChip icon={ClipboardList} label='Selesai hari ini' value={doneToday} accent='bg-green-100 text-green-700' />
      </div>

      <div className='grid md:grid-cols-2 gap-4 md:gap-6'>
        <div className='bg-white border border-slate-200 rounded-xl shadow-sm'>
          <div className='flex items-center justify-between px-4 md:px-5 py-3 border-b border-slate-100'>
            <h2 className='font-semibold text-slate-800 flex items-center gap-2'>
              <Clock className='w-4 h-4 text-amber-600' /> Menunggu
            </h2>
            <span className='text-xs font-medium bg-amber-50 text-amber-700 px-2 py-0.5 rounded-full'>{waiting.length}</span>
          </div>
          <div className='p-4 md:p-5'>
            {isLoading ? (
              <div className='space-y-2'>{Array.from({ length: 3 }).map((_, i) => <div key={i} className='h-20 rounded-lg bg-slate-100 animate-pulse' />)}</div>
            ) : waiting.length === 0 ? (
              <div className='text-center py-10 text-slate-400 text-sm'>
                <Clock className='w-8 h-8 mx-auto mb-2 text-slate-300' />
                Tidak ada antrian menunggu.
              </div>
            ) : (
              <ul className='space-y-2.5'>
                {waiting.map((q, i) => (
                  <li key={q.id} className={`rounded-lg p-3 flex items-center gap-3 border transition ${i === 0 ? 'border-brand-500 bg-brand-50 ring-1 ring-brand-500' : 'border-slate-200 hover:border-slate-300'}`}>
                    <QueueNo n={q.queue_number?.replace(/^0+/, '') || q.queue_number} tone={i === 0 ? 'brand-solid' : 'slate'} />
                    <div className='min-w-0 flex-1'>
                      {i === 0 && <span className='text-[10px] font-semibold text-brand-700 uppercase tracking-wide'>Berikutnya</span>}
                      <div className='font-medium text-slate-800 truncate'>{q.patient_name || `Antrian ${q.queue_number}`}</div>
                    </div>
                    <button onClick={() => handleCall(q)} disabled={updateQueueStatus.isPending || startServing.isPending}
                      className={`inline-flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium shrink-0 disabled:opacity-50 ${i === 0 ? 'bg-brand-600 text-white hover:bg-brand-700' : 'bg-slate-800 text-white hover:bg-slate-900'}`}>
                      Panggil <ArrowRight className='w-3.5 h-3.5' />
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className='bg-white border border-slate-200 rounded-xl shadow-sm'>
          <div className='flex items-center justify-between px-4 md:px-5 py-3 border-b border-slate-100'>
            <h2 className='font-semibold text-slate-800 flex items-center gap-2'>
              <Activity className='w-4 h-4 text-brand-600' /> Sedang Diperiksa
            </h2>
            <span className='text-xs font-medium bg-brand-50 text-brand-700 px-2 py-0.5 rounded-full'>{serving.length}</span>
          </div>
          <div className='p-4 md:p-5'>
            {isLoading ? (
              <div className='space-y-2'>{Array.from({ length: 2 }).map((_, i) => <div key={i} className='h-20 rounded-lg bg-slate-100 animate-pulse' />)}</div>
            ) : serving.length === 0 ? (
              <div className='text-center py-10 text-slate-400 text-sm'>
                <Activity className='w-8 h-8 mx-auto mb-2 text-slate-300' />
                Belum ada pasien yang diperiksa.
              </div>
            ) : (
              <ul className='space-y-2.5'>
                {serving.map((v) => (
                  <li key={v.id} className='rounded-lg p-3 flex items-center gap-3 border border-slate-200'>
                    <QueueNo n={v.queue_number?.replace(/^0+/, '') || v.queue_number} tone='brand' />
                    <div className='min-w-0 flex-1'>
                      <div className='font-medium text-slate-800 truncate flex items-center gap-1'>
                        <User className='w-3.5 h-3.5 text-slate-400' /> {v.patient_name || `Visit ${v.visit_number}`}
                      </div>
                      {v.complaint && <div className='text-xs text-slate-500 truncate'>{v.complaint}</div>}
                      <div className='text-[11px] text-slate-400 mt-0.5'>mulai {formatTime(v.visit_date)}</div>
                    </div>
                    <div className='flex gap-1.5'>
                      <button onClick={() => navigate(CLINIC_ROUTES.medicalRecords)} className='inline-flex items-center gap-1 px-3 py-2 rounded-lg bg-slate-800 text-white text-sm font-medium hover:bg-slate-900 shrink-0'>
                        Rekam Medis <ArrowRight className='w-3.5 h-3.5' />
                      </button>
                      <button onClick={() => finishVisit.mutate(v.id)} disabled={finishVisit.isPending}
                        className='inline-flex items-center gap-1 px-3 py-2 rounded-lg bg-green-600 text-white text-sm font-medium hover:bg-green-700 disabled:opacity-50 shrink-0'>
                        <CheckCircle className='w-4 h-4' />
                        {finishVisit.isPending ? '…' : 'Selesai'}
                      </button>
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

export default Queue;
