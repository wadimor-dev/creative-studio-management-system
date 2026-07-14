import React from 'react';

const FormField = ({ label, error, children, helpText }) => {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1.5">
        {label}
      </label>
      {children}
      {error && (
        <p className="mt-1.5 text-sm text-rose-500 flex items-center gap-1">
          <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}
      {helpText && !error && (
        <p className="mt-1.5 text-sm text-slate-500">{helpText}</p>
      )}
    </div>
  );
};

export default FormField;
