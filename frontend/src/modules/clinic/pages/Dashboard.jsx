// frontend/src/modules/clinic/pages/Dashboard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  ClipboardList,
  Clock,
  Pill,
  Plus,
  ArrowRight,
  Activity,
  AlertTriangle,
} from 'lucide-react';
import { useClinicDashboard } from '../hooks';
import { StatusBadge } from '../components';
import { CLINIC_ROUTES, VISIT_STATUS_LABEL } from '../constants';
import { formatDate, visitStatusLabel } from '../helpers';
import { useAuth } from '../../../contexts/AuthContext'; // sesuaikan kalau pakai alias '@/'

/* ---------- sub-komponen ---------- */

const StatCard = ({ icon: Icon, label, value, accent }) => (
  <div className='bg-white border border-slate-200 rounded-xl p-4 flex items-center gap-4 shadow-sm hover:shadow transition'>
    <div className={`w-11 h-11 rounded-lg grid place-items-center ${accent}`}>
      <Icon className='w-5 h-5' />
    </div>
    <div>
      <div className='text-2xl font-bold leading-tight text-slate-800'>
        {value ?? '—'}
      </div>
      <div className='text-slate-500 text-sm'>{label}</div>
    </div>
  </div>
);

const BAR_COLOR = {
  WAITING: 'bg-amber-400',
  IN_PROGRESS: 'bg-purple-400',
  COMPLETED: 'bg-green-500',
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
              <div
                className={`h-full ${BAR_COLOR[s] || 'bg-slate-400'}`}
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        );
      })}
      {total === 0 && (
        <p className='text-slate-400 text-sm'>Belum ada kunjungan hari ini.</p>
      )}
    </div>
  );
};

const SkeletonCard = () => (
  <div className='bg-white border border-slate-200 rounded-xl p-4 animate-pulse h-[76px]'>
    <div className='flex items-center gap-4 h-full'>
      <div className='w-11 h-11 rounded-lg bg-slate-200' />
      <div className='flex-1 space-y-2'>
        <div className='h-5 w-12 bg-slate-200 rounded' />
        <div className='h-3 w-24 bg-slate-100 rounded' />
      </div>
    </div>
  </div>
);

/* ---------- halaman ---------- */

const Dashboard = () => {
  const { data, isLoading } = useClinicDashboard();
  const navigate = useNavigate();
  const { user } = useAuth();
  const t = data?.totals;
  const lowStock = data?.lowStockMedicines || [];

  return (
    <div className='p-4 md:p-6 space-y-6 max-w-6xl'>
      {/* Header */}
      <div className='rounded-2xl bg-gradient-to-r from-slate-800 to-slate-900 text-white p-5 md:p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4'>
        <div>
          <p className='text-slate-300 text-sm capitalize'>
            {formatDate(new Date())}
          </p>
          <h1 className='text-xl md:text-2xl font-semibold mt-0.5'>
            Selamat datang{user?.username ? `, ${user.username}` : ''} 👋
          </h1>
          <p className='text-slate-300 text-sm mt-1'>
            Ringkasan aktivitas klinik hari ini
          </p>
        </div>
        <div className='flex gap-2'>
          <button
            onClick={() => navigate(CLINIC_ROUTES.visits)}
            className='inline-flex items-center gap-2 bg-white text-brand-600 px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-50'
          >
            <Plus className='w-4 h-4' /> Daftar Kunjungan
          </button>
          <button
            onClick={() => navigate(CLINIC_ROUTES.queue)}
            className='inline-flex items-center gap-2 bg-white/10 border border-white/25 px-4 py-2 rounded-lg text-sm font-medium hover:bg-white/20'
          >
            <Clock className='w-4 h-4' /> Antrian
          </button>
        </div>
      </div>

      {/* Statistik */}
      <div className='grid grid-cols-2 lg:grid-cols-4 gap-3'>
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <SkeletonCard key={i} />)
        ) : (
          <>
            <StatCard
              icon={Users}
              label='Karyawan aktif'
              value={t?.employeesActive}
              accent='bg-brand-100 text-brand-700'
            />
            <StatCard
              icon={ClipboardList}
              label='Kunjungan hari ini'
              value={t?.visitsToday}
              accent='bg-green-100 text-green-700'
            />
            <StatCard
              icon={Clock}
              label='Menunggu'
              value={t?.waitingCount}
              accent='bg-amber-100 text-amber-700'
            />
            <StatCard
              icon={Pill}
              label='Obat menipis'
              value={lowStock.length}
              accent='bg-red-100 text-red-700'
            />
          </>
        )}
      </div>

      {/* Konten utama */}
      <div className='grid md:grid-cols-3 gap-4'>
        {/* Antrian hari ini */}
        <section className='md:col-span-2 bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
          <div className='flex justify-between items-center mb-3'>
            <h2 className='font-semibold text-slate-800 flex items-center gap-2'>
              <Activity className='w-4 h-4 text-brand-600' /> Antrian hari ini
            </h2>
            <button
              onClick={() => navigate(CLINIC_ROUTES.queue)}
              className='text-brand-600 text-sm inline-flex items-center gap-1 hover:underline'
            >
              Lihat semua <ArrowRight className='w-3.5 h-3.5' />
            </button>
          </div>

          {isLoading ? (
            <div className='space-y-2'>
              {Array.from({ length: 3 }).map((_, i) => (
                <div
                  key={i}
                  className='h-12 rounded-lg bg-slate-100 animate-pulse'
                />
              ))}
            </div>
          ) : (data?.todayQueue || []).length === 0 ? (
            <div className='text-center py-10 text-slate-400'>
              <ClipboardList className='w-10 h-10 mx-auto mb-2 opacity-40' />
              <p className='text-sm'>Belum ada antrian hari ini.</p>
              <button
                onClick={() => navigate(CLINIC_ROUTES.visits)}
                className='mt-3 text-brand-600 text-sm hover:underline'
              >
                + Daftar kunjungan pertama
              </button>
            </div>
          ) : (
            <ul className='divide-y divide-slate-100'>
              {data.todayQueue.map((v) => (
                <li key={v.id} className='py-2.5 flex items-center gap-3'>
                  <span className='w-9 h-9 rounded-lg bg-brand-50 text-brand-700 font-bold grid place-items-center text-sm shrink-0'>
                    #{v.queue_no}
                  </span>
                  <div className='flex-1 min-w-0'>
                    <div className='font-medium text-slate-800 truncate'>
                      {v.employee_name}
                    </div>
                    {v.complaint && (
                      <div className='text-xs text-slate-500 truncate'>
                        {v.complaint}
                      </div>
                    )}
                  </div>
                  <StatusBadge status={v.status} />
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* Panel kanan */}
        <div className='space-y-4'>
          {/* Status kunjungan */}
          <section className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <h2 className='font-semibold text-slate-800 mb-3'>
              Status kunjungan
            </h2>
            {isLoading ? (
              <div className='h-24 bg-slate-100 rounded animate-pulse' />
            ) : (
              <StatusBreakdown byStatus={data?.visitsByStatus} />
            )}
          </section>

          {/* Obat menipis */}
          <section
            className={`border rounded-xl p-4 md:p-5 shadow-sm ${lowStock.length ? 'bg-red-50 border-red-200' : 'bg-white border-slate-200'}`}
          >
            <h2
              className={`font-semibold mb-3 flex items-center gap-2 ${lowStock.length ? 'text-red-700' : 'text-slate-800'}`}
            >
              <AlertTriangle className='w-4 h-4' /> Obat menipis
            </h2>
            {isLoading ? (
              <div className='h-16 bg-slate-100 rounded animate-pulse' />
            ) : lowStock.length === 0 ? (
              <p className='text-slate-400 text-sm'>Semua stok obat aman 👍</p>
            ) : (
              <ul className='space-y-2'>
                {lowStock.map((m) => (
                  <li
                    key={m.id}
                    className='flex justify-between items-center text-sm'
                  >
                    <span className='text-red-800'>{m.name}</span>
                    <span className='font-medium text-red-700'>
                      {m.stock} {m.unit}
                    </span>
                  </li>
                ))}
                <li className='pt-1'>
                  <button
                    onClick={() => navigate(CLINIC_ROUTES.medicines)}
                    className='text-red-700 text-sm hover:underline inline-flex items-center gap-1'
                  >
                    Kelola stok <ArrowRight className='w-3.5 h-3.5' />
                  </button>
                </li>
              </ul>
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
