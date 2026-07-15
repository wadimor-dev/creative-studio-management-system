import React, { useState, useRef, useEffect } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import ProductsTabs from './components/ProductsTabs';
import { QrCode, Printer, FileText, CheckSquare, Square, Settings } from 'lucide-react';
import { useReactToPrint } from 'react-to-print';
import { QRCodeSVG } from 'qrcode.react';
import Barcode from 'react-barcode';
import { usePlacements } from '../../hooks/usePlacements';
import SearchableSelect from '../../components/common/SearchableSelect';
import { productService } from '../../api/services/productService';
import { toastSuccess } from '../../utils/toast';

const DEFAULT_PRINTER_SETTINGS = {
  width: 50,
  height: 30,
  margin: 2
};

const getPrinterSettings = () => {
  const saved = localStorage.getItem('printerSettings');
  if (saved) {
    try {
      return JSON.parse(saved);
    } catch (e) {
      return DEFAULT_PRINTER_SETTINGS;
    }
  }
  return DEFAULT_PRINTER_SETTINGS;
};

const PrinterSettingsModal = ({ isOpen, onClose, onSave }) => {
  const [settings, setSettings] = useState(getPrinterSettings());

  const handleSave = () => {
    localStorage.setItem('printerSettings', JSON.stringify(settings));
    onSave(settings);
    toastSuccess('Printer settings saved successfully');
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Printer Settings">
      <div className="space-y-4">
        <p className="text-sm text-slate-500">
          Configure the dimensions for your label printer. These settings apply to the physical paper size (e.g. thermal stickers).
        </p>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Label Width (mm)</label>
            <input
              type="number"
              value={settings.width}
              onChange={(e) => setSettings({...settings, width: Number(e.target.value)})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Label Height (mm)</label>
            <input
              type="number"
              value={settings.height}
              onChange={(e) => setSettings({...settings, height: Number(e.target.value)})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>
          <div className="col-span-2">
            <label className="block text-sm font-medium text-slate-700 mb-1">Margin (mm)</label>
            <input
              type="number"
              value={settings.margin}
              onChange={(e) => setSettings({...settings, margin: Number(e.target.value)})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            />
          </div>
        </div>

        <div className="mt-4 p-4 bg-slate-50 border border-slate-200 rounded-lg">
          <h4 className="text-xs font-semibold text-slate-500 uppercase mb-2">Preview Layout</h4>
          <div className="flex justify-center">
            <div 
              style={{
                width: `${settings.width * 3}px`,
                height: `${settings.height * 3}px`,
                padding: `${settings.margin * 3}px`,
                backgroundColor: 'white',
                border: '1px solid #cbd5e1',
                boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
              }}
              className="flex items-center justify-center relative"
            >
              <div className="w-full h-full border border-dashed border-brand-200 bg-brand-50 flex items-center justify-center text-[10px] text-brand-600 text-center leading-tight">
                Print Area
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button variant="primary" onClick={handleSave}>Save Settings</Button>
        </div>
      </div>
    </Modal>
  );
};

const SingleGeneratorModal = ({ isOpen, onClose, settings }) => {
  const [code, setCode] = useState('');
  const [type, setType] = useState('QR'); // QR or BARCODE
  const [source, setSource] = useState('MANUAL'); // MANUAL, PRODUCT, PLACEMENT
  const printRef = useRef(null);

  const { placements } = usePlacements(false);
  const [products, setProducts] = useState([]);
  const [loadingProducts, setLoadingProducts] = useState(false);

  useEffect(() => {
    if (source === 'PRODUCT' && products.length === 0) {
      setLoadingProducts(true);
      productService.getAll()
        .then(res => {
          if (res.success) setProducts(res.data);
        })
        .finally(() => setLoadingProducts(false));
    }
  }, [source, products.length]);

  const handlePrint = useReactToPrint({
    contentRef: printRef,
  });

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Single Barcode Generator">
      <div className="space-y-4">
        
        <div className="flex gap-2 bg-slate-100 p-1 rounded-lg">
          <button 
            className={`flex-1 py-1.5 text-sm font-medium rounded-md ${source === 'MANUAL' ? 'bg-white shadow-sm text-brand-600' : 'text-slate-500'}`}
            onClick={() => { setSource('MANUAL'); setCode(''); }}
          >
            Manual
          </button>
          <button 
            className={`flex-1 py-1.5 text-sm font-medium rounded-md ${source === 'PRODUCT' ? 'bg-white shadow-sm text-brand-600' : 'text-slate-500'}`}
            onClick={() => { setSource('PRODUCT'); setCode(''); }}
          >
            Product
          </button>
          <button 
            className={`flex-1 py-1.5 text-sm font-medium rounded-md ${source === 'PLACEMENT' ? 'bg-white shadow-sm text-brand-600' : 'text-slate-500'}`}
            onClick={() => { setSource('PLACEMENT'); setCode(''); }}
          >
            Placement
          </button>
        </div>

        <div>
          {source === 'MANUAL' && (
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              placeholder="Enter code to generate..."
            />
          )}
          
          {source === 'PRODUCT' && (
            <SearchableSelect
              value={code}
              onChange={(val) => setCode(val)}
              placeholder={loadingProducts ? 'Loading products...' : 'Search product by name or SKU...'}
              disabled={loadingProducts}
              options={products.map(p => ({
                value: p.sku,
                label: p.display_name || p.name,
                subLabel: p.sku
              }))}
            />
          )}

          {source === 'PLACEMENT' && (
            <SearchableSelect
              value={code}
              onChange={(val) => setCode(val)}
              placeholder="Search placement by name or code..."
              options={placements.map(p => ({
                value: p.code || '',
                label: p.name,
                subLabel: p.code ? `Code: ${p.code}` : 'No Barcode Assigned',
                disabled: !p.code
              }))}
            />
          )}
        </div>
        
        <div className="flex gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="radio" checked={type === 'QR'} onChange={() => setType('QR')} className="text-brand-600 focus:ring-brand-500" />
            <span className="text-sm">QR Code</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="radio" checked={type === 'BARCODE'} onChange={() => setType('BARCODE')} className="text-brand-600 focus:ring-brand-500" />
            <span className="text-sm">Barcode (1D)</span>
          </label>
        </div>

        {code && (
          <div className="mt-6 border border-slate-200 rounded-lg p-6 bg-slate-50 flex flex-col items-center">
            
            {/* Visible Preview (Not printed directly with size, just visual) */}
            <div className="p-4 bg-white inline-block border border-slate-200 rounded">
              {type === 'QR' ? (
                <div className="flex flex-col items-center">
                  <QRCodeSVG value={code} size={120} level="M" />
                  <span className="mt-2 font-mono text-xs">{code}</span>
                </div>
              ) : (
                <Barcode value={code} width={1.5} height={50} fontSize={12} />
              )}
            </div>
            
            <Button variant="primary" className="mt-4 w-full" onClick={handlePrint}>
              <Printer size={16} className="mr-2" /> Print Now
            </Button>

            {/* Hidden Printable Area */}
            <div style={{ display: 'none' }}>
              <div ref={printRef}>
                <style type="text/css" media="print">
                  {`
                    @page { size: ${settings.width}mm ${settings.height}mm; margin: 0; }
                    html, body { margin: 0; padding: 0; width: ${settings.width}mm; height: ${settings.height}mm; }
                    .print-single {
                      width: ${settings.width}mm;
                      height: ${settings.height}mm;
                      padding: ${settings.margin}mm;
                      display: flex;
                      flex-direction: column;
                      align-items: center;
                      justify-content: center;
                      box-sizing: border-box;
                    }
                  `}
                </style>
                <div className="print-single">
                  {type === 'QR' ? (
                    <>
                      <QRCodeSVG value={code} size={Math.min(settings.width, settings.height) * 2.5} level="M" />
                      <div style={{ marginTop: '2mm', fontSize: '8pt', fontFamily: 'monospace', fontWeight: 'bold' }}>{code}</div>
                    </>
                  ) : (
                    <Barcode value={code} width={1} height={Math.max(10, settings.height * 1.5)} fontSize={10} margin={0} />
                  )}
                </div>
              </div>
            </div>

          </div>
        )}
      </div>
    </Modal>
  );
};

const BulkPrintModal = ({ isOpen, onClose, settings }) => {
  const { placements, loading } = usePlacements(false);
  const [selectedIds, setSelectedIds] = useState(new Set());
  const printRef = useRef(null);

  const handlePrint = useReactToPrint({
    contentRef: printRef,
  });

  const toggleSelection = (id) => {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  };

  const toggleAll = () => {
    if (selectedIds.size === placements.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(placements.map(p => p.id)));
    }
  };

  const selectedPlacements = placements.filter(p => selectedIds.has(p.id));

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Bulk Print Placements" size="lg">
      <div className="flex flex-col h-[60vh]">
        {loading ? (
          <div className="flex-1 flex justify-center items-center">Loading placements...</div>
        ) : (
          <>
            <div className="flex justify-between items-center mb-3">
              <span className="text-sm font-medium text-slate-600">{selectedIds.size} Selected</span>
              <button onClick={toggleAll} className="text-sm text-brand-600 hover:underline">
                {selectedIds.size === placements.length ? 'Deselect All' : 'Select All'}
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto border border-slate-200 rounded-lg bg-slate-50 p-2 space-y-1">
              {placements.map(p => (
                <div 
                  key={p.id} 
                  className={`flex items-center gap-3 p-3 rounded-md cursor-pointer transition-colors ${selectedIds.has(p.id) ? 'bg-brand-50 border-brand-200' : 'bg-white border-slate-200'} border`}
                  onClick={() => toggleSelection(p.id)}
                >
                  <div className="text-brand-600">
                    {selectedIds.has(p.id) ? <CheckSquare size={20} /> : <Square size={20} className="text-slate-300" />}
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-slate-800">{p.name}</p>
                    <p className="text-xs text-slate-500 font-mono">{p.code || 'NO CODE'}</p>
                  </div>
                  <div className="text-xs px-2 py-1 bg-slate-100 rounded-full text-slate-600">
                    {p.placement_type?.name}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 pt-4 border-t border-slate-200 flex justify-end gap-3">
              <Button variant="outline" onClick={onClose}>Cancel</Button>
              <Button variant="primary" disabled={selectedIds.size === 0} onClick={handlePrint}>
                <Printer size={16} className="mr-2" /> Print {selectedIds.size} Labels
              </Button>
            </div>

            {/* Hidden Printable Area */}
            <div style={{ display: 'none' }}>
              <div ref={printRef} className="print-container">
                <style type="text/css" media="print">
                  {`
                    @page { size: ${settings.width}mm ${settings.height}mm; margin: 0; }
                    html, body { margin: 0; padding: 0; }
                    .print-label { 
                      width: ${settings.width}mm;
                      height: ${settings.height}mm;
                      padding: ${settings.margin}mm;
                      page-break-after: always;
                      display: flex;
                      flex-direction: column;
                      align-items: center;
                      justify-content: center;
                      box-sizing: border-box;
                      overflow: hidden;
                    }
                  `}
                </style>
                {selectedPlacements.map(p => (
                  <div key={p.id} className="print-label">
                    {p.code ? (
                      <>
                        <QRCodeSVG value={p.code} size={Math.min(settings.width, settings.height) * 2} level="M" />
                        <div style={{ marginTop: '2mm', fontSize: '8pt', fontFamily: 'monospace', fontWeight: 'bold' }}>{p.code}</div>
                        <div style={{ fontSize: '6pt', textAlign: 'center', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '100%' }}>
                          {p.name}
                        </div>
                      </>
                    ) : (
                      <div style={{ fontSize: '10pt' }}>No Code</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </Modal>
  );
};

const BarcodeCenter = () => {
  const [singleModalOpen, setSingleModalOpen] = useState(false);
  const [bulkModalOpen, setBulkModalOpen] = useState(false);
  const [settingsModalOpen, setSettingsModalOpen] = useState(false);
  const [printerSettings, setPrinterSettings] = useState(getPrinterSettings());

  return (
    <div>
      <PageHeader 
        title="Products" 
        description="Manage product catalog, stock, and placements."
      />
      <ProductsTabs />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center text-center transition-all hover:shadow-md">
          <div className="w-12 h-12 bg-brand-50 text-brand-600 rounded-full flex items-center justify-center mb-4">
            <QrCode size={24} />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">Generate Single Barcode</h3>
          <p className="text-sm text-slate-500 mb-6">Create a barcode or QR code for a specific placement or product manually.</p>
          <Button variant="primary" className="w-full mt-auto" onClick={() => setSingleModalOpen(true)}>
            Open Generator
          </Button>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center text-center transition-all hover:shadow-md">
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-4">
            <FileText size={24} />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">Bulk Print Placements</h3>
          <p className="text-sm text-slate-500 mb-6">Select multiple locations/racks and generate a PDF with their barcode labels ready for printing.</p>
          <Button variant="outline" className="w-full mt-auto" onClick={() => setBulkModalOpen(true)}>
            Select Placements
          </Button>
        </div>
        
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center text-center transition-all hover:shadow-md">
          <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center mb-4">
            <Settings size={24} />
          </div>
          <h3 className="text-lg font-semibold text-slate-800 mb-2">Printer Settings</h3>
          <p className="text-sm text-slate-500 mb-6">Configure label dimensions (e.g. 50x30mm) for thermal printers.</p>
          <div className="mt-auto w-full">
            <div className="text-xs text-slate-400 mb-2">Current: {printerSettings.width}x{printerSettings.height}mm</div>
            <Button variant="outline" className="w-full" onClick={() => setSettingsModalOpen(true)}>
              Configure Settings
            </Button>
          </div>
        </div>

      </div>

      <SingleGeneratorModal 
        isOpen={singleModalOpen} 
        onClose={() => setSingleModalOpen(false)} 
        settings={printerSettings}
      />
      <BulkPrintModal 
        isOpen={bulkModalOpen} 
        onClose={() => setBulkModalOpen(false)} 
        settings={printerSettings}
      />
      <PrinterSettingsModal 
        isOpen={settingsModalOpen} 
        onClose={() => setSettingsModalOpen(false)} 
        onSave={setPrinterSettings}
      />
    </div>
  );
};

export default BarcodeCenter;
