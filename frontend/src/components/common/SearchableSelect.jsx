import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Search, Check } from 'lucide-react';

const SearchableSelect = ({ 
  options, 
  value, 
  onChange, 
  placeholder = 'Select an option...',
  disabled = false,
  className = ''
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const wrapperRef = useRef(null);
  
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const filteredOptions = options.filter(opt => 
    opt.label.toLowerCase().includes(search.toLowerCase()) || 
    (opt.subLabel && opt.subLabel.toLowerCase().includes(search.toLowerCase())) ||
    opt.value.toLowerCase().includes(search.toLowerCase())
  );

  const selectedOption = options.find(opt => opt.value === value);

  return (
    <div ref={wrapperRef} className={`relative ${className}`}>
      <div 
        className={`w-full px-3 py-2 border rounded-lg flex items-center justify-between cursor-pointer transition-colors ${
          disabled 
            ? 'bg-slate-100 border-slate-200 text-slate-400 cursor-not-allowed' 
            : isOpen 
              ? 'bg-white border-brand-500 ring-2 ring-brand-500/20' 
              : 'bg-white border-slate-300 hover:border-slate-400'
        }`}
        onClick={() => !disabled && setIsOpen(!isOpen)}
      >
        <span className={`block truncate ${!selectedOption ? 'text-slate-500' : 'text-slate-800'}`}>
          {selectedOption ? selectedOption.label : placeholder}
        </span>
        <ChevronDown size={16} className={`text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </div>

      {isOpen && (
        <div className="absolute z-50 w-full mt-1 bg-white border border-slate-200 rounded-lg shadow-xl max-h-60 flex flex-col overflow-hidden">
          <div className="p-2 border-b border-slate-100 shrink-0 relative">
            <Search size={14} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              className="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-transparent rounded-md text-sm focus:outline-none focus:bg-white focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all"
              placeholder="Search..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              autoFocus
              onClick={(e) => e.stopPropagation()}
            />
          </div>
          
          <div className="overflow-y-auto flex-1 p-1">
            {filteredOptions.length === 0 ? (
              <div className="p-3 text-center text-sm text-slate-500">No results found</div>
            ) : (
              filteredOptions.map((opt) => {
                const isSelected = opt.value === value;
                return (
                  <div
                    key={opt.value}
                    className={`px-3 py-2 text-sm rounded-md cursor-pointer flex flex-col ${
                      opt.disabled 
                        ? 'opacity-50 cursor-not-allowed bg-slate-50 text-slate-400' 
                        : isSelected 
                          ? 'bg-brand-50 text-brand-700' 
                          : 'hover:bg-slate-50 text-slate-700'
                    }`}
                    onClick={() => {
                      if (!opt.disabled) {
                        onChange(opt.value);
                        setIsOpen(false);
                        setSearch('');
                      }
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{opt.label}</span>
                      {isSelected && <Check size={14} className="text-brand-600 shrink-0 ml-2" />}
                    </div>
                    {opt.subLabel && (
                      <span className={`text-xs mt-0.5 ${opt.disabled ? 'text-slate-400' : 'text-slate-500'} font-mono`}>
                        {opt.subLabel}
                      </span>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchableSelect;
