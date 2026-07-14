import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const InventoryTabs = () => {
  const location = useLocation();
  const currentPath = location.pathname;

  const tabs = [
    { name: 'Overview', href: '/inventory' },
    { name: 'Items', href: '/inventory/items' },
    { name: 'History', href: '/inventory/history' },
    { name: 'Categories', href: '/inventory/categories' },
    { name: 'Locations', href: '/inventory/locations' },
  ];

  return (
    <div className="mb-6 border-b border-slate-200">
      <nav className="-mb-px flex space-x-8" aria-label="Tabs">
        {tabs.map((tab) => {
          const isActive = currentPath === tab.href;
          return (
            <Link
              key={tab.name}
              to={tab.href}
              className={`
                whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors duration-200
                ${isActive
                  ? 'border-brand-500 text-brand-600'
                  : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                }
              `}
            >
              {tab.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default InventoryTabs;
