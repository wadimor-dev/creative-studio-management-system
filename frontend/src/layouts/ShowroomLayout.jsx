import React, { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  Users,
  ShoppingCart,
  Truck,
  X,
  ArrowLeft,
  Menu,
  ArrowUpRight,
  ArrowDownRight,
  RefreshCw,
  Box,
} from 'lucide-react';

const navItems = [
  { to: '/showroom/dashboard', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/showroom/stock', label: 'Stok', icon: Box },
  { to: '/showroom/transfers', label: 'Transfer', icon: RefreshCw },
  { to: '/showroom/stock-in', label: 'Barang Masuk', icon: ArrowUpRight },
  { to: '/showroom/stock-out', label: 'Barang Keluar', icon: ArrowDownRight },
  { to: '/showroom/products', label: 'Produk', icon: Package },
  { to: '/showroom/customers', label: 'Pelanggan', icon: Users },
  { to: '/showroom/orders', label: 'Pesanan', icon: ShoppingCart },
  { to: '/showroom/delivery', label: 'Pengiriman', icon: Truck },
];

const ShowroomLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-stone-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-neutral-900 flex flex-col
          transform transition-transform duration-300 lg:translate-x-0 lg:static lg:inset-auto
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex items-center justify-between h-16 px-5 border-b border-neutral-800">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded bg-amber-500 text-neutral-900 font-semibold text-sm">
              S
            </div>
            <div className="leading-tight">
              <p className="text-sm font-semibold text-white">Showroom</p>
              <p className="text-[11px] text-neutral-500 tracking-wide uppercase">
                Modul Internal
              </p>
            </div>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden text-neutral-400 hover:text-white"
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
                `group flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium
                transition-colors border-l-2
                ${
                  isActive
                    ? 'bg-neutral-800 text-white border-amber-500'
                    : 'text-neutral-400 border-transparent hover:bg-neutral-800/60 hover:text-neutral-200'
                }`
              }
            >
              <Icon size={18} className="shrink-0" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="px-3 py-4 border-t border-neutral-800">
          <NavLink
            to="/dashboard"
            className="flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium text-neutral-400 hover:bg-neutral-800/60 hover:text-neutral-200 transition-colors"
          >
            <ArrowLeft size={18} className="shrink-0" />
            <span>Kembali ke Aplikasi Utama</span>
          </NavLink>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Mobile header */}
        <header className="lg:hidden flex items-center justify-between h-16 px-4 bg-white border-b border-stone-200">
          <button
            onClick={() => setSidebarOpen(true)}
            className="text-neutral-600 hover:text-neutral-900"
          >
            <Menu size={24} />
          </button>
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded bg-amber-500 text-neutral-900 font-semibold text-xs">
              S
            </div>
            <span className="text-sm font-semibold text-neutral-900">Showroom</span>
          </div>
          <div className="w-6" />
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default ShowroomLayout;