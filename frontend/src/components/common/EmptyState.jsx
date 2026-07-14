import React from 'react';
import { PackageOpen } from 'lucide-react';

const EmptyState = ({ 
  title = 'No data found', 
  description = 'Get started by creating a new record.',
  icon: Icon = PackageOpen,
  action 
}) => {
  return (
    <div className="text-center py-10 px-4">
      <Icon className="mx-auto h-12 w-12 text-slate-300" strokeWidth={1.5} />
      <h3 className="mt-2 text-sm font-semibold text-slate-900">{title}</h3>
      <p className="mt-1 text-sm text-slate-500">{description}</p>
      {action && (
        <div className="mt-6">
          {action}
        </div>
      )}
    </div>
  );
};

export default EmptyState;
