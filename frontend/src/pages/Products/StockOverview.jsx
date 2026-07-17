import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import { Search, PackageOpen, MapPin, ClipboardCheck } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import StockOpnameModal from './components/StockOpnameModal';
import GlobalFilter from '../../components/common/GlobalFilter';
import { useProductStocks } from '../../hooks/useProductStocks';
import { useLocations } from '../../hooks/useLocations';
import { productStockService } from '../../api/services/productMovementService';

const StockOverview = () => {
  const [filters, setFilters] = useState({});
  const { data: stocksData, loading, refetch } = useProductStocks(filters);
  const { locations } = useLocations();
  const [searchTerm, setSearchTerm] = useState('');
  const [opnameModalOpen, setOpnameModalOpen] = useState(false);

  // Stocks response from API is directly the data array since it's unpaginated SuccessResponse
  const stocks = Array.isArray(stocksData) ? stocksData : (stocksData?.data || []);
  const locationArray = Array.isArray(locations) ? locations : (locations?.data || []);

  const locationStats = locationArray.map(loc => {
    const totalQty = stocks
      .filter(s => s.placement?.id === loc.id)
      .reduce((sum, current) => sum + current.quantity, 0);
    return { ...loc, totalQty };
  }).filter(loc => loc.totalQty > 0);

  const filteredStocks = stocks.filter(s =>
    s.product?.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.product?.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.placement?.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleOpnameSubmit = async (data) => {
    try {
      const res = await productStockService.performOpname(data);
      if (res.success) {
        toastSuccess(`Stock opname completed. ${res.data.adjustments_made} adjustments made.`);
        setOpnameModalOpen(false);
        refetch();
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Stock Overview"
        description="Monitor current stock balances across all storage locations."
        actions={
          <Button
            variant="primary"
            size="sm"
            className="gap-2 whitespace-nowrap"
            onClick={() => setOpnameModalOpen(true)}
          >
            <ClipboardCheck size={16} />
            Perform Stock Opname
          </Button>
        }
      />

      <GlobalFilter
        availableFilters={['type', 'category', 'motif', 'sub_motif', 'color', 'location']}
        onApply={setFilters}
      />

      {locationStats.length > 0 && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {locationStats.map(loc => (
            <div
              key={loc.id}
              className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-5 transition-shadow hover:shadow-sm"
            >
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-slate-500">{loc.name}</p>
                <h3 className="mt-1 text-2xl font-bold text-slate-800">
                  {loc.totalQty}
                  <span className="ml-1 text-sm font-normal text-slate-400">items</span>
                </h3>
              </div>
              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-brand-50 text-brand-600">
                <MapPin size={20} />
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white">
        <div className="border-b border-slate-200 p-4">
          <div className="relative w-full sm:w-80">
            <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input
              type="text"
              placeholder="Search product or location..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full rounded-lg border border-slate-300 py-2 pl-9 pr-3 text-sm text-slate-700 placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          {loading ? (
            <div className="flex h-48 items-center justify-center">
              <LoadingSpinner size="md" />
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-xs font-medium uppercase tracking-wider text-slate-500">
                  <th className="px-4 py-3">Product</th>
                  <th className="px-4 py-3">Location</th>
                  <th className="px-4 py-3 text-right">Qty Available</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {filteredStocks.map((item) => (
                  <tr key={item.id} className="transition-colors hover:bg-slate-50">
                    <td className="px-4 py-3.5">
                      <div className="font-medium text-slate-900">{item.product?.display_name}</div>
                      <div className="mt-0.5 font-mono text-xs text-slate-500">{item.product?.sku}</div>
                    </td>
                    <td className="px-4 py-3.5 text-slate-600">
                      {item.placement?.name}
                    </td>
                    <td className="px-4 py-3.5 text-right">
                      <Badge variant={item.quantity > 0 ? 'success' : 'danger'}>
                        {item.quantity}
                      </Badge>
                    </td>
                  </tr>
                ))}

                {filteredStocks.length === 0 && (
                  <tr>
                    <td colSpan="3" className="px-4 py-16 text-center">
                      <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-slate-400">
                        <PackageOpen size={22} />
                      </div>
                      <div className="text-sm font-medium text-slate-700">No stock data found</div>
                      <div className="mt-1 text-sm text-slate-500">
                        Stock balances will appear here when product movements are recorded.
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <Modal isOpen={opnameModalOpen} onClose={() => setOpnameModalOpen(false)} title="Perform Stock Opname">
        <StockOpnameModal onSubmit={handleOpnameSubmit} onCancel={() => setOpnameModalOpen(false)} />
      </Modal>
    </div>
  );
};

export default StockOverview;