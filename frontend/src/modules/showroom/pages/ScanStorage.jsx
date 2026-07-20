import React, { useState, useEffect, useRef } from 'react';
import { toastSuccess, toastError } from '../../../utils/toast';
import { showroomService } from '../../../api/services/showroomService';
import { Scan, MapPin, ScanLine, Package, ArrowDownToLine, ArrowUpFromLine, Search, Camera, Keyboard, RefreshCw, ClipboardList, Layers, Plus } from 'lucide-react';
import Button from '../../../components/common/Button';
import Modal from '../../../components/common/Modal';
import Html5QrcodePlugin from '../../../components/common/Html5QrcodePlugin';

const OUT_REASONS = [
  { value: 'OTHER', label: 'Lainnya' },
  { value: 'DAMAGED', label: 'Rusak' },
  { value: 'MISSING', label: 'Hilang' },
  { value: 'PHOTO_SHOOT', label: 'Fotografi' },
  { value: 'SALES_SAMPLE', label: 'Sample Sales' },
];

const SAMPLE_TYPES = [
  { value: 'Display', label: 'Display' },
  { value: 'Photography', label: 'Fotografi' },
  { value: 'Premium', label: 'Premium' },
  { value: 'Archive', label: 'Arsip' },
];

const ScanStorage = () => {
  const [currentPlacement, setCurrentPlacement] = useState(null);
  const [currentToken, setCurrentToken] = useState('');
  const [entityType, setEntityType] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [scannedItems, setScannedItems] = useState([]);
  const [actionModal, setActionModal] = useState({ isOpen: false, type: null, item: null });
  const [qty, setQty] = useState(1);
  const [notes, setNotes] = useState('');
  const [sampleType, setSampleType] = useState('Display');
  const [outReason, setOutReason] = useState('OTHER');
  const [destToken, setDestToken] = useState('');
  const [inventoryResult, setInventoryResult] = useState(null);
  const [productResult, setProductResult] = useState(null);
  const [opnameData, setOpnameData] = useState({});
  const inputRef = useRef(null);
  const [useCamera, setUseCamera] = useState(false);
  const [addProductModal, setAddProductModal] = useState(false);
  const [productSearch, setProductSearch] = useState('');
  const [allProducts, setAllProducts] = useState([]);
  const [productsLoading, setProductsLoading] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [addQty, setAddQty] = useState(1);
  const [addSampleType, setAddSampleType] = useState('Display');

  const processScanCode = async (code) => {
    setLoading(true);
    setProductResult(null);
    try {
      const res = await showroomService.resolveQR(code.trim());
      if (res.success !== false) {
        const data = res.data;
        const qrInfo = data.qr || {};
        const entType = qrInfo.entity_type;
        const entity = data.entity;

        if (entType === 'storage' || entType === 'location') {
          setCurrentToken(code.trim());
          setEntityType(entType);
          setCurrentPlacement(entity);
          try {
            const invRes = await showroomService.storageScan({ token: code.trim(), action: 'CHECK_INVENTORY' });
            if (invRes.success !== false) {
              const items = (invRes.data?.items || []).map(item => ({
                id: item.product_id,
                display_name: item.product_name,
                name: item.product_name,
                sku: item.sku,
                currentStock: item.quantity,
                sample_type: item.sample_type,
                category: item.category,
                motif: item.motif,
                sub_motif: item.sub_motif,
                variant: item.variant,
                scanTime: new Date(),
              }));
              setScannedItems(items);
            }
          } catch (_) {}
          toastSuccess(`${entType === 'storage' ? 'Storage' : 'Lokasi'}: ${entity.name}`);
        } else if (entType === 'product') {
          if (!currentPlacement) {
            try {
              const checkRes = await showroomService.productScan({ token: code.trim(), action: 'CHECK_STOCK' });
              if (checkRes.success !== false) {
                setProductResult(checkRes.data);
                toastSuccess(`Detail ${entity.display_name}`);
              }
            } catch (_) {
              toastError('Scan lokasi/storage terlebih dahulu');
            }
            return;
          }
          const stockInStorage = scannedItems.find(s => s.id === entity.id)?.currentStock || 0;
          setScannedItems(prev => {
            const exists = prev.find(s => s.id === entity.id);
            if (exists) return prev;
            return [{
              id: entity.id,
              display_name: entity.display_name,
              name: entity.display_name,
              sku: entity.sku,
              currentStock: stockInStorage,
              category: entity.category,
              motif: entity.motif,
              sub_motif: entity.sub_motif,
              variant: entity.variant,
              scanTime: new Date(),
            }, ...prev];
          });
          toastSuccess(`${entity.display_name} ditambahkan`);
        }
      }
    } catch (err) {
      toastError(err.response?.data?.detail || err.response?.data?.message || 'Kode tidak dikenal');
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
    processScanCode(decodedText);
    setUseCamera(false);
  };

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

  const openAddProductModal = async () => {
    setAddProductModal(true);
    setProductSearch('');
    setSelectedProduct(null);
    setAddQty(1);
    setAddSampleType('Display');
    if (allProducts.length === 0) {
      setProductsLoading(true);
      try {
        const res = await showroomService.getProducts();
        if (res.success) {
          setAllProducts(res.data);
        }
      } catch (_) {} finally {
        setProductsLoading(false);
      }
    }
  };

  const closeAddProductModal = () => {
    setAddProductModal(false);
  };

  const handleAddProduct = () => {
    if (!selectedProduct) return;
    const p = selectedProduct;
    setScannedItems(prev => {
      const exists = prev.find(s => s.id === p.id);
      if (exists) {
        return prev.map(s => s.id === p.id ? { ...s, currentStock: s.currentStock + addQty } : s);
      }
      return [{
        id: p.id,
        display_name: p.display_name || p.name,
        name: p.display_name || p.name,
        sku: p.sku,
        currentStock: addQty,
        sample_type: addSampleType,
        category: p.category || null,
        motif: p.motif || null,
        sub_motif: p.sub_motif || null,
        scanTime: new Date(),
      }, ...prev];
    });
    toastSuccess(`${p.display_name || p.name} ditambahkan (${addQty} ${addSampleType})`);
    closeAddProductModal();
  };

  const openAction = (type, item = null) => {
    setQty(1);
    setNotes('');
    setSampleType('Display');
    setOutReason('OTHER');
    setDestToken('');
    setInventoryResult(null);
    if (type === 'OPNAME') {
      const initial = {};
      scannedItems.forEach(i => { initial[i.id] = { qty: i.currentStock || 0, sample_type: i.sample_type || 'Display' }; });
      setOpnameData(initial);
    }
    setActionModal({ isOpen: true, type, item });
  };

  const closeAction = () => {
    setActionModal({ isOpen: false, type: null, item: null });
    setInventoryResult(null);
    setProductResult(null);
  };

  const refreshItems = async () => {
    if (!currentToken) return;
    try {
      const invRes = await showroomService.storageScan({ token: currentToken, action: 'CHECK_INVENTORY' });
      if (invRes.success !== false) {
        const items = (invRes.data?.items || []).map(item => ({
          id: item.product_id,
          display_name: item.product_name,
          name: item.product_name,
          sku: item.sku,
          currentStock: item.quantity,
          sample_type: item.sample_type,
          category: item.category,
          motif: item.motif,
          sub_motif: item.sub_motif,
          variant: item.variant,
          scanTime: new Date(),
        }));
        setScannedItems(items);
      }
    } catch (_) {}
  };

  const handleStockIn = async () => {
    if (qty <= 0) { toastError('Qty harus > 0'); return; }
    setLoading(true);
    try {
      const res = await showroomService.storageScan({
        token: currentToken, action: 'STOCK_IN',
        product_id: actionModal.item.id, quantity: qty, sample_type: sampleType,
      });
      if (res.success !== false) {
        toastSuccess('Stock in berhasil');
        closeAction();
        await refreshItems();
      }
    } catch (err) {
      toastError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleStockOut = async () => {
    if (qty <= 0) { toastError('Qty harus > 0'); return; }
    setLoading(true);
    try {
      const res = await showroomService.storageScan({
        token: currentToken, action: 'STOCK_OUT',
        product_id: actionModal.item.id, quantity: qty, sample_type: sampleType,
      });
      if (res.success !== false) {
        toastSuccess('Stock out berhasil');
        closeAction();
        await refreshItems();
      }
    } catch (err) {
      toastError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleMove = async () => {
    if (qty <= 0) { toastError('Qty harus > 0'); return; }
    if (!destToken.trim()) { toastError('Scan token tujuan'); return; }
    setLoading(true);
    try {
      const destRes = await showroomService.resolveQR(destToken.trim());
      if (destRes.success === false || !['storage', 'location'].includes(destRes.data?.qr?.entity_type)) {
        toastError('Token tujuan bukan storage/lokasi'); return;
      }
      const outRes = await showroomService.storageScan({
        token: currentToken, action: 'STOCK_OUT',
        product_id: actionModal.item.id, quantity: qty, sample_type: sampleType,
      });
      if (outRes.success !== false) {
        await showroomService.storageScan({
          token: destToken.trim(), action: 'STOCK_IN',
          product_id: actionModal.item.id, quantity: qty, sample_type: sampleType,
        });
        toastSuccess('Pindah barang berhasil');
        closeAction();
        await refreshItems();
      }
    } catch (err) {
      toastError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOpname = async () => {
    const items = Object.entries(opnameData).map(([productId, val]) => ({
      product_id: parseInt(productId),
      actual_quantity: val.qty,
      sample_type: val.sample_type || 'Display',
    }));
    if (items.length === 0) { toastError('Tidak ada item'); return; }
    setLoading(true);
    try {
      const res = await showroomService.storageScan({
        token: currentToken, action: 'STOCK_OPNAME', items,
      });
      if (res.success !== false) {
        const adjCount = res.data?.adjustments?.filter(a => a.variance !== 0).length || 0;
        toastSuccess(`Opname selesai. ${adjCount} penyesuaian.`);
        closeAction();
        await refreshItems();
      }
    } catch (err) {
      toastError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckInventory = async () => {
    if (!currentToken) return;
    setLoading(true);
    try {
      const res = await showroomService.storageScan({ token: currentToken, action: 'CHECK_INVENTORY' });
      if (res.success !== false) {
        setInventoryResult(res.data);
        const items = (res.data?.items || []).map(item => ({
          id: item.product_id,
          display_name: item.product_name,
          name: item.product_name,
          sku: item.sku,
          currentStock: item.quantity,
          sample_type: item.sample_type,
          category: item.category,
          motif: item.motif,
          sub_motif: item.sub_motif,
          variant: item.variant,
          scanTime: new Date(),
        }));
        setScannedItems(items);
        toastSuccess('Inventory di-refresh');
      }
    } catch (err) {
      toastError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  const showCategoryInfo = (item) => {
    const parts = [];
    if (item.category?.name) parts.push(item.category.name);
    if (item.motif?.name) parts.push(item.motif.name);
    if (item.sub_motif?.name) parts.push(item.sub_motif.name);
    return parts.length > 0 ? parts.join(' / ') : null;
  };

  const getHeaderTitle = () => {
    if (!currentPlacement) return '';
    return entityType === 'location' ? 'Lokasi' : 'Storage';
  };

  return (
    <div className="flex flex-col h-full w-full max-w-lg mx-auto bg-slate-50 relative">

      <div className="bg-slate-900 text-white p-4 rounded-b-3xl shadow-lg shrink-0">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2 text-brand-300">
            <MapPin size={20} />
            <span className="font-medium text-sm">{getHeaderTitle() || 'SCAN QR'}</span>
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
                <span className="text-white font-medium">{scannedItems.length}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-slate-500">Total Qty</span>
                <span className="text-white font-medium">
                  {scannedItems.reduce((acc, curr) => acc + (curr.currentStock || 0), 0)}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="py-4 text-slate-400 flex flex-col items-center justify-center text-center">
            <Scan size={32} className="mb-2 opacity-50" />
            <p>Scan QR Storage / Lokasi untuk memulai</p>
          </div>
        )}
      </div>

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
              fps={10} qrbox={250} disableFlip={false}
              qrCodeSuccessCallback={onCameraScanSuccess}
            />
            <p className="text-center text-xs text-slate-500 mt-2">Arahkan kamera ke QR</p>
          </div>
        ) : (
          <form onSubmit={handleScan} className="relative">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <ScanLine className={`h-6 w-6 ${loading ? 'text-brand-500 animate-pulse' : 'text-slate-400'}`} />
            </div>
            <input
              ref={inputRef}
              type="text"
              className="block w-full pl-12 pr-12 py-4 bg-white border-2 border-transparent focus:border-brand-500 rounded-2xl shadow-xl text-lg font-mono text-center focus:outline-none transition-all"
              placeholder="SCAN QR TOKEN..."
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

      {productResult && (
        <div className="px-4 pb-2 shrink-0">
          <div className="bg-white rounded-xl border border-sky-200 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-slate-800">{productResult.product_name}</h3>
              <button onClick={() => setProductResult(null)} className="text-slate-400 hover:text-slate-600 text-xs">Tutup</button>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div><span className="text-slate-500">SKU:</span> <span className="font-mono text-xs">{productResult.sku}</span></div>
              {productResult.category && <div><span className="text-slate-500">Kategori:</span> {productResult.category.name}</div>}
              {productResult.motif && <div><span className="text-slate-500">Motif:</span> {productResult.motif.name}</div>}
              {productResult.sub_motif && <div><span className="text-slate-500">Sub Motif:</span> {productResult.sub_motif.name}</div>}
            </div>
            <div className="text-sm font-medium text-slate-700 mt-1">Lokasi Penyimpanan:</div>
            {productResult.items?.length > 0 ? (
              <div className="space-y-1">
                {productResult.items.map((loc, i) => (
                  <div key={i} className="flex justify-between text-sm bg-slate-50 rounded-lg p-2">
                    <span className="text-slate-700">{loc.location_name}{loc.storage_name ? ` / ${loc.storage_name}` : ''}</span>
                    <span className="font-semibold">{loc.quantity} {loc.sample_type ? `(${loc.sample_type})` : ''}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400">Tidak ada stok di lokasi manapun</p>
            )}
          </div>
        </div>
      )}

      {inventoryResult && !actionModal.isOpen && !productResult && (
        <div className="px-4 pb-2 shrink-0">
          <div className="bg-white rounded-xl border border-slate-200 p-3 text-sm flex items-center justify-between">
            <span className="text-slate-500">
              <span className="font-semibold text-slate-700">{inventoryResult.total_items}</span> total qty,{' '}
              <span className="font-semibold text-slate-700">{inventoryResult.items?.length || 0}</span> SKU
            </span>
            <button onClick={() => setInventoryResult(null)} className="text-slate-400 hover:text-slate-600"><Keyboard size={14} /></button>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-4 pt-0">
        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Produk</h3>

        {scannedItems.length === 0 ? (
          <div className="text-center py-10 text-slate-400 flex flex-col items-center">
            <Package size={48} className="mb-2 opacity-20" />
            <p className="text-sm">Scan QR Storage/Lokasi untuk melihat daftar produk</p>
          </div>
        ) : (
          <div className="space-y-3">
            {scannedItems.map((item, idx) => {
              const catInfo = showCategoryInfo(item);
              return (
                <div key={item.id || idx} className="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col gap-3">
                  <div className="flex justify-between items-start">
                    <div className="flex flex-col min-w-0">
                      <span className="font-bold text-slate-800 leading-tight">{item.display_name || item.name}</span>
                      <span className="text-xs text-slate-500 font-mono mt-1">{item.sku || `ID: ${item.id}`}</span>
                      {catInfo && (
                        <span className="text-[11px] text-slate-400 mt-1 flex items-center gap-1">
                          <Layers size={12} /> {catInfo}
                        </span>
                      )}
                    </div>
                    <div className="flex flex-col items-end shrink-0">
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider">Stock</span>
                      <span className="font-bold text-lg text-slate-700">{item.currentStock || 0}</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-4 gap-2 mt-1">
                    <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-emerald-50 !text-emerald-700 !border-emerald-200 hover:!bg-emerald-100" onClick={() => openAction('IN', item)}>
                      <ArrowDownToLine size={14} /> IN
                    </Button>
                    <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-sky-50 !text-sky-700 !border-sky-200 hover:!bg-sky-100" onClick={() => openAction('CEK', item)}>
                      <ClipboardList size={14} /> CEK
                    </Button>
                    <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-amber-50 !text-amber-700 !border-amber-200 hover:!bg-amber-100" onClick={() => openAction('MOVE', item)}>
                      <Search size={14} /> PINDAH
                    </Button>
                    <Button size="sm" variant="outline" className="flex items-center justify-center gap-1 !bg-rose-50 !text-rose-700 !border-rose-200 hover:!bg-rose-100" onClick={() => openAction('OUT', item)}>
                      <ArrowUpFromLine size={14} /> OUT
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {currentPlacement && (
        <div className="p-4 pb-8 bg-white border-t border-slate-200 shrink-0 grid grid-cols-4 gap-2 shadow-[0_-4px_6px_-1px_rgb(0,0,0,0.05)]">
          <Button variant="secondary" className="flex flex-col items-center py-3 gap-1 h-auto" onClick={handleCheckInventory}>
            <Search size={20} className="text-brand-600" />
            <span className="text-xs font-semibold text-slate-700">Inventory</span>
          </Button>
          <Button variant="secondary" className="flex flex-col items-center py-3 gap-1 h-auto" onClick={() => openAction('OPNAME')}>
            <ClipboardList size={20} className="text-brand-600" />
            <span className="text-xs font-semibold text-slate-700">Opname</span>
          </Button>
          <Button variant="primary" className="flex flex-col items-center py-3 gap-1 h-auto" onClick={openAddProductModal}>
            <Plus size={20} />
            <span className="text-xs font-semibold">Tambah Produk</span>
          </Button>
          <Button variant="outline" className="flex flex-col items-center py-3 gap-1 h-auto" onClick={() => {
            setCurrentPlacement(null);
            setCurrentToken('');
            setEntityType('');
            setScannedItems([]);
            setInventoryResult(null);
            setProductResult(null);
            toastSuccess('Sesi dibersihkan');
          }}>
            <RefreshCw size={20} className="text-slate-500" />
            <span className="text-xs text-slate-600">Bersihkan</span>
          </Button>
        </div>
      )}

      <Modal
        isOpen={actionModal.isOpen}
        onClose={closeAction}
        title={
          actionModal.type === 'IN' ? 'Stock In' :
          actionModal.type === 'OUT' ? 'Stock Out' :
          actionModal.type === 'MOVE' ? 'Pindah Storage' :
          actionModal.type === 'CEK' ? 'Cek Stok' :
          actionModal.type === 'OPNAME' ? 'Stock Opname' : ''
        }
      >
        {actionModal.type === 'IN' && actionModal.item && (
          <div className="space-y-4">
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              <p>Tambah stok <strong>{actionModal.item.display_name || actionModal.item.name}</strong> ke <strong>{currentPlacement?.name}</strong></p>
            </div>
            <div className="space-y-3">
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Jumlah</label>
                <input type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-lg font-bold" min="1" />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Tipe Sample</label>
                <select value={sampleType} onChange={(e) => setSampleType(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20">
                  {SAMPLE_TYPES.map(st => (<option key={st.value} value={st.value}>{st.label}</option>))}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Catatan</label>
                <input type="text" value={notes} onChange={(e) => setNotes(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20" placeholder="Opsional..." />
              </div>
            </div>
            <div className="flex gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={closeAction}>Batal</Button>
              <Button variant="primary" className="flex-1" onClick={handleStockIn} isLoading={loading}>Simpan</Button>
            </div>
          </div>
        )}

        {actionModal.type === 'OUT' && actionModal.item && (
          <div className="space-y-4">
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              <p>Kurangi stok <strong>{actionModal.item.display_name || actionModal.item.name}</strong> dari <strong>{currentPlacement?.name}</strong></p>
              <p className="text-xs text-slate-500 mt-1">Stok saat ini: <strong>{actionModal.item.currentStock || 0}</strong></p>
            </div>
            <div className="space-y-3">
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Jumlah</label>
                <input type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-lg font-bold" min="1" />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Tipe Sample</label>
                <select value={sampleType} onChange={(e) => setSampleType(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20">
                  {SAMPLE_TYPES.map(st => (<option key={st.value} value={st.value}>{st.label}</option>))}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Alasan</label>
                <select value={outReason} onChange={(e) => setOutReason(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20">
                  {OUT_REASONS.map(r => (<option key={r.value} value={r.value}>{r.label}</option>))}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Catatan</label>
                <input type="text" value={notes} onChange={(e) => setNotes(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20" placeholder="Opsional..." />
              </div>
            </div>
            <div className="flex gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={closeAction}>Batal</Button>
              <Button variant="danger" className="flex-1" onClick={handleStockOut} isLoading={loading}>Keluarkan</Button>
            </div>
          </div>
        )}

        {actionModal.type === 'MOVE' && actionModal.item && (
          <div className="space-y-4">
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              <p>Pindahkan <strong>{actionModal.item.display_name || actionModal.item.name}</strong> dari <strong>{currentPlacement?.name}</strong></p>
            </div>
            <div className="space-y-3">
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Jumlah</label>
                <input type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-lg font-bold" min="1" />
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Tipe Sample</label>
                <select value={sampleType} onChange={(e) => setSampleType(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20">
                  {SAMPLE_TYPES.map(st => (<option key={st.value} value={st.value}>{st.label}</option>))}
                </select>
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Token Tujuan</label>
                <div className="flex gap-2">
                  <input type="text" value={destToken} onChange={(e) => setDestToken(e.target.value)} placeholder="Scan atau ketik token..." className="flex-1 p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 font-mono text-sm" />
                  <Button size="sm" variant="outline" onClick={async () => {
                    if (!destToken.trim()) { toastError('Masukkan token'); return; }
                    try {
                      const destRes = await showroomService.resolveQR(destToken.trim());
                      if (destRes.success !== false && ['storage', 'location'].includes(destRes.data?.qr?.entity_type)) {
                        toastSuccess(`Tujuan: ${destRes.data.entity.name}`);
                      } else { toastError('Token tidak valid'); }
                    } catch (_) { toastError('Token tidak dikenal'); }
                  }}>Cek</Button>
                </div>
              </div>
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase">Catatan</label>
                <input type="text" value={notes} onChange={(e) => setNotes(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20" placeholder="Opsional..." />
              </div>
            </div>
            <div className="flex gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={closeAction}>Batal</Button>
              <Button variant="primary" className="flex-1" onClick={handleMove} isLoading={loading}>Pindahkan</Button>
            </div>
          </div>
        )}

        {actionModal.type === 'CEK' && actionModal.item && (
          <div className="space-y-4">
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              <p>Detail stok <strong>{actionModal.item.display_name || actionModal.item.name}</strong></p>
            </div>
            <div className="bg-white border border-slate-200 rounded-lg p-4 text-sm space-y-2">
              <div className="flex justify-between"><span className="text-slate-500">Nama</span><span className="font-semibold">{actionModal.item.display_name || actionModal.item.name}</span></div>
              {actionModal.item.sku && <div className="flex justify-between"><span className="text-slate-500">SKU</span><span className="font-mono text-xs">{actionModal.item.sku}</span></div>}
              {actionModal.item.category?.name && <div className="flex justify-between"><span className="text-slate-500">Kategori</span><span>{actionModal.item.category.name}</span></div>}
              {actionModal.item.motif?.name && <div className="flex justify-between"><span className="text-slate-500">Motif</span><span>{actionModal.item.motif.name}</span></div>}
              {actionModal.item.sub_motif?.name && <div className="flex justify-between"><span className="text-slate-500">Sub Motif</span><span>{actionModal.item.sub_motif.name}</span></div>}
              <div className="flex justify-between"><span className="text-slate-500">Stok</span><span className="font-bold text-lg">{actionModal.item.currentStock || 0}</span></div>
              <div className="flex justify-between"><span className="text-slate-500">Lokasi</span><span>{currentPlacement?.name}</span></div>
            </div>
            <div className="flex justify-end pt-2"><Button variant="outline" onClick={closeAction}>Tutup</Button></div>
          </div>
        )}

        {actionModal.type === 'OPNAME' && (
          <div className="space-y-4">
            <div className="bg-slate-100 p-3 rounded-lg text-sm text-slate-700">
              <p>Opname stok di <strong>{currentPlacement?.name}</strong></p>
              <p className="text-xs text-slate-500 mt-1">Masukkan jumlah fisik untuk setiap produk.</p>
            </div>
            <div className="max-h-60 overflow-y-auto space-y-2 pr-1">
              {scannedItems.map(item => (
                <div key={item.id} className="flex items-center justify-between p-2 border border-slate-200 rounded-lg">
                  <div className="flex flex-col overflow-hidden min-w-0 flex-1">
                    <span className="text-sm font-semibold truncate">{item.display_name || item.name}</span>
                    <span className="text-xs text-slate-400 truncate">
                      {item.category?.name || ''}{item.motif?.name ? ` / ${item.motif.name}` : ''}{item.sub_motif?.name ? ` / ${item.sub_motif.name}` : ''}
                    </span>
                    <span className="text-[11px] text-slate-500">Sistem: {item.currentStock || 0}</span>
                  </div>
                  <div className="flex items-center gap-2 shrink-0 ml-2">
                    <span className="text-xs font-semibold text-slate-600">Aktual:</span>
                    <input
                      type="number" min="0"
                      value={opnameData[item.id]?.qty !== undefined ? opnameData[item.id].qty : ''}
                      onChange={(e) => setOpnameData({ ...opnameData, [item.id]: { ...opnameData[item.id], qty: parseInt(e.target.value) || 0, sample_type: item.sample_type || 'Display' } })}
                      className="w-16 p-1 text-center border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-brand-500 text-sm"
                    />
                  </div>
                </div>
              ))}
              {scannedItems.length === 0 && (
                <p className="text-sm text-slate-500 text-center py-4">Tidak ada produk.</p>
              )}
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase">Catatan</label>
              <input type="text" value={notes} onChange={(e) => setNotes(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 mt-1" placeholder="Opsional..." />
            </div>
            <div className="flex gap-2 pt-4 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={closeAction}>Batal</Button>
              <Button variant="primary" className="flex-1" onClick={handleOpname} isLoading={loading}>Simpan Opname</Button>
            </div>
          </div>
        )}
      </Modal>

      <Modal isOpen={addProductModal} onClose={closeAddProductModal} title="Tambah Produk">
        <div className="space-y-4">
          <div>
            <label className="text-xs font-bold text-slate-700 uppercase mb-1 block">Cari Produk</label>
            <input
              type="text"
              value={productSearch}
              onChange={(e) => setProductSearch(e.target.value)}
              placeholder="Ketik nama atau SKU produk..."
              className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-sm"
              autoFocus
            />
          </div>

          <div className="max-h-52 overflow-y-auto space-y-1 border border-slate-200 rounded-lg p-1">
            {productsLoading ? (
              <div className="py-8 text-center text-sm text-slate-400">Memuat produk...</div>
            ) : (
              (() => {
                const filtered = allProducts.filter(p => {
                  const q = productSearch.toLowerCase();
                  if (!q) return true;
                  return (p.display_name || p.name || '').toLowerCase().includes(q) ||
                         (p.sku || '').toLowerCase().includes(q);
                });
                return filtered.length === 0 ? (
                  <div className="py-8 text-center text-sm text-slate-400">
                    {productSearch ? 'Produk tidak ditemukan' : 'Tidak ada produk'}
                  </div>
                ) : (
                  filtered.map(p => (
                    <button
                      key={p.id}
                      onClick={() => setSelectedProduct(p)}
                      className={`w-full text-left p-2.5 rounded-lg text-sm transition-colors ${
                        selectedProduct?.id === p.id
                          ? 'bg-indigo-100 border border-indigo-300'
                          : 'hover:bg-slate-50 border border-transparent'
                      }`}
                    >
                      <span className="font-semibold text-slate-800 block truncate">{p.display_name || p.name}</span>
                      <span className="text-[11px] text-slate-400 font-mono">{p.sku}</span>
                    </button>
                  ))
                );
              })()
            )}
          </div>

          {selectedProduct && (
            <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-3 space-y-3">
              <p className="text-sm font-semibold text-indigo-800">
                {selectedProduct.display_name || selectedProduct.name}
                <span className="text-xs font-mono text-indigo-500 ml-2">{selectedProduct.sku}</span>
              </p>
              <div className="flex gap-3">
                <div className="flex-1">
                  <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Jumlah</label>
                  <input
                    type="number" min="1"
                    value={addQty}
                    onChange={(e) => setAddQty(Math.max(1, parseInt(e.target.value) || 1))}
                    className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 text-lg font-bold"
                  />
                </div>
                <div className="flex-1">
                  <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Tipe Sample</label>
                  <select
                    value={addSampleType}
                    onChange={(e) => setAddSampleType(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20"
                  >
                    {SAMPLE_TYPES.map(st => <option key={st.value} value={st.value}>{st.label}</option>)}
                  </select>
                </div>
              </div>
            </div>
          )}

          <div className="flex gap-2 pt-2 border-t border-slate-100">
            <Button variant="outline" className="flex-1" onClick={closeAddProductModal}>Batal</Button>
            <Button variant="primary" className="flex-1" onClick={handleAddProduct} disabled={!selectedProduct}>
              {selectedProduct ? 'Tambah ke Daftar' : 'Pilih produk'}
            </Button>
          </div>
        </div>
      </Modal>

    </div>
  );
};

export default ScanStorage;
