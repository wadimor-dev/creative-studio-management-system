import React from 'react';
import { useLocation } from 'react-router-dom';
import { Menu, Bell } from 'lucide-react';

const titleMap = {
  '/showroom': 'Dashboard',
  '/showroom/dashboard': 'Dashboard',
  '/showroom/samples': 'Sample Management',
  '/showroom/borrowings': 'Peminjaman',
  '/showroom/guests': 'Manajemen Tamu',
  '/showroom/stock-control': 'Kontrol Stok',
  '/showroom/reports': 'Pelaporan',
  '/showroom/master-data': 'Master Data',
};

const ShowroomNavbar = ({ onMenuToggle }) => {
  const { pathname } = useLocation();
  const title = titleMap[pathname] ?? 'Showroom';

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-stone-200 bg-white/80 backdrop-blur px-4 sm:px-6 lg:px-8">
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuToggle}
          className="lg:hidden text-neutral-600 hover:text-neutral-900"
        >
          <Menu size={22} />
        </button>
        <h1 className="text-base sm:text-lg font-semibold text-neutral-900">
          {title}
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <button className="relative text-neutral-500 hover:text-neutral-800">
          <Bell size={20} />
          <span className="absolute -top-1 -right-1 h-2 w-2 rounded-full bg-amber-500" />
        </button>
        <div className="h-8 w-8 rounded-full bg-neutral-900 flex items-center justify-center text-amber-400 text-xs font-semibold">
          S
        </div>
      </div>
    </header>
  );
};

export default ShowroomNavbar;
