import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Badge from '../../components/common/Badge';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import { Search, PackageOpen, MapPin, ClipboardCheck } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import ProductsTabs from './components/ProductsTabs';
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
      .filter(s => s.location?.id === loc.id)
      .reduce((sum, current) => sum + current.quantity, 0);
    return { ...loc, totalQty };
  }).filter(loc => loc.totalQty > 0);

  const filteredStocks = stocks.filter(s => 
    s.product?.display_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    s.product?.sku.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.location?.name.toLowerCase().includes(searchTerm.toLowerCase())
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
    <div>
      <PageHeader 
        title="Products" 
        description="Manage your product catalog, movements, and master data."
      />
      
      <ProductsTabs />

      <GlobalFilter 
        availableFilters={['type', 'category', 'motif', 'sub_motif', 'color', 'location']} 
        onApply={setFilters} 
      />

      {locationStats.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4 mb-6">
          {locationStats.map(loc => (
            <div key={loc.id} className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex items-center justify-between hover:shadow-md transition-shadow">
              <div>
                <p className="text-sm font-medium text-slate-500 mb-1">{loc.name}</p>
                <h3 className="text-2xl font-bold text-slate-800">
                  {loc.totalQty} <span className="text-sm font-normal text-slate-400 ml-1">items</span>
                </h3>
              </div>
              <div className="w-12 h-12 rounded-full bg-brand-50 flex items-center justify-center text-brand-600">
                <MapPin size={24} />
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
        <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row justify-between gap-4">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text"
              placeholder="Search product or location..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
            />
          </div>
          <Button variant="primary" size="sm" className="gap-2" onClick={() => setOpnameModalOpen(true)}>
            <ClipboardCheck size={16} />
            Perform Stock Opname
          </Button>
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
                  <th className="p-4 font-medium border-b border-slate-200">Product</th>
                  <th className="p-4 font-medium border-b border-slate-200">Location</th>
                  <th className="p-4 font-medium border-b border-slate-200 text-right">Qty Available</th>
                </tr>
              </thead>
              <tbody className="text-sm divide-y divide-slate-100">
                {filteredStocks.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="p-4">
                      <div className="font-semibold text-slate-900">{item.product?.display_name}</div>
                      <div className="text-xs font-mono text-slate-500 mt-0.5">{item.product?.sku}</div>
                    </td>
                    <td className="p-4 text-slate-700 font-medium">
                      {item.location?.name}
                    </td>
                    <td className="p-4 text-right">
                      <Badge variant={item.quantity > 0 ? 'success' : 'danger'} className="text-sm font-semibold">
                        {item.quantity}
                      </Badge>
                    </td>
                  </tr>
                ))}
                {filteredStocks.length === 0 && (
                  <tr>
                    <td colSpan="3" className="p-12 text-center">
                      <div className="text-slate-400 mb-2 flex justify-center"><PackageOpen size={32} /></div>
                      <div className="text-slate-600 font-medium">No stock data found</div>
                      <div className="text-slate-500 text-sm mt-1">Stock balances will appear here when product movements are recorded.</div>
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
