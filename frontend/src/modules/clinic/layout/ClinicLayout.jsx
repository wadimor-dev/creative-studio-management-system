import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import {
  Stethoscope,
  LayoutDashboard,
  ClipboardList,
  Clock,
  FileText,
  Pill,
  ArrowLeft,
  LogOut,
  Menu,
  X,
} from 'lucide-react';
import { useAuth } from '../../../contexts/AuthContext'; // sesuaikan bila pakai alias '@/'
import { CLINIC_ROUTES } from '../constants';

const navItems = [
  {
    to: CLINIC_ROUTES.dashboard,
    label: 'Dashboard',
    icon: LayoutDashboard,
    end: true,
  },
  { to: CLINIC_ROUTES.visits, label: 'Kunjungan', icon: ClipboardList },
  { to: CLINIC_ROUTES.queue, label: 'Antrian', icon: Clock },
  { to: CLINIC_ROUTES.medicalRecords, label: 'Rekam Medis', icon: FileText },
  { to: CLINIC_ROUTES.medicines, label: 'Obat & Stok', icon: Pill },
];

const ClinicLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className='min-h-screen flex bg-slate-50'>
      {/* Overlay mobile */}
      {sidebarOpen && (
        <div
          onClick={() => setSidebarOpen(false)}
          className='fixed inset-0 bg-slate-900/50 z-40 lg:hidden'
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-slate-900 text-white
        flex flex-col transform transition-transform duration-200
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0`}
      >
        {/* Brand */}
        <div className='flex items-center gap-3 px-4 h-16 border-b border-slate-800 shrink-0'>
          <div className='w-9 h-9 rounded-lg bg-brand-500 grid place-items-center font-bold text-white'>
            C
          </div>
          <div className='flex-1'>
            <div className='font-semibold leading-tight flex items-center gap-1.5'>
              <Stethoscope className='w-4 h-4 text-brand-400' /> Clinic
            </div>
            <div className='text-xs text-slate-400'>Modul Internal</div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className='lg:hidden text-slate-400 hover:text-white'
          >
            <X className='w-5 h-5' />
          </button>
        </div>

        {/* Nav */}
        <nav className='flex-1 px-3 py-4 space-y-1 overflow-y-auto'>
          {navItems.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium
                transition-all duration-200 border-l-2 ${
                  isActive
                    ? 'bg-slate-800 text-white border-brand-500 shadow-sm'
                    : 'text-slate-400 border-transparent hover:bg-slate-800/60 hover:text-slate-200'
                }`
              }
            >
              <Icon className='w-4 h-4 shrink-0' />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className='border-t border-slate-800 p-3 space-y-1 shrink-0'>
          <button
            onClick={() => navigate('/dashboard')}
            className='w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
          >
            <ArrowLeft className='w-4 h-4' /> Kembali ke Aplikasi Utama
          </button>
          {user && (
            <div className='px-3 py-1.5 text-xs text-slate-500 truncate'>
              {user.username || user.email} · {user.role?.name}
            </div>
          )}
          <button
            onClick={() => logout?.()}
            className='w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800/60 hover:text-slate-200'
          >
            <LogOut className='w-4 h-4' /> Logout
          </button>
        </div>
      </aside>

      {/* Konten */}
      <div className='flex-1 flex flex-col min-w-0'>
        {/* Topbar mobile */}
        <header className='lg:hidden flex items-center gap-3 h-14 px-4 bg-white border-b'>
          <button
            onClick={() => setSidebarOpen(true)}
            className='text-slate-600 hover:text-slate-900'
          >
            <Menu className='w-6 h-6' />
          </button>
          <div className='w-7 h-7 rounded-md bg-brand-500 grid place-items-center text-white font-bold text-sm'>
            C
          </div>
          <span className='font-semibold text-slate-800'>Clinic</span>
        </header>

        <main className='flex-1 overflow-y-auto'>
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ClinicLayout;
