import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Badge from '../../components/common/Badge';
import { Plus, ArrowRightLeft, ArrowDownToLine, ArrowUpFromLine, Download, FileSpreadsheet } from 'lucide-react';
import { toastSuccess, toastError, toastInfo } from '../../utils/toast';

import MovementForm from './components/MovementForm';
import GlobalFilter from '../../components/common/GlobalFilter';
import { useProductMovements } from '../../hooks/useProductMovements';
import { productMovementService } from '../../api/services/productMovementService';
import { exportService } from '../../api/services/exportService';

const Movements = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({});
  const { data: movementsData, loading, refetch } = useProductMovements(filters);
  // const [formModal, setFormModal] = useState({ isOpen: false });

  // const openFormModal = () => setFormModal({ isOpen: true });
  // const closeFormModal = () => setFormModal({ isOpen: false });

  const handleFormSubmit = async (formData) => {
    try {
      const res = await productMovementService.create(formData);
      if (res.success) {
        toastSuccess('Movement recorded successfully!');
        // closeFormModal();
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
    switch (type) {
      case 'IN': return <ArrowDownToLine size={16} className="text-emerald-500" />;
      case 'OUT': return <ArrowUpFromLine size={16} className="text-rose-500" />;
      case 'TRANSFER': return <ArrowRightLeft size={16} className="text-blue-500" />;
      default: return null;
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Movements"
        description="Track and record every stock in, out, and transfer for your products."
          actions={
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" className="gap-2" onClick={() => handleExport('excel')} title="Export to Excel">
                <FileSpreadsheet size={16} className="text-green-600" />
                <span className="hidden lg:inline">Excel</span>
              </Button>
              <Button variant="outline" size="sm" className="gap-2" onClick={() => handleExport('pdf')} title="Export to PDF">
                <Download size={16} className="text-rose-600" />
                <span className="hidden lg:inline">PDF</span>
              </Button>
              <Button variant="primary" size="sm" className="gap-2" onClick={() => navigate('/products/movements/create')}>
                <Plus size={16} />
                Record Movement
              </Button>
            </div>
          }

      />

      <GlobalFilter
        availableFilters={['date', 'type', 'category', 'motif', 'sub_motif', 'color', 'location', 'user']}
        onApply={setFilters}
      />

      <div className="flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white">
        <div className="overflow-x-auto">
          {loading ? (
            <div className="flex h-48 items-center justify-center">
              <LoadingSpinner size="md" />
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-xs font-medium uppercase tracking-wider text-slate-500">
                  <th className="px-4 py-3">Date</th>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3">Product</th>
                  <th className="px-4 py-3">Qty</th>
                  <th className="px-4 py-3">Locations</th>
                  <th className="px-4 py-3">Ref / Notes</th>
                  <th className="px-4 py-3">User</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {movements.map((item) => (
                  <tr key={item.id} className="transition-colors hover:bg-slate-50">
                    <td className="whitespace-nowrap px-4 py-3.5 text-slate-600">
                      {new Intl.DateTimeFormat('en-GB', {
                        day: '2-digit', month: 'short', year: 'numeric',
                        hour: '2-digit', minute: '2-digit'
                      }).format(new Date(item.date))}
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-1.5">
                        {getMovementIcon(item.type)}
                        <span className="font-medium text-slate-700">{item.type}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="font-medium text-slate-900">{item.product?.display_name}</div>
                      <div className="mt-0.5 font-mono text-xs text-slate-500">{item.product?.sku}</div>
                    </td>
                    <td className="px-4 py-3.5 font-semibold text-slate-700">
                      {item.type === 'OUT' ? '-' : (item.type === 'IN' ? '+' : '')}{item.quantity}
                    </td>
                    <td className="px-4 py-3.5 text-slate-600">
                      {item.type === 'IN' && <span className="font-medium text-emerald-600">{item.destination_location?.name}</span>}
                      {item.type === 'OUT' && <span className="font-medium text-rose-600">{item.source_location?.name}</span>}
                      {item.type === 'TRANSFER' && (
                        <div className="flex items-center gap-2 text-xs">
                          <span className="w-20 truncate" title={item.source_location?.name}>{item.source_location?.name}</span>
                          <ArrowRightLeft size={12} className="shrink-0 text-slate-400" />
                          <span className="w-20 truncate" title={item.destination_location?.name}>{item.destination_location?.name}</span>
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3.5">
                      {item.reference && <div className="mb-0.5 text-xs font-medium text-slate-700">Ref: {item.reference}</div>}
                      {item.notes && <div className="line-clamp-1 text-xs text-slate-500" title={item.notes}>{item.notes}</div>}
                    </td>
                    <td className="px-4 py-3.5 text-xs text-slate-500">
                      {item.user?.full_name}
                    </td>
                  </tr>
                ))}

                {movements.length === 0 && (
                  <tr>
                    <td colSpan="7" className="px-4 py-16 text-center text-sm text-slate-500">
                      No product movements recorded yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* <Modal isOpen={formModal.isOpen} onClose={closeFormModal} title="Record Movement">
        <MovementForm onSubmit={handleFormSubmit} onCancel={closeFormModal} />
      </Modal> */}
    </div>
  );
};

export default Movements;