import React, { useState, useRef, useEffect } from 'react';
import Button from '../../../components/common/Button';
import { Download, FileSpreadsheet, FileText, ChevronDown, Package, Activity } from 'lucide-react';
import { toastSuccess, toastInfo, toastError } from '../../../utils/toast';

const InventoryExportButton = ({ filters = {} }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleExport = async (format, type) => {
    setIsOpen(false);
    setIsExporting(true);
    try {
      toastInfo(`Exporting ${type} as ${format.toUpperCase()}...`);
      const { exportService } = await import('../../../api/services/exportService');
      
      let response;
      if (type === 'items') {
          response = format === 'xlsx' ? await exportService.exportItemsExcel(filters) : await exportService.exportItemsPdf(filters);
      } else {
          response = format === 'xlsx' ? await exportService.exportInventoryTransactionsExcel(filters) : await exportService.exportInventoryTransactionsPdf(filters);
      }
        
      const blob = response instanceof Blob ? response : new Blob([response]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `inventory_${type}_${new Date().toISOString().split('T')[0]}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toastSuccess(`Inventory ${type} exported successfully!`);
    } catch (err) {
      toastError('Failed to export inventory ' + type);
    } finally {
      setIsExporting(false);
    }
  };

  const exportOptions = [
    { label: 'Items Catalog (PDF)', icon: FileText, format: 'pdf', type: 'items', description: 'Export master items' },
    { label: 'Items Catalog (Excel)', icon: FileSpreadsheet, format: 'xlsx', type: 'items', description: 'Export master items' },
    { label: 'Transactions (PDF)', icon: FileText, format: 'pdf', type: 'transactions', description: 'Export stock movements' },
    { label: 'Transactions (Excel)', icon: FileSpreadsheet, format: 'xlsx', type: 'transactions', description: 'Export stock movements' },
  ];

  return (
    <div className="relative" ref={dropdownRef}>
      <Button 
        variant="secondary" 
        className="gap-2" 
        onClick={() => setIsOpen(!isOpen)}
        disabled={isExporting}
      >
        <Download size={16} className={isExporting ? 'animate-bounce' : ''} />
        <span className="hidden sm:inline">{isExporting ? 'Exporting...' : 'Export'}</span>
        <ChevronDown size={14} className={"hidden sm:block transition-transform duration-200 " + (isOpen ? 'rotate-180' : '')} />
      </Button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 origin-top-right rounded-xl bg-white py-1.5 shadow-lg shadow-slate-200/50 ring-1 ring-slate-200 z-10 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="px-3 py-2 border-b border-slate-100">
            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Export Format</p>
          </div>
          {exportOptions.map((option, idx) => (
            <button
              key={idx}
              onClick={() => handleExport(option.format, option.type)}
              className="flex w-full items-center gap-3 px-3 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-colors"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-500">
                <option.icon size={16} />
              </div>
              <div className="text-left">
                <p className="font-medium text-slate-800">{option.label}</p>
                <p className="text-xs text-slate-500">{option.description}</p>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default InventoryExportButton;
