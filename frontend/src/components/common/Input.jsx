import React, { forwardRef } from 'react';

const Input = forwardRef(({ 
  type = 'text', 
  error = false, 
  className = '', 
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
      <input
        ref={ref}
        type={type}
        className={`
          block w-full rounded-lg border-0 py-2.5 text-slate-900 shadow-sm ring-1 ring-inset transition-all duration-200 sm:text-sm sm:leading-6
          ${Icon ? 'pl-10 pr-3' : 'px-3'}
          ${error 
            ? 'ring-rose-300 text-rose-900 focus:ring-2 focus:ring-inset focus:ring-rose-500 placeholder:text-rose-300' 
            : 'ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-brand-500'
          }
          ${className}
        `}
        {...props}
      />
    </div>
  );
});

Input.displayName = 'Input';
export default Input;
