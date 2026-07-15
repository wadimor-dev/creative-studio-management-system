import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { scannerService } from '../../api/services/scannerService';
import { locationService } from '../../api/services/locationService';
import { productStockService } from '../../api/services/productStockService';
import { toastSuccess, toastError } from '../../utils/toast';
import { Package, ArrowLeft, ArrowUpCircle, ArrowDownCircle, Scan } from 'lucide-react';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';

// Simple beep sound using Web Audio API
const playBeep = () => {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    oscillator.type = 'sine';
    oscillator.frequency.value = 800;
    gainNode.gain.value = 0.1;
    
    oscillator.start();
    setTimeout(() => {
      oscillator.stop();
    }, 100);
  } catch (e) {
    console.error("Audio API not supported");
  }
};

const LocationView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState(null);
  const [stocks, setStocks] = useState([]);
  
  // Scanning state
  const [scanMode, setScanMode] = useState('IN'); // 'IN' or 'OUT'
  const [scanLoading, setScanLoading] = useState(false);
  
  // Barcode scanner listener logic
  const barcodeBuffer = useRef('');
  const lastKeyTime = useRef(Date.now());

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const [locRes, stockRes] = await Promise.all([
        locationService.getById(id),
        productStockService.getAll({ location_id: id })
      ]);
      
      if (locRes.success) setLocation(locRes.data);
      if (stockRes.success) setStocks(stockRes.data);
    } catch (err) {
      toastError("Failed to load location data");
      navigate('/scanner');
    } finally {
      setLoading(false);
    }
  }, [id, navigate]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Handle Barcode Scans
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      const currentTime = Date.now();
      if (currentTime - lastKeyTime.current > 50) {
        barcodeBuffer.current = '';
      }
      
      if (e.key === 'Enter') {
        if (barcodeBuffer.current.length > 2) {
          e.preventDefault();
          handleProductScan(barcodeBuffer.current);
        }
        barcodeBuffer.current = '';
      } else if (e.key.length === 1) {
        barcodeBuffer.current += e.key;
      }
      
      lastKeyTime.current = currentTime;
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }); // Note: depends on scanMode which is accessed in handleProductScan

  const handleProductScan = async (sku) => {
    if (!sku || scanLoading) return;
    setScanLoading(true);
    
    try {
      const payload = {
        location_id: parseInt(id),
        product_sku: sku,
        quantity: 1
      };
      
      let res;
      if (scanMode === 'IN') {
        res = await scannerService.scanIn(payload);
      } else {
        res = await scannerService.scanOut(payload);
      }
      
      if (res.success) {
        playBeep();
        toastSuccess(res.message);
        // Refresh stocks directly to show updated quantities
        const stockRes = await productStockService.getAll({ location_id: id });
        if (stockRes.success) setStocks(stockRes.data);
      } else {
        toastError(res.message);
      }
    } catch (err) {
      toastError(err.response?.data?.message || `Failed to scan ${scanMode} product`);
    } finally {
      setScanLoading(false);
    }
  };

  if (loading || !location) {
    return (
      <div className="flex justify-center items-center h-[50vh]">
        <LoadingSpinner size="lg" text="Loading location..." />
      </div>
    );
  }

  // Calculate capacities
  const totalItems = stocks.reduce((sum, item) => sum + item.quantity, 0);
  const capacityWarning = location.capacity && totalItems >= location.capacity * 0.9;

  return (
    <div className="max-w-5xl mx-auto mt-4 space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex justify-between items-start">
          <div className="flex gap-4">
            <button 
              onClick={() => navigate('/scanner')}
              className="p-2 h-fit bg-slate-50 text-slate-500 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <ArrowLeft size={20} />
            </button>
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 className="text-2xl font-bold text-slate-800">{location.name}</h1>
                <span className="px-2.5 py-1 text-xs font-medium bg-brand-50 text-brand-700 rounded-full">
                  {location.location_type}
                </span>
                <span className="px-2.5 py-1 text-xs font-medium bg-slate-100 text-slate-600 rounded-full font-mono">
                  {location.code || `ID: ${location.id}`}
                </span>
              </div>
              <p className="text-slate-500 text-sm">{location.description || 'No description provided'}</p>
            </div>
          </div>
          
          <div className="text-right">
            <div className={`text-2xl font-bold ${capacityWarning ? 'text-rose-600' : 'text-slate-800'}`}>
              {totalItems} <span className="text-sm font-normal text-slate-500">items</span>
            </div>
            {location.capacity && (
              <div className="text-xs text-slate-400 mt-1">
                Capacity: {location.capacity}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Scanner Panel */}
        <div className="md:col-span-1 space-y-4">
          <div className={`p-6 rounded-2xl border-2 transition-colors ${
            scanMode === 'IN' ? 'border-brand-500 bg-brand-50' : 'border-rose-500 bg-rose-50'
          }`}>
            <div className="flex justify-between items-center mb-6">
              <h3 className={`font-bold ${scanMode === 'IN' ? 'text-brand-800' : 'text-rose-800'}`}>
                Scan Mode
              </h3>
              <Scan className={scanMode === 'IN' ? 'text-brand-500' : 'text-rose-500'} />
            </div>
            
            <div className="flex gap-2 mb-6 bg-white p-1 rounded-xl shadow-sm border border-slate-200">
              <button
                className={`flex-1 py-2 rounded-lg font-medium text-sm transition-all flex items-center justify-center gap-2 ${
                  scanMode === 'IN' ? 'bg-brand-500 text-white shadow-sm' : 'text-slate-500 hover:bg-slate-50'
                }`}
                onClick={() => setScanMode('IN')}
              >
                <ArrowDownCircle size={16} />
                Scan IN
              </button>
              <button
                className={`flex-1 py-2 rounded-lg font-medium text-sm transition-all flex items-center justify-center gap-2 ${
                  scanMode === 'OUT' ? 'bg-rose-500 text-white shadow-sm' : 'text-slate-500 hover:bg-slate-50'
                }`}
                onClick={() => setScanMode('OUT')}
              >
                <ArrowUpCircle size={16} />
                Scan OUT
              </button>
            </div>

            <div className="text-center">
              <div className={`w-16 h-16 mx-auto rounded-full flex items-center justify-center mb-4 ${
                scanLoading ? 'animate-spin' : ''
              } ${scanMode === 'IN' ? 'bg-brand-100 text-brand-600' : 'bg-rose-100 text-rose-600'}`}>
                <Package size={28} />
              </div>
              <p className="font-medium text-slate-700">Ready to Scan</p>
              <p className="text-xs text-slate-500 mt-1">
                Point your scanner at a product barcode to {scanMode === 'IN' ? 'add to' : 'remove from'} this location.
              </p>
            </div>
          </div>
        </div>

        {/* Inventory List */}
        <div className="md:col-span-2">
          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
            <div className="p-4 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
              <h3 className="font-semibold text-slate-800">Current Inventory</h3>
              <span className="text-xs font-medium px-2 py-1 bg-slate-200 text-slate-600 rounded-md">
                Live Updates
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="bg-slate-50/50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="p-4 font-medium border-b border-slate-100">Product</th>
                    <th className="p-4 font-medium border-b border-slate-100">SKU</th>
                    <th className="p-4 font-medium border-b border-slate-100 text-right">Qty</th>
                  </tr>
                </thead>
                <tbody className="text-sm divide-y divide-slate-50">
                  {stocks.map((stock) => (
                    <tr key={stock.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="p-4 font-medium text-slate-800">
                        {stock.product?.display_name || stock.product?.name || '-'}
                      </td>
                      <td className="p-4 text-slate-500 font-mono text-xs">
                        {stock.product?.sku || '-'}
                      </td>
                      <td className="p-4 text-right">
                        <span className="inline-flex items-center justify-center min-w-[2rem] h-8 px-2 bg-brand-50 text-brand-700 font-semibold rounded-lg border border-brand-100">
                          {stock.quantity}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {stocks.length === 0 && (
                    <tr>
                      <td colSpan="3" className="p-12 text-center text-slate-400">
                        <Package size={32} className="mx-auto mb-3 opacity-20" />
                        <p>No products in this location.</p>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LocationView;
