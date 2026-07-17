import React, { useEffect, useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { useLocation } from 'react-router-dom';

import SidebarItem from './SidebarItem';

const SidebarCollapse = ({ item }) => {

  const { pathname } = useLocation();

  const isActive = item.children.some(child =>
    pathname.startsWith(child.path)
  );

  const [open, setOpen] = useState(isActive);

  useEffect(() => {

    if (isActive) {
      setOpen(true);
    }

  }, [isActive]);

  const Icon = item.icon;
  const isValidIcon = typeof Icon === 'function' || typeof Icon === 'object';

  return (

    <li>

      <button
        onClick={() => setOpen(!open)}
        className={`flex w-full items-center justify-between rounded-lg px-3 py-2.5 text-sm font-medium transition-all
        ${
          isActive
            ? 'bg-brand-50 text-brand-600'
            : 'text-slate-600 hover:bg-slate-50'
        }`}
      >

        <div className="flex items-center gap-3">

          {isValidIcon && (
            <Icon
              size={20}
              className={
                isActive
                  ? 'text-brand-600'
                  : 'text-slate-400'
              }
            />
          )}

          {item.name}

        </div>

        <ChevronDown
          size={18}
          className={`transition-transform duration-200
          ${
            open
              ? 'rotate-180'
              : ''
          }`}
        />

      </button>

      {open && (

        <ul className="ml-6 mt-1 space-y-1">

          {item.children.map(child => (

            <SidebarItem
              key={child.path}
              item={child}
              nested
            />

          ))}

        </ul>

      )}

    </li>

  );

};

export default SidebarCollapse;