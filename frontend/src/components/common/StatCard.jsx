import React from 'react';

const colorMap = {
  brand: 'bg-brand-50 text-brand-600',
  blue: 'bg-blue-50 text-blue-600',
  emerald: 'bg-emerald-50 text-emerald-600',
  amber: 'bg-amber-50 text-amber-600',
  rose: 'bg-rose-50 text-rose-600',
  violet: 'bg-violet-50 text-violet-600',
  slate: 'bg-slate-100 text-slate-600',
};

const StatCard = ({ label, value, icon: Icon, color = 'brand', trend, className = '' }) => {
  return (
    <div className={`rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md ${className}`}>
      <div className="flex items-center justify-between">
        <div className="min-w-0">
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-1 text-2xl font-bold text-slate-900">{value}</p>
        </div>
        <div className={`shrink-0 rounded-lg p-3 ${colorMap[color] || colorMap.brand}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      {trend && (
        <p className="mt-2 text-xs text-slate-400">{trend}</p>
      )}
    </div>
  );
};

export default StatCard;
