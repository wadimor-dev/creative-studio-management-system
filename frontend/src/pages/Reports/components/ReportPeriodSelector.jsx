import React from 'react';
import { Calendar, CalendarDays, CalendarRange } from 'lucide-react';

const ReportPeriodSelector = ({ activePeriod, onChange }) => {
  const periods = [
    { label: 'daily', icon: Calendar },
    { label: 'weekly', icon: CalendarDays },
    { label: 'monthly', icon: CalendarRange },
  ];

  return (
    <div className="inline-flex rounded-xl bg-slate-100/80 p-1 shadow-inner">
      {periods.map(({ label, icon: Icon }) => (
        <button
          key={label}
          onClick={() => onChange(label)}
          className={`
            group flex items-center gap-1.5 rounded-lg px-3 sm:px-4 py-2 text-xs sm:text-sm font-medium transition-all duration-200
            ${activePeriod === label 
              ? 'bg-white text-slate-900 shadow-sm ring-1 ring-slate-200/60' 
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/50'
            }
          `}
        >
          <Icon size={14} className={`transition-colors ${activePeriod === label ? 'text-brand-500' : 'text-slate-400 group-hover:text-slate-500'}`} />
          {label}
        </button>
      ))}
    </div>
  );
};

export default ReportPeriodSelector;
