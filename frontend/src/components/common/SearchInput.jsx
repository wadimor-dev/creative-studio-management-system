import React, { forwardRef } from 'react';
import { Search } from 'lucide-react';

const SearchInput = forwardRef(({ className = '', ...props }, ref) => {
  return (
    <div className="relative">
      <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
        <Search size={16} className="text-slate-400" />
      </div>
      <input
        ref={ref}
        type="text"
        className={`block w-full rounded-lg border-0 py-2 pl-9 pr-3 text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 placeholder:text-slate-400 focus:ring-2 focus:ring-inset focus:ring-brand-500 sm:text-sm sm:leading-6 transition-all duration-200 ${className}`}
        {...props}
      />
    </div>
  );
});

SearchInput.displayName = 'SearchInput';
export default SearchInput;
