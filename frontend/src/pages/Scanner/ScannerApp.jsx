import React, { useState, useEffect, useRef } from 'react';
import { toastSuccess, toastError } from '../../utils/toast';
import { scannerService } from '../../api/services/scannerService';
import { Scan, MapPin, ScanLine, Package, ArrowDownToLine, ArrowUpFromLine, ArrowRightLeft, Camera, Keyboard, Search, AlertTriangle, X, RefreshCw } from 'lucide-react';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import Html5QrcodePlugin from '../../components/common/Html5QrcodePlugin';

const ScannerApp = () => {
  const [currentPlacement, setCurrentPlacement] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  
  // List of items scanned in the current session
  const [scannedItems, setScannedItems] = useState([]);
  
  // Action Modal State
  const [actionModal, setActionModal] = useState({ isOpen: false, type: null, item: null });
  
  // Transfer destination code (used when moving products to another rack)
  const [destCode, setDestCode] = useState('');
  const [qty, setQty] = useState(1);
  const [notes, setNotes] = useState('');
  const [outReason, setOutReason] = useState('OTHER');
  const [opnameData, setOpnameData] = useState({});

  const inputRef = useRef(null);

  const [useCamera, setUseCamera] = useState(false);
  // Main Scan Input 
  const processScanCode = async (code) => {
    setLoading(true);
    try {
      const res = await scannerService.resolvePlacement(code);
      if (res.success) {
        const data = res.data;
        if (data.type === 'placement') {
          setCurrentPlacement(data);
          
          // Auto-populate the list with existing products in this placement
          const existingItems = (data.stocks || []).map(stock => ({
            id: stock.product_id,
            display_name: stock.product_name,
            name: stock.product_name, // fallback
            sku: stock.sku,
            currentStock: stock.quantity,
            scanTime: new Date()
          }));
          
          setScannedItems(prev => {
            if (prev.length === 0) return existingItems;
            
            // Preserve order: update currentStock of existing items
            const updatedPrev = prev.map(item => {
              const stock = data.stocks.find(s => s.product_id === item.id);
              return { ...item, currentStock: stock ? stock.quantity : 0 };
            });

            // Add any new items that weren't in the list
            const newItems = existingItems.filter(ei => !updatedPrev.some(up => up.id === ei.id));
            return [...newItems, ...updatedPrev];
          });
          
          if (res.data.type === 'placement' && !currentPlacement) {
            toastSuccess(`Placement switched to ${data.name}`);
          }
        } else if (data.type === 'product') {
          if (!currentPlacement) {
            toastError("Please scan a placement (Rak/Location) first before scanning products.");
          } else {
            const stockInPlacement = currentPlacement.stocks?.find(s => s.product_id === data.id)?.quantity || 0;
            setScannedItems(prev => [{ ...data, currentStock: stockInPlacement, scanTime: new Date() }, ...prev]);
            toastSuccess(`${data.name} scanned.`);
          }
        }
      }
    } catch (err) {
      toastError(err.response?.data?.message || "Code not recognized");
    } finally {
      setLoading(false);
    }
  };

  const handleScan = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;
    const code = inputValue.trim();
    setInputValue('');
    await processScanCode(code);
  };

  const onCameraScanSuccess = (decodedText) => {
    // html5-qrcode can trigger multiple times quickly, we can add a slight debounce if needed
    // For now we assume processScanCode handles it, but maybe close camera after successful scan?
    // Let's keep it open for continuous scanning but we might need a small debounce
    // Or just temporarily pause the scanner? The library handles some of it.
    processScanCode(decodedText);
    setUseCamera(false); // Close camera after scan to prevent duplicate scans
  };

  // Keep focus on input for hardware scanners
  useEffect(() => {
    const focusInput = () => {
      if (!actionModal.isOpen && inputRef.current && !useCamera) {
        inputRef.current.focus();
      }
    };
    
    focusInput();
    document.addEventListener('click', focusInput);
    return () => document.removeEventListener('click', focusInput);
  }, [actionModal.isOpen, useCamera]);

  const openAction = (type, item = null) => {
    setQty(1);
    setNotes('');
    setDestCode('');
    setOutReason('OTHER');
    
    if (type === 'OPNAME') {
      const initialOpname = {};
      scannedItems.forEach(i => initialOpname[i.id] = i.currentStock || 0);
      setOpnameData(initialOpname);
    }
    
    setActionModal({ isOpen: true, type, item });
  };

  const closeAction = () => {
    setActionModal({ isOpen: false, type: null, item: null });
  };

  const handleExecuteMovement = async () => {
    if (qty <= 0) {
      toastError("Quantity must be greater than 0");
      return;
    }

    let payload = {
      product_id: actionModal.item.id,
      quantity: qty,
      notes: notes
    };

    try {
      if (actionModal.type === 'IN') {
        payload.reason = 'RECEIVE_FROM_FACTORY';
        payload.destination_placement_id = currentPlacement.id;
      } else if (actionModal.type === 'OUT') {
        payload.reason = outReason; // Use selected reason
        payload.source_placement_id = currentPlacement.id;
      } else if (actionModal.type === 'MOVE') {
        // Need to resolve destination code to placement ID first
        if (!destCode) {
          toastError("Please scan destination placement");
          return;
        }
        const destRes = await scannerService.resolvePlacement(destCode);
        if (!destRes.success || destRes.data.type !== 'placement') {
          toastError("Destination code is not a valid placement");
          return;
        }
        payload.reason = 'SHOWROOM_TRANSFER';
        payload.source_placement_id = currentPlacement.id;
        payload.destination_placement_id = destRes.data.id;
      }

      const res = await scannerService.executeMovement(payload);
      if (res.success) {
        toastSuccess("Movement executed successfully");
        closeAction();
        // Refresh placement stock
        const placementRes = await scannerService.resolvePlacement(currentPlacement.code);
        if (placementRes.success) setCurrentPlacement(placementRes.data);
      } else {
        toastError(res.message);
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    }
  };

  const handleExecuteOpname = async () => {
    setLoading(true);
    try {
      const items = Object.entries(opnameData).map(([productId, actualQty]) => ({
        product_id: parseInt(productId),
        actual_quantity: actualQty
      }));
      
      const payload = {
        placement_id: currentPlacement.id,
        items: items,
        notes: notes || "Stock Opname"
      };

      const res = await scannerService.executeOpname(payload);
      if (res.success) {
        const adjustments = res.data.adjustments_made || [];
        toastSuccess(`Opname completed. ${adjustments.length} adjustments made.`);
        closeAction();
        // Refresh placement
        await processScanCode(currentPlacement.code);
      }
    } catch (err) {
      toastError(err.response?.data?.message || "Failed to execute opname");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full w-full max-w-lg mx-auto bg-slate-50 relative">
      
      {/* Scanner Dashboard / Header */}
      <div className="bg-slate-900 text-white p-4 rounded-b-3xl shadow-lg shrink-0">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2 text-brand-300">
            <MapPin size={20} />
            <span className="font-medium text-sm">CURRENT PLACEMENT</span>
          </div>
          {currentPlacement && (
             <span className="text-xs bg-slate-800 px-2 py-1 rounded-lg border border-slate-700">
               {currentPlacement.code}
             </span>
          )}
        </div>
        
        {currentPlacement ? (
          <div>
            <h2 className="text-2xl font-bold mb-2">{currentPlacement.name}</h2>
            <div className="flex gap-4 text-sm text-slate-400">
              <div className="flex flex-col">
                <span className="text-slate-500">Total SKU</span>
                <span className="text-white font-medium">{currentPlacement.stocks?.length || 0}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-slate-500">Total Qty</span>
                <span className="text-white font-medium">
                  {currentPlacement.stocks?.reduce((acc, curr) => acc + curr.quantity, 0) || 0}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="py-4 text-slate-400 flex flex-col items-center justify-center text-center">
            <Scan size={32} className="mb-2 opacity-50" />
            <p>Scan a Location Barcode to begin.</p>
          </div>
        )}
      </div>

      {/* Main Scan Input */}
      <div className="p-4 shrink-0 -mt-6">
        {useCamera ? (
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden p-2 relative">
            <div className="absolute top-4 right-4 z-10">
              <button 
                onClick={() => setUseCamera(false)}
                className="bg-slate-900/50 hover:bg-slate-900/80 text-white p-2 rounded-full backdrop-blur transition-colors"
              >
                <Keyboard size={20} />
              </button>
            </div>
            <Html5QrcodePlugin
              fps={10}
              qrbox={250}
              disableFlip={false}
              qrCodeSuccessCallback={onCameraScanSuccess}
            />
            <p className="text-center text-xs text-slate-500 mt-2">Point camera at a barcode</p>
          </div>
        ) : (
          <form onSubmit={handleScan} className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Scan className={`h-6 w-6 ${loading ? 'text-brand-500 animate-pulse' : 'text-slate-400'}`} />
            </div>
            <input
              ref={inputRef}
              type="text"
              className="block w-full pl-12 pr-12 py-4 bg-white border-2 border-transparent focus:border-brand-500 rounded-2xl shadow-xl text-lg font-mono text-center focus:outline-none transition-all"
              placeholder="SCAN BARCODE..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={loading}
              autoFocus
            />
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              <button 
                type="button"
                onClick={() => setUseCamera(true)}
                className="p-2 text-brand-600 hover:bg-brand-50 rounded-xl transition-colors"
              >
                <Camera size={24} />
              </button>
            </div>
          </form>
        )}
      </div>

      {/* Scanned Items List */}
      <div className="flex-1 overflow-y-auto p-4 pt-0">
        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Recently Scanned</h3>
        
        {scannedItems.length === 0 ? (
          <div className="text-center py-10 text-slate-400 flex flex-col items-center">
            <Package size={48} className="mb-2 opacity-20" />
            <p className="text-sm">No items scanned yet in this session.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {scannedItems.map((item, idx) => (
              <div key={idx} className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col gap-3">
                <div className="flex justify-between items-start">
                  <div className="flex flex-col">
                    <span className="font-bold text-slate-800 leading-tight">{item.display_name || item.name}</span>
                    <span className="text-xs text-slate-500 font-mono mt-1">{item.sku}</span>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Current Stock</span>
                    <span className="font-bold text-lg text-slate-700">{item.currentStock || 0}</span>
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-2 mt-1">
                  <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-emerald-50 !text-emerald-700 !border-emerald-200 hover:!bg-emerald-100" onClick={() => openAction('IN', item)}>
                    <ArrowDownToLine size={14} /> IN
                  </Button>
                  <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-blue-50 !text-blue-700 !border-blue-200 hover:!bg-blue-100" onClick={() => openAction('MOVE', item)}>
                    <ArrowRightLeft size={14} /> MOVE
                  </Button>
                  <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-rose-50 !text-rose-700 !border-rose-200 hover:!bg-rose-100" onClick={() => openAction('OUT', item)}>
                    <ArrowUpFromLine size={14} /> OUT
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions Footer (Only if Placement is selected) */}
      {currentPlacement && (
        <div className="p-4 pb-8 bg-white border-t border-slate-200 shrink-0 grid grid-cols-2 gap-2 shadow-[0_-4px_6px_-1px_rgb(0,0,0,0.05)]">
          <Button variant="secondary" className="flex flex-col items-center py-3 gap-1 h-auto" onClick={() => openAction('OPNAME')}>
            <Search size={20} className="text-brand-600" />
            <span className="text-xs font-semibold text-slate-700">Audit/Opname</span>
          </Button>
          <Button variant="outline" className="flex flex-col items-center py-3 gap-1 h-auto" onClick={() => {
            setCurrentPlacement(null);
            setScannedItems([]);
            toastSuccess("Session cleared");
          }}>
            <RefreshCw size={20} className="text-slate-500" />
            <span className="text-xs text-slate-600">Clear Session</span>
          </Button>
        </div>
      )}

      {/* Action Modals */}
      <Modal 
        isOpen={actionModal.isOpen} 
        onClose={closeAction}
        title={
          actionModal.type === 'IN' ? 'Stock Inbound' : 
          actionModal.type === 'OUT' ? 'Stock Outbound' :
          actionModal.type === 'MOVE' ? 'Transfer Product' : 
          actionModal.type === 'OPNAME' ? 'Stock Opname' : 'Report Issue'
        }
      >
        {actionModal.item && ['IN', 'OUT', 'MOVE'].includes(actionModal.type) && (
          <div className="space-y-4">
            
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              {actionModal.type === 'IN' && <p>Adding stock for <strong>{actionModal.item.display_name || actionModal.item.name}</strong> into <strong>{currentPlacement.name}</strong>.</p>}
              {actionModal.type === 'OUT' && <p>Removing stock for <strong>{actionModal.item.display_name || actionModal.item.name}</strong> from <strong>{currentPlacement.name}</strong>.</p>}
              {actionModal.type === 'MOVE' && <p>Moving <strong>{actionModal.item.display_name || actionModal.item.name}</strong> from <strong>{currentPlacement.name}</strong> to another location.</p>}
            </div>

            <div className="space-y-3">
               <div>
                 <label className="text-xs font-bold text-slate-700 uppercase">Quantity</label>
                 <input 
                   type="number" 
                   value={qty} 
                   onChange={(e) => setQty(Number(e.target.value))}
                   className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-lg font-bold" 
                   min="1"
                 />
               </div>
               
               {actionModal.type === 'MOVE' && (
                 <div>
                   <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1 block">Destination Rak Code</label>
                   <input
                     type="text"
                     value={destCode}
                     onChange={(e) => setDestCode(e.target.value.toUpperCase())}
                     placeholder="e.g. RAK-B02"
                     className="w-full bg-slate-50 border border-slate-300 rounded-lg p-3 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 font-mono"
                   />
                 </div>
               )}
               
               {actionModal.type === 'OUT' && (
                 <div>
                   <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1 block">Reason for Outbound</label>
                   <select
                     value={outReason}
                     onChange={(e) => setOutReason(e.target.value)}
                     className="w-full bg-slate-50 border border-slate-300 rounded-lg p-3 text-sm focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
                   >
                     <option value="OTHER">General Outbound</option>
                     <option value="DAMAGED">Damaged Item</option>
                     <option value="MISSING">Missing / Lost</option>
                     <option value="PHOTO_SHOOT">Photo Shoot</option>
                     <option value="SALES_SAMPLE">Sales Sample</option>
                   </select>
                 </div>
               )}

               <div>
                 <label className="text-xs font-bold text-slate-700 uppercase">Optional Notes</label>
                 <input 
                   type="text" 
                   value={notes}
                   onChange={(e) => setNotes(e.target.value)}
                   className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20" 
                   placeholder="E.g. from supplier PO-123..." 
                 />
               </div>
            </div>
            
            <div className="flex gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={closeAction}>Cancel</Button>
              <Button variant={actionModal.type === 'OUT' ? 'danger' : 'primary'} className="flex-1" onClick={handleExecuteMovement}>
                Confirm {actionModal.type}
              </Button>
            </div>
          </div>
        )}

        {actionModal.type === 'OPNAME' && (
          <div className="space-y-4">
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              <p>Audit stock for <strong>{currentPlacement.name}</strong>.</p>
              <p className="text-xs text-slate-500 mt-1">Update the actual physical quantities you found.</p>
            </div>
            
            <div className="max-h-60 overflow-y-auto space-y-2 pr-1">
              {scannedItems.map(item => (
                <div key={item.id} className="flex items-center justify-between p-2 border border-slate-200 rounded-lg">
                  <div className="flex flex-col overflow-hidden">
                    <span className="text-sm font-semibold truncate max-w-[150px]">{item.display_name || item.name}</span>
                    <span className="text-xs text-slate-500">Sys: {item.currentStock || 0}</span>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className="text-xs font-semibold text-slate-600">Actual:</span>
                    <input
                      type="number"
                      min="0"
                      value={opnameData[item.id] !== undefined ? opnameData[item.id] : ''}
                      onChange={(e) => setOpnameData({...opnameData, [item.id]: parseInt(e.target.value) || 0})}
                      className="w-16 p-1 text-center border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-brand-500"
                    />
                  </div>
                </div>
              ))}
              {scannedItems.length === 0 && (
                <p className="text-sm text-slate-500 text-center py-4">No items scanned in this placement.</p>
              )}
            </div>

            <div>
              <label className="text-xs font-bold text-slate-700 uppercase">Optional Notes</label>
              <input 
                type="text" 
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 mt-1" 
                placeholder="e.g. Audit by John" 
              />
            </div>
            
            <div className="flex gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={closeAction}>Cancel</Button>
              <Button variant="primary" className="flex-1" onClick={handleExecuteOpname} isLoading={loading}>
                Submit Opname
              </Button>
            </div>
          </div>
        )}
      </Modal>

    </div>
  );
};

export default ScannerApp;
