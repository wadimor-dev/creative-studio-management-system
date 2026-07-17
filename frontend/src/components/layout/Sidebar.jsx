import React from 'react';
import { X } from 'lucide-react';

import { useAuth } from '../../contexts/AuthContext';
import { SIDEBARS } from '../../config/sidebar';

import SidebarGroup from './sidebar/SidebarGroup';

import logoUrl from '../../assets/logo/logo.webp';

const Sidebar = ({ isOpen = false, onClose }) => {
  const { user } = useAuth();

  // Untuk sementara hardcode, nanti diganti berdasarkan division user
  const getSidebar = (user) => {
    if (!user) return SIDEBARS.default;

    switch (user.role?.name) {
      case 'ADMIN':
        return SIDEBARS.admin;

      case 'CREATIVE':
        return SIDEBARS.creative;

      case 'STAFF':
        return SIDEBARS.creative;

      default:
        return SIDEBARS.default;
    }
  };

  const sidebar = getSidebar(user);

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/50 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed left-0 top-0 z-50 h-screen w-64 border-r border-slate-200 bg-white shadow-sm
          transition-transform duration-300
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:z-40
        `}
      >
        {/* Header */}
        <div className="flex h-16 items-center justify-between border-b border-slate-100 px-6">
          <div className="flex items-center gap-2 text-md font-bold text-slate-800">
            <div className="flex h-8 w-8 overflow-hidden">
              <img
                src={logoUrl}
                alt="Logo"
                className="h-full w-full object-cover"
              />
            </div>

            WADIMOR CREATIVE
          </div>

          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 lg:hidden"
          >
            <X size={20} />
          </button>
        </div>

        {/* Menu */}
        <div className="h-[calc(100vh-4rem)] overflow-y-auto px-4 py-6">

          {sidebar.map((group) => (
            <SidebarGroup
              key={group.title}
              group={group}
              user={user}
            />
          ))}

        </div>
      </aside>
    </>
  );
};

export default Sidebar;