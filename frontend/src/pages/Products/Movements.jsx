import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Badge from '../../components/common/Badge';
import { Plus, ArrowRightLeft, ArrowDownToLine, ArrowUpFromLine, Download, FileSpreadsheet } from 'lucide-react';
import { toastSuccess, toastError, toastInfo } from '../../utils/toast';

import ProductsTabs from './components/ProductsTabs';
import MovementForm from './components/MovementForm';
import GlobalFilter from '../../components/common/GlobalFilter';
import { useProductMovements } from '../../hooks/useProductMovements';
import { productMovementService } from '../../api/services/productMovementService';
import { exportService } from '../../api/services/exportService';

const Movements = () => {
  const [filters, setFilters] = useState({});
  const { data: movementsData, loading, refetch } = useProductMovements(filters);
  const [formModal, setFormModal] = useState({ isOpen: false });

  const openFormModal = () => setFormModal({ isOpen: true });
  const closeFormModal = () => setFormModal({ isOpen: false });

  const handleFormSubmit = async (formData) => {
    try {
      const res = await productMovementService.create(formData);
      if (res.success) {
        toastSuccess('Movement recorded successfully!');
        closeFormModal();
        refetch();
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    }
  };

  const handleExport = async (type) => {
    try {
      toastInfo(`Exporting ${type.toUpperCase()}...`);
      const response = type === 'excel' 
        ? await exportService.exportProductMovementsExcel(filters)
        : await exportService.exportProductMovementsPdf(filters);
        
      // Interceptor returns response.data directly, so 'response' is the Blob
      const blob = response instanceof Blob ? response : new Blob([response]);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `product_movements_${new Date().toISOString().split('T')[0]}.${type === 'excel' ? 'xlsx' : 'pdf'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toastSuccess('Export downloaded successfully!');
    } catch (err) {
      toastError('Failed to export data');
    }
  };

  const movements = Array.isArray(movementsData) ? movementsData : (movementsData?.data || []);

  const getMovementIcon = (type) => {
    switch(type) {
      case 'IN': return <ArrowDownToLine size={16} className="text-emerald-500" />;
      case 'OUT': return <ArrowUpFromLine size={16} className="text-rose-500" />;
      case 'TRANSFER': return <ArrowRightLeft size={16} className="text-blue-500" />;
      default: return null;
    }
  };

  return (
    <div>
      <PageHeader 
        title="Products" 
        description="Manage your product catalog, movements, and master data."
      />
      
      <ProductsTabs />

      <GlobalFilter 
        availableFilters={['date', 'type', 'category', 'motif', 'sub_motif', 'color', 'location', 'user']} 
        onApply={setFilters} 
      />

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
        <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <h2 className="text-base font-semibold text-slate-800 shrink-0">Movement History</h2>
          
          <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
            
            <div className="flex items-center gap-2 border-l border-slate-200 pl-3">
              <Button variant="outline" size="sm" className="gap-2" onClick={() => handleExport('excel')} title="Export to Excel">
                <FileSpreadsheet size={16} className="text-green-600" />
                <span className="hidden lg:inline">Excel</span>
              </Button>
              <Button variant="outline" size="sm" className="gap-2" onClick={() => handleExport('pdf')} title="Export to PDF">
                <Download size={16} className="text-rose-600" />
                <span className="hidden lg:inline">PDF</span>
              </Button>
              <Button variant="primary" size="sm" className="gap-2 ml-1" onClick={openFormModal}>
                <Plus size={16} />
                <span className="hidden sm:inline">Record Movement</span>
              </Button>
            </div>
          </div>
        </div>

        <div className="overflow-x-auto">
          {loading ? (
            <div className="flex justify-center items-center h-48">
              <LoadingSpinner size="md" />
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                  <th className="p-4 font-medium border-b border-slate-200">Date</th>
                  <th className="p-4 font-medium border-b border-slate-200">Type</th>
                  <th className="p-4 font-medium border-b border-slate-200">Product</th>
                  <th className="p-4 font-medium border-b border-slate-200">Qty</th>
                  <th className="p-4 font-medium border-b border-slate-200">Locations</th>
                  <th className="p-4 font-medium border-b border-slate-200">Ref / Notes</th>
                  <th className="p-4 font-medium border-b border-slate-200">User</th>
                </tr>
              </thead>
              <tbody className="text-sm divide-y divide-slate-100">
                {movements.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="p-4 text-slate-600 whitespace-nowrap">
                      {new Intl.DateTimeFormat('en-GB', { 
                        day: '2-digit', month: 'short', year: 'numeric', 
                        hour: '2-digit', minute: '2-digit' 
                      }).format(new Date(item.date))}
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-1.5">
                        {getMovementIcon(item.type)}
                        <span className="font-medium text-slate-700">{item.type}</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="font-medium text-slate-900">{item.product?.display_name}</div>
                      <div className="text-xs text-slate-500 font-mono mt-0.5">{item.product?.sku}</div>
                    </td>
                    <td className="p-4 font-semibold text-slate-700">
                      {item.type === 'OUT' ? '-' : (item.type === 'IN' ? '+' : '')}{item.quantity}
                    </td>
                    <td className="p-4 text-slate-600">
                      {item.type === 'IN' && <span className="text-emerald-600 font-medium">{item.destination_location?.name}</span>}
                      {item.type === 'OUT' && <span className="text-rose-600 font-medium">{item.source_location?.name}</span>}
                      {item.type === 'TRANSFER' && (
                        <div className="flex items-center gap-2 text-xs">
                          <span className="truncate w-20" title={item.source_location?.name}>{item.source_location?.name}</span>
                          <ArrowRightLeft size={12} className="text-slate-400 shrink-0" />
                          <span className="truncate w-20" title={item.destination_location?.name}>{item.destination_location?.name}</span>
                        </div>
                      )}
                    </td>
                    <td className="p-4">
                      {item.reference && <div className="text-xs font-medium text-slate-700 mb-0.5">Ref: {item.reference}</div>}
                      {item.notes && <div className="text-xs text-slate-500 line-clamp-1" title={item.notes}>{item.notes}</div>}
                    </td>
                    <td className="p-4 text-slate-500 text-xs">
                      {item.user?.full_name}
                    </td>
                  </tr>
                ))}
                {movements.length === 0 && (
                  <tr>
                    <td colSpan="7" className="p-12 text-center text-slate-500">
                      No product movements recorded yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <Modal isOpen={formModal.isOpen} onClose={closeFormModal} title="Record Movement">
        <MovementForm onSubmit={handleFormSubmit} onCancel={closeFormModal} />
      </Modal>
    </div>
  );
};

export default Movements;
