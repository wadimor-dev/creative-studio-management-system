import React, { forwardRef } from 'react';
import { ChevronDown } from 'lucide-react';

const Select = forwardRef(({ 
  error = false, 
  className = '', 
  children,
  icon: Icon,
  ...props 
}, ref) => {
  return (
    <div className="relative">
      {Icon && (
        <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
          <Icon size={18} className="text-slate-400" />
        </div>
      )}
      <select
        ref={ref}
        className={`
          block w-full appearance-none rounded-lg border-0 py-2.5 text-slate-900 shadow-sm ring-1 ring-inset transition-all duration-200 sm:text-sm sm:leading-6
          ${Icon ? 'pl-10 pr-10' : 'pl-3 pr-10'}
          ${error 
            ? 'ring-rose-300 text-rose-900 focus:ring-2 focus:ring-inset focus:ring-rose-500' 
            : 'ring-slate-300 focus:ring-2 focus:ring-inset focus:ring-brand-500'
          }
          ${className}
        `}
        {...props}
      >
        {children}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
        <ChevronDown size={16} className={error ? 'text-rose-400' : 'text-slate-400'} />
      </div>
    </div>
  );
});

Select.displayName = 'Select';
export default Select;
