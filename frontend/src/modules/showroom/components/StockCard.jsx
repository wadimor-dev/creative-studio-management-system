import React from 'react';

const StockCard = ({ label, value, icon: Icon, trend, color = 'amber' }) => {
  const colorVariants = {
    amber: {
      bg: 'bg-amber-50',
      text: 'text-amber-600',
    },
    blue: {
      bg: 'bg-blue-50',
      text: 'text-blue-600',
    },
    emerald: {
      bg: 'bg-emerald-50',
      text: 'text-emerald-600',
    },
    rose: {
      bg: 'bg-rose-50',
      text: 'text-rose-600',
    },
  };

  const colors = colorVariants[color] || colorVariants.amber;

  return (
    <div className="rounded-xl border border-stone-200 bg-white p-5">
      <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${colors.bg} ${colors.text}`}>
        <Icon size={20} />
      </div>
      <p className="mt-4 text-2xl font-semibold text-neutral-900">{value}</p>
      <p className="text-sm text-neutral-500">{label}</p>
      {trend && <p className="mt-2 text-xs text-neutral-400">{trend}</p>}
    </div>
  );
};

export default StockCard;
