import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Package, ArrowRightLeft, Database } from 'lucide-react';

const ProductsTabs = () => {
  const location = useLocation();
  const currentPath = location.pathname;

  const tabs = [
    { name: 'Stock Overview', href: '/products/stock', icon: LayoutDashboard },
    { name: 'Catalog', href: '/products/catalog', icon: Package },
    { name: 'Movements', href: '/products/movements', icon: ArrowRightLeft },
    { name: 'Placements', href: '/products/placements', icon: Database },
    { name: 'Barcode Center', href: '/products/barcode-center', icon: Database },
    { name: 'Master Data', href: '/products/master-data', icon: Database },
  ];

  return (
    <div className="overflow-x-auto overflow-y-hidden mb-6 border-b border-slate-200">
      <nav className="-mb-px flex space-x-8" aria-label="Tabs">
        {tabs.map((tab) => {
          const isActive = currentPath === tab.href || (currentPath.startsWith(tab.href) && tab.href !== '/products');
          // For '/products' Overview tab, it should only be active if exact match
          const isExact = tab.href === '/products' ? currentPath === '/products' : isActive;
          
          return (
            <Link
              key={tab.name}
              to={tab.href}
              className={`
                whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors duration-200
                ${isExact
                  ? 'border-brand-500 text-brand-600'
                  : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                }
              `}
            >
              <div className="flex items-center gap-2">
                <tab.icon size={16} className={isExact ? 'text-brand-600' : 'text-slate-400'} />
                {tab.name}
              </div>
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default ProductsTabs;
