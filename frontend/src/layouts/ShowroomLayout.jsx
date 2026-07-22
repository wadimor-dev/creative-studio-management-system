import React, { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  ArrowLeftRight,
  Users,
  ClipboardCheck,
  BarChart3,
  Settings,
  MapPin,
  FolderTree,
  ScanLine,
  QrCode,
  FolderOpen,
  X,
  ArrowLeft,
  Menu,
} from 'lucide-react';

const navItems = [
  { to: '/showroom/dashboard', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/showroom/samples', label: 'Sample Management', icon: Package },
  { to: '/showroom/borrowings', label: 'Peminjaman', icon: ArrowLeftRight },
  { to: '/showroom/guests', label: 'Manajemen Tamu', icon: Users },
  { to: '/showroom/stock-control', label: 'Kontrol Stok', icon: ClipboardCheck },
  { to: '/showroom/locations', label: 'Lokasi & QR Code', icon: MapPin },
  { to: '/showroom/storage', label: 'Storage Management', icon: FolderTree },
  { to: '/showroom/management', label: 'Showroom Management', icon: FolderOpen },
  { to: '/showroom/scan', label: 'Scan QR', icon: ScanLine },
  { to: '/showroom/qr-generator', label: 'QR Generator', icon: QrCode },
  { to: '/showroom/reports', label: 'Pelaporan', icon: BarChart3 },
  { to: '/showroom/master-data', label: 'Master Data', icon: Settings },
];

const ShowroomLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-slate-50">
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 flex flex-col
          transform transition-transform duration-300 lg:translate-x-0 lg:static lg:inset-auto
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex items-center justify-between h-16 px-5 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-500 text-white font-semibold text-sm">
              S
            </div>
            <div className="leading-tight">
              <p className="text-sm font-semibold text-white">Showroom</p>
              <p className="text-[11px] text-slate-400 tracking-wide uppercase">
                Modul Internal
              </p>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-slate-400 hover:text-white"
          >
            <X size={20} />
          </button>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium
                transition-all duration-200 border-l-2
                ${
                  isActive
                    ? 'bg-slate-800 text-white border-brand-500 shadow-sm'
                    : 'text-slate-400 border-transparent hover:bg-slate-800/60 hover:text-slate-200'
                }`
              }
            >
              <Icon size={18} className="shrink-0" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-slate-800">
          <NavLink
            to="/dashboard"
            className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 hover:bg-slate-800/60 hover:text-slate-200 transition-colors"
          >
            <ArrowLeft size={18} className="shrink-0" />
            <span>Kembali ke Aplikasi Utama</span>
          </NavLink>
        </div>
      </aside>

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="lg:hidden flex items-center justify-between h-16 px-4 bg-white border-b border-slate-200">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-slate-600 hover:text-slate-900"
          >
            <Menu size={24} />
          </button>
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-brand-500 text-white font-semibold text-xs">
              S
            </div>
            <span className="text-sm font-semibold text-slate-900">Showroom</span>
          </div>
          <div className="w-6" />
        </header>

        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ShowroomLayout;
