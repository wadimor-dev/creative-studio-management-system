import React, { forwardRef } from 'react';

const Checkbox = forwardRef(({ 
  label, 
  description,
  className = '', 
  ...props 
}, ref) => {
  return (
    <div className={`relative flex items-start ${className}`}>
      <div className="flex h-6 items-center">
        <input
          ref={ref}
          type="checkbox"
          className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-600 transition-all duration-200"
          {...props}
        />
      </div>
      {(label || description) && (
        <div className="ml-3 text-sm leading-6">
          {label && (
            <label htmlFor={props.id || props.name} className="font-medium text-slate-900">
              {label}
            </label>
          )}
          {description && (
            <p className="text-slate-500">{description}</p>
          )}
        </div>
      )}
    </div>
  );
});

Checkbox.displayName = 'Checkbox';
export default Checkbox;
