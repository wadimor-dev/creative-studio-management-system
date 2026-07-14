import React from 'react';
import Card from '../../../components/common/Card';
import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

const StatWidget = ({ title, value, icon: Icon, color, trend, trendUp, subtitle }) => {
  return (
    <Card className="p-4 sm:p-6 transition-all hover:shadow-md hover:border-slate-300">
      <div className="flex items-start sm:items-center justify-between gap-2">
        <div className="min-w-0">
          <p className="truncate text-xs sm:text-sm font-medium text-slate-500">{title}</p>
          <div className="mt-1 sm:mt-2 flex items-baseline gap-2">
            <span className="text-xl sm:text-3xl font-semibold tracking-tight text-slate-900">{value}</span>
          </div>
        </div>
        {Icon && (
          <div className={`flex h-9 w-9 sm:h-12 sm:w-12 flex-shrink-0 items-center justify-center rounded-lg sm:rounded-xl bg-${color}-50 text-${color}-600`}>
            <Icon className="h-5 w-5 sm:h-6 sm:w-6" />
          </div>
        )}
      </div>
      
      {(trend || subtitle) && (
        <div className="mt-3 sm:mt-4 flex items-center gap-1 sm:gap-2 text-xs sm:text-sm">
          {trend && (
            <span className={`flex items-center font-medium ${trendUp ? 'text-emerald-600' : 'text-rose-600'}`}>
              {trendUp ? <ArrowUpRight size={14} className="mr-0.5" /> : <ArrowDownRight size={14} className="mr-0.5" />}
              {trend}
            </span>
          )}
          {subtitle && <span className="text-slate-500 truncate">{subtitle}</span>}
        </div>
      )}
    </Card>
  );
};

export default StatWidget;
