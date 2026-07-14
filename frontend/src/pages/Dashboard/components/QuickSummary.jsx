import React from 'react';
import { Trophy, Star, TrendingUp, Package } from 'lucide-react';

const QuickSummary = ({ data }) => {
  const eom = data.employee_of_month || { name: 'None', value: '-' };
  const mua = data.most_used_asset || { name: 'None', value: '-' };
  const mpc = data.most_productive_category || { name: 'None', value: '-' };

  return (
    <div className="rounded-xl border border-gray-100 bg-white p-4 sm:p-6 dark:border-gray-800 dark:bg-gray-900 shadow-sm">
      <h3 className="mb-4 sm:mb-6 text-base sm:text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
        <Trophy className="text-amber-500" size={20} />
        Quick Summary
      </h3>
      
      <div className="space-y-4">
        {/* Employee of the Month */}
        <div className="flex items-start gap-4 rounded-lg bg-gray-50 p-3 sm:p-4 dark:bg-gray-800/50">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400">
            <Star size={20} />
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Employee of the Month</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white mt-1">{eom.name}</p>
            <p className="text-xs text-brand-600 dark:text-brand-400 font-medium">{eom.value}</p>
          </div>
        </div>

        {/* Most Used Asset */}
        <div className="flex items-start gap-4 rounded-lg bg-gray-50 p-3 sm:p-4 dark:bg-gray-800/50">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
            <Package size={20} />
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Most Used Asset</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white mt-1">{mua.name}</p>
            <p className="text-xs text-brand-600 dark:text-brand-400 font-medium">{mua.value}</p>
          </div>
        </div>

        {/* Most Productive Category */}
        <div className="flex items-start gap-4 rounded-lg bg-gray-50 p-3 sm:p-4 dark:bg-gray-800/50">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400">
            <TrendingUp size={20} />
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Most Productive Category</p>
            <p className="text-sm font-semibold text-gray-900 dark:text-white mt-1">{mpc.name}</p>
            <p className="text-xs text-brand-600 dark:text-brand-400 font-medium">{mpc.value}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuickSummary;
