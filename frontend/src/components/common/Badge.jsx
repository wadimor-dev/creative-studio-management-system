import React, { forwardRef } from 'react';

const Badge = forwardRef(({ 
  children, 
  variant = 'default',
  className = '', 
  ...props 
}, ref) => {
  const baseStyles = 'inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset';
  
  const variants = {
    default: 'bg-slate-50 text-slate-600 ring-slate-500/10',
    info: 'bg-blue-50 text-blue-700 ring-blue-700/10',
    success: 'bg-emerald-50 text-emerald-700 ring-emerald-600/10',
    warning: 'bg-amber-50 text-amber-700 ring-amber-600/20',
    danger: 'bg-rose-50 text-rose-700 ring-rose-600/10',
  };

  return (
    <span
      ref={ref}
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </span>
  );
});

Badge.displayName = 'Badge';
export default Badge;
