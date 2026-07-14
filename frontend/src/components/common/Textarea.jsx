import React, { forwardRef } from 'react';

const Textarea = forwardRef(({ 
  error = false, 
  className = '', 
  rows = 4,
  ...props 
}, ref) => {
  return (
    <textarea
      ref={ref}
      rows={rows}
      className={`
        block w-full rounded-lg border-0 py-2.5 px-3 text-slate-900 shadow-sm ring-1 ring-inset transition-all duration-200 sm:text-sm sm:leading-6 resize-y
        ${error 
          ? 'ring-rose-300 text-rose-900 focus:ring-2 focus:ring-inset focus:ring-rose-500 placeholder:text-rose-300' 
          : 'ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-brand-500'
        }
        ${className}
      `}
      {...props}
    />
  );
});

Textarea.displayName = 'Textarea';
export default Textarea;
