import React, { useEffect } from 'react';
import { X } from 'lucide-react';

const Modal = ({ 
  isOpen, 
  onClose, 
  title, 
  children, 
  footer,
  maxWidth = 'max-w-lg'
}) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
      <div 
        className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />
      
      <div className={`relative w-full ${maxWidth} transform rounded-xl bg-white text-left shadow-xl transition-all sm:my-8`}>
        <div className="flex items-center justify-between border-b border-slate-100 px-4 sm:px-6 py-4">
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <button
            onClick={onClose}
            className="rounded-md text-slate-400 hover:text-slate-500 focus:outline-none focus:ring-2 focus:ring-brand-500"
          >
            <span className="sr-only">Close</span>
            <X size={20} />
          </button>
        </div>
        
        <div className="px-4 sm:px-6 py-4">
          {children}
        </div>
        
        {footer && (
          <div className="border-t border-slate-100 bg-slate-50 px-4 sm:px-6 py-4 sm:flex sm:flex-row-reverse sm:rounded-b-xl">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};

export default Modal;
