import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users, ClipboardList, Clock, Pill, Plus, ArrowRight, Activity, AlertTriangle,
} from 'lucide-react';
import { useClinicDashboard } from '../hooks';
import { CLINIC_ROUTES, VISIT_STATUS_LABEL } from '../constants';
import { formatDate, visitStatusLabel } from '../helpers';
import { useAuth } from '../../../contexts/AuthContext';

const StatCard = ({ icon: Icon, label, value, accent }) => (
  <div className='bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-4 shadow-sm hover:shadow transition'>
    <div className={`w-11 h-11 rounded-lg grid place-items-center ${accent}`}>
      <Icon className='w-5 h-5' />
    </div>
    <div>
      <div className='text-2xl font-bold leading-tight text-slate-800'>{value ?? '—'}</div>
      <div className='text-slate-500 text-sm'>{label}</div>
    </div>
  </div>
);

const BAR_COLOR = {
  CHECKIN: 'bg-amber-400',
  SERVING: 'bg-purple-400',
  FINISHED: 'bg-green-500',
  CANCELLED: 'bg-red-400',
};

const StatusBreakdown = ({ byStatus = {} }) => {
  const total = Object.values(byStatus).reduce((a, b) => a + (b || 0), 0);
  return (
    <div className='space-y-3'>
      {Object.keys(VISIT_STATUS_LABEL).map((s) => {
        const count = byStatus[s] || 0;
        const pct = total ? Math.round((count / total) * 100) : 0;
        return (
          <div key={s}>
            <div className='flex justify-between text-sm mb-1'>
              <span className='text-slate-600'>{visitStatusLabel(s)}</span>
              <span className='font-medium text-slate-700'>{count}</span>
            </div>
            <div className='h-2 rounded-full bg-slate-100 overflow-hidden'>
              <div className={`h-full ${BAR_COLOR[s] || 'bg-slate-400'}`} style={{ width: `${pct}%` }} />
            </div>
          </div>
        );
      })}
      {total === 0 && <p className='text-slate-400 text-sm'>Belum ada kunjungan hari ini.</p>}
    </div>
  );
};

const Dashboard = () => {
  const { data, isLoading } = useClinicDashboard();
  const navigate = useNavigate();
  const { user } = useAuth();
  const t = data?.totals;
  const todayQueue = data?.todayQueue || [];

  return (
    <div className='p-4 md:p-6 space-y-6 max-w-6xl'>
      <div className='rounded-2xl bg-gradient-to-r from-slate-800 to-slate-900 text-white p-5 md:p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4'>
        <div>
          <p className='text-slate-300 text-sm capitalize'>{formatDate(new Date())}</p>
          <h1 className='text-xl md:text-2xl font-semibold mt-0.5'>
            Selamat datang{user?.username ? `, ${user.username}` : ''}
          </h1>
          <p className='text-slate-300 text-sm mt-1'>Ringkasan aktivitas klinik hari ini</p>
        </div>
        <div className='flex gap-2'>
          <button onClick={() => navigate(CLINIC_ROUTES.visits)} className='inline-flex items-center gap-2 bg-white text-brand-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-50'>
            <Plus className='w-4 h-4' /> Daftar Kunjungan
          </button>
          <button onClick={() => navigate(CLINIC_ROUTES.queue)} className='inline-flex items-center gap-2 bg-white/10 border border-white/25 px-4 py-2 rounded-lg text-sm font-medium hover:bg-white/20'>
            <Clock className='w-4 h-4' /> Antrian
          </button>
        </div>
      </div>

      <div className='grid grid-cols-2 lg:grid-cols-4 gap-3'>
        {isLoading ? Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className='bg-white border border-slate-200 rounded-xl p-4 animate-pulse h-[76px]'>
            <div className='flex items-center gap-4 h-full'>
              <div className='w-11 h-11 rounded-lg bg-slate-200' />
              <div className='flex-1 space-y-2'>
                <div className='h-5 w-12 bg-slate-200 rounded' />
                <div className='h-3 w-24 bg-slate-100 rounded' />
              </div>
            </div>
          </div>
        )) : (
          <>
            <StatCard icon={Users} label='Pasien terdaftar' value={t?.patientsActive} accent='bg-brand-100 text-brand-700' />
            <StatCard icon={ClipboardList} label='Kunjungan hari ini' value={t?.visitsToday} accent='bg-green-100 text-green-700' />
            <StatCard icon={Clock} label='Menunggu' value={t?.waitingCount} accent='bg-amber-100 text-amber-700' />
            <StatCard icon={Activity} label='Diperiksa' value={t?.servingCount} accent='bg-purple-100 text-purple-700' />
          </>
        )}
      </div>

      <div className='grid md:grid-cols-3 gap-4'>
        <section className='md:col-span-2 bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
          <div className='flex justify-between items-center mb-3'>
            <h2 className='font-semibold text-slate-800 flex items-center gap-2'>
              <Activity className='w-4 h-4 text-brand-600' /> Antrian hari ini
            </h2>
            <button onClick={() => navigate(CLINIC_ROUTES.queue)} className='text-brand-600 text-sm inline-flex items-center gap-1 hover:underline'>
              Lihat semua <ArrowRight className='w-3.5 h-3.5' />
            </button>
          </div>
          {isLoading ? (
            <div className='space-y-2'>{Array.from({ length: 3 }).map((_, i) => <div key={i} className='h-12 rounded-lg bg-slate-100 animate-pulse' />)}</div>
          ) : todayQueue.length === 0 ? (
            <div className='text-center py-10 text-slate-400'>
              <ClipboardList className='w-10 h-10 mx-auto mb-2 opacity-40' />
              <p className='text-sm'>Belum ada antrian hari ini.</p>
            </div>
          ) : (
            <ul className='divide-y divide-slate-100'>
              {todayQueue.map((q) => (
                <li key={q.id} className='py-2.5 flex items-center gap-3'>
                  <span className='w-9 h-9 rounded-lg bg-brand-50 text-brand-700 font-bold grid place-items-center text-sm shrink-0'>
                    #{q.queue_number}
                  </span>
                  <div className='flex-1 min-w-0'>
                    <div className='font-medium text-slate-800 truncate'>{q.patient_name || `Queue ${q.queue_number}`}</div>
                  </div>
                  <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${q.status === 'WAITING' ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>
                    {q.status === 'WAITING' ? 'Menunggu' : 'Dipanggil'}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <div className='space-y-4'>
          <section className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <h2 className='font-semibold text-slate-800 mb-3'>Status kunjungan</h2>
            {isLoading ? <div className='h-24 bg-slate-100 rounded animate-pulse' /> : <StatusBreakdown byStatus={data?.visitsByStatus} />}
          </section>
          <section className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <h2 className='font-semibold text-slate-800 mb-3 flex items-center gap-2'>
              <AlertTriangle className='w-4 h-4 text-amber-600' /> Kunjungan terbaru
            </h2>
            {isLoading ? <div className='h-16 bg-slate-100 rounded animate-pulse' /> : !data?.todayVisits?.length ? (
              <p className='text-slate-400 text-sm'>Belum ada kunjungan</p>
            ) : (
              <ul className='space-y-2'>
                {data.todayVisits.map((v) => (
                  <li key={v.id} className='flex justify-between items-center text-sm'>
                    <span className='text-slate-700 truncate'>{v.patient_name || v.visit_number}</span>
                    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${v.visit_status === 'CHECKIN' ? 'bg-amber-100 text-amber-700' : v.visit_status === 'SERVING' ? 'bg-purple-100 text-purple-700' : 'bg-green-100 text-green-700'}`}>
                      {visitStatusLabel(v.visit_status)}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
