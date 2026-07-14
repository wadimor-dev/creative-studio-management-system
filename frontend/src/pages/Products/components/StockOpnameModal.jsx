import React, { useState, useEffect } from 'react';
import Button from '../../../components/common/Button';
import { useLocations } from '../../../hooks/useLocations';
import { useProducts } from '../../../hooks/useProducts';
import { useProductStocks } from '../../../hooks/useProductStocks';
import LoadingSpinner from '../../../components/common/LoadingSpinner';

const StockOpnameModal = ({ onSubmit, onCancel }) => {
  const { locations, loading: loadingLocations } = useLocations();
  const { data: productsData, loading: loadingProducts } = useProducts();
  const { data: stocksData, loading: loadingStocks } = useProductStocks();

  const [selectedLocation, setSelectedLocation] = useState('');
  const [actualStocks, setActualStocks] = useState({});

  const productArray = Array.isArray(productsData) ? productsData : (productsData?.data || []);
  const locationArray = Array.isArray(locations) ? locations : (locations?.data || []);
  const stockArray = Array.isArray(stocksData) ? stocksData : (stocksData?.data || []);

  const loading = loadingLocations || loadingProducts || loadingStocks;

  useEffect(() => {
    // Reset actual stocks when location changes
    if (selectedLocation) {
      const initialStocks = {};
      productArray.forEach(p => {
        const stock = stockArray.find(s => s.product_id === p.id && s.location_id === parseInt(selectedLocation));
        initialStocks[p.id] = stock ? stock.quantity : 0;
      });
      setActualStocks(initialStocks);
    } else {
      setActualStocks({});
    }
  }, [selectedLocation, productArray, stockArray]);

  const handleStockChange = (productId, value) => {
    const numValue = value === '' ? 0 : parseInt(value, 10);
    setActualStocks(prev => ({ ...prev, [productId]: isNaN(numValue) ? 0 : numValue }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedLocation) return;

    const items = Object.entries(actualStocks).map(([product_id, actual_quantity]) => ({
      product_id: parseInt(product_id),
      actual_quantity
    }));

    onSubmit({
      location_id: parseInt(selectedLocation),
      items
    });
  };

  if (loading) {
    return <div className="flex justify-center p-8"><LoadingSpinner size="md" /></div>;
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 mt-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Select Location *</label>
        <select 
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          value={selectedLocation}
          onChange={(e) => setSelectedLocation(e.target.value)}
          required
        >
          <option value="">Select Location to Opname...</option>
          {locationArray.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
        </select>
      </div>

      {selectedLocation && (
        <div className="mt-4 border border-slate-200 rounded-lg overflow-hidden">
          <div className="max-h-80 overflow-y-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead className="bg-slate-50 sticky top-0 shadow-sm z-10">
                <tr className="text-slate-500 text-xs uppercase">
                  <th className="p-3 font-medium">Product</th>
                  <th className="p-3 font-medium text-center">System Qty</th>
                  <th className="p-3 font-medium text-center">Actual Qty</th>
                  <th className="p-3 font-medium text-center">Diff</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 bg-white">
                {productArray.map(p => {
                  const stock = stockArray.find(s => s.product_id === p.id && s.location_id === parseInt(selectedLocation));
                  const systemQty = stock ? stock.quantity : 0;
                  const actualQty = actualStocks[p.id] !== undefined ? actualStocks[p.id] : systemQty;
                  const diff = actualQty - systemQty;
                  
                  return (
                    <tr key={p.id} className="hover:bg-slate-50/50">
                      <td className="p-3">
                        <div className="font-medium text-slate-800">{p.display_name}</div>
                        <div className="text-xs text-slate-500 font-mono">{p.sku}</div>
                      </td>
                      <td className="p-3 text-center text-slate-600 font-medium">
                        {systemQty}
                      </td>
                      <td className="p-3 text-center">
                        <input 
                          type="number" 
                          min="0"
                          value={actualStocks[p.id] === undefined ? '' : actualStocks[p.id]}
                          onChange={(e) => handleStockChange(p.id, e.target.value)}
                          className="w-20 text-center border border-slate-300 rounded px-2 py-1 focus:ring-1 focus:ring-brand-500 outline-none"
                        />
                      </td>
                      <td className="p-3 text-center">
                        <span className={`font-semibold ${diff > 0 ? 'text-emerald-600' : (diff < 0 ? 'text-rose-600' : 'text-slate-400')}`}>
                          {diff > 0 ? `+${diff}` : diff}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-slate-200">
        <Button variant="outline" type="button" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant="primary" type="submit" disabled={!selectedLocation}>
          Submit Opname
        </Button>
      </div>
    </form>
  );
};

export default StockOpnameModal;
