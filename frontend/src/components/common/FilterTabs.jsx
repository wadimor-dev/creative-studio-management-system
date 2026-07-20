import React from 'react';

const FilterTabs = ({ tabs, active, onChange, className = '' }) => {
  return (
    <div className={`flex gap-2 ${className}`}>
      {tabs.map((tab) => {
        const isActive = active === tab.value;
        return (
          <button
            key={tab.value}
            onClick={() => onChange(tab.value)}
            className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-all duration-200 ${
              isActive
                ? 'bg-brand-600 text-white shadow-sm'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            {tab.icon && <tab.icon className="mr-1.5 inline h-4 w-4" />}
            {tab.label}
            {tab.count !== undefined && (
              <span className={`ml-1.5 rounded-full px-1.5 py-0.5 text-xs ${
                isActive ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-500'
              }`}>
                {tab.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};

export default FilterTabs;
