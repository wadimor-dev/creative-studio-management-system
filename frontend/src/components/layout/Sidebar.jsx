import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Package,
  Layers,
  FileText,
  Users,
  Settings,
  X,
  Briefcase
} from 'lucide-react';

import { useAuth } from '../../contexts/AuthContext';
import { hasPermission } from '../../utils/permissions';

import logoUrl from '../../assets/logo/logo.webp';

const Sidebar = ({ isOpen = false, onClose }) => {

  const { user } = useAuth();

  const menuItems = [

    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: <LayoutDashboard size={20} />,
      permission: 'DASHBOARD'
    },

    {
      name: 'Work',
      path: '/work',
      icon: <Briefcase size={20} />,
      permission: 'WORK'
    },

    {
      name: 'Inventory',
      path: '/inventory',
      icon: <Package size={20} />,
      permission: 'INVENTORY'
    },

    {
      name: 'Products',
      path: '/products',
      icon: <Layers size={20} />,
      permission: 'PRODUCTS'
    },

    {
      name: 'Reports',
      path: '/reports',
      icon: <FileText size={20} />,
      permission: 'REPORTS'
    },

    {
      name: 'Users',
      path: '/users',
      icon: <Users size={20} />,
      permission: 'USERS'
    },

    {
      name: 'Settings',
      path: '/settings',
      icon: <Settings size={20} />,
      permission: 'SETTINGS'
    }

  ];

  const visibleMenus = menuItems.filter(menu =>
    hasPermission(user, menu.permission)
  );

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

        <div className="flex h-16 items-center justify-between border-b border-slate-100 px-6">

          <div className="flex items-center gap-2 font-bold text-md text-slate-800">

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

        <div className="flex h-[calc(100vh-4rem)] flex-col justify-between overflow-y-auto px-4 py-6">

          <ul className="space-y-1.5">

            {visibleMenus.map(item => (

              <li key={item.name}>

                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all
                    ${
                      isActive
                        ? 'bg-brand-50 text-brand-600'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }`
                  }
                >

                  {({ isActive }) => (
                    <>
                      <span
                        className={`transition-transform group-hover:scale-110 ${
                          isActive
                            ? 'text-brand-600'
                            : 'text-slate-400 group-hover:text-slate-600'
                        }`}
                      >
                        {item.icon}
                      </span>

                      {item.name}
                    </>
                  )}

                </NavLink>

              </li>

            ))}

          </ul>

        </div>

      </aside>
    </>
  );
};

export default Sidebar;