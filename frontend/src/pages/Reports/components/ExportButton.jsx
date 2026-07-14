import React, { useState, useRef, useEffect } from 'react';
import Button from '../../../components/common/Button';
import { Download, FileSpreadsheet, FileText, ChevronDown } from 'lucide-react';
import { toastSuccess, toastInfo, toastError } from '../../../utils/toast';
import { useAuth } from '../../../contexts/AuthContext';

const ExportButton = ({ activePeriod, filters = {} }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const { user } = useAuth();

  const userRole = typeof user?.role === 'string' ? user.role : user?.role?.name;

  // Roles: ADMIN, STAFF
  // We assume STAFF is supervisor/employee. Let's allow STAFF to export PDF. ADMIN can export PDF and Excel.
  const canExportPdf = userRole === 'Admin' || userRole === 'ADMIN' || userRole === 'STAFF';
  const canExportExcel = userRole === 'Admin' || userRole === 'ADMIN'; // Assuming only Admin/Manager can export Excel

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleExport = async (format) => {
    setIsOpen(false);
    setIsExporting(true);
    try {
      toastInfo(`Exporting report as ${format.toUpperCase()}...`);
      const { exportService } = await import('../../../api/services/exportService');
      const params = { type: activePeriod, ...filters };
      
      const response = format === 'xlsx' 
        ? await exportService.exportReportsExcel(params)
        : await exportService.exportReportsPdf(params);
        
      const blob = response instanceof Blob ? response : new Blob([response.data || response]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      // Note: Backend might send Content-Disposition, but we ensure download attribute
      const timestamp = new Date().getTime();
      link.setAttribute('download', `activity_report_${activePeriod.toLowerCase()}_${new Date().toISOString().split('T')[0]}_${timestamp}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toastSuccess(`Report exported successfully!`);
    } catch (err) {
      // Handle the 400 bad request error from backend for limit exceeded
      const msg = err.response?.data?.detail || err.message || 'Failed to export report';
      toastError(msg);
    } finally {
      setIsExporting(false);
    }
  };

  const exportOptions = [];
  
  if (canExportPdf) {
    exportOptions.push({ label: 'Export as PDF', icon: FileText, format: 'pdf', description: 'Best for printing' });
  }
  if (canExportExcel) {
    exportOptions.push({ label: 'Export as Excel', icon: FileSpreadsheet, format: 'xlsx', description: 'Best for analysis' });
  }

  // If no export permission at all
  if (exportOptions.length === 0) {
    return null;
  }

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
        <ChevronDown size={14} className={`hidden sm:block transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
      </Button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 origin-top-right rounded-xl bg-white py-1.5 shadow-lg shadow-slate-200/50 ring-1 ring-slate-200 z-10 animate-in fade-in slide-in-from-top-2 duration-200">
          <div className="px-3 py-2 border-b border-slate-100">
            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Export Format</p>
          </div>
          {exportOptions.map((option) => (
            <button
              key={option.format}
              onClick={() => handleExport(option.format)}
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

export default ExportButton;
