import React from 'react';
import { MapPin } from 'lucide-react';

const InventoryStats = ({ locations = [], items = [] }) => {
  
  // Calculate total stock per location by summing up items whose primary location matches
  // If your backend expands ItemResponse to include full stocks array, you'd iterate over item.stocks
  const locationStats = locations.map(loc => {
    const totalQty = items
      .filter(item => item.location?.id === loc.id)
      .reduce((sum, item) => sum + (item.stock_qty || 0), 0);
    return { ...loc, totalQty };
  }).filter(loc => loc.totalQty > 0);

  if (locationStats.length === 0) {
    return (
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 mb-6">
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <p className="text-sm font-medium text-slate-500">No Locations Found</p>
        </div>
      </div>
    );
  }

  return (
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
  );
};

export default InventoryStats;
