import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../../components/common/PageHeader';
import { scannerService } from '../../api/services/scannerService';
import { toastError } from '../../utils/toast';
import { ScanLine, Camera } from 'lucide-react';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';

const ScannerHome = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [manualCode, setManualCode] = useState('');
  
  // Barcode scanner listener logic
  const barcodeBuffer = useRef('');
  const lastKeyTime = useRef(Date.now());

  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ignore if typing in an input field (unless it's our manual fallback)
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        if (e.target.id !== 'manual-scan-input') return;
      }

      const currentTime = Date.now();
      
      // If time between keystrokes is > 50ms, it's probably human typing, reset buffer
      if (currentTime - lastKeyTime.current > 50) {
        barcodeBuffer.current = '';
      }
      
      if (e.key === 'Enter') {
        if (barcodeBuffer.current.length > 2) {
          e.preventDefault();
          handleScan(barcodeBuffer.current);
        }
        barcodeBuffer.current = '';
      } else if (e.key.length === 1) { // Only capture single characters
        barcodeBuffer.current += e.key;
      }
      
      lastKeyTime.current = currentTime;
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleScan = async (code) => {
    if (!code) return;
    setLoading(true);
    try {
      const res = await scannerService.resolveLocation(code);
      if (res.success && res.data) {
        // Redirect to Location View
        navigate(`/scanner/location/${res.data.id}`);
      } else {
        toastError(res.message || "Location not found");
      }
    } catch (err) {
      toastError(err.response?.data?.message || "Invalid Barcode or Location not found");
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    handleScan(manualCode);
  };

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 text-center">
        <div className="w-20 h-20 bg-brand-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <ScanLine className="text-brand-600" size={40} />
        </div>
        
        <h2 className="text-2xl font-bold text-slate-800 mb-2">Location Scanner Mode</h2>
        <p className="text-slate-500 mb-8">
          Please scan a Rack or Showroom barcode to begin operations.
        </p>

        {loading ? (
          <div className="animate-pulse text-brand-600 font-medium">Resolving location...</div>
        ) : (
          <div className="space-y-6">
            <div className="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p className="text-sm text-slate-600 font-medium flex items-center justify-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                Scanner is active and ready
              </p>
            </div>
            
            <div className="relative flex items-center py-2">
              <div className="flex-grow border-t border-slate-200"></div>
              <span className="flex-shrink-0 mx-4 text-slate-400 text-sm">or</span>
              <div className="flex-grow border-t border-slate-200"></div>
            </div>

            <form onSubmit={handleManualSubmit} className="flex gap-2 max-w-sm mx-auto">
              <Input 
                id="manual-scan-input"
                placeholder="Enter Code (e.g. LOC-001)" 
                value={manualCode}
                onChange={(e) => setManualCode(e.target.value)}
              />
              <Button type="submit" variant="primary">Go</Button>
            </form>

            <Button variant="secondary" className="w-full max-w-sm mx-auto gap-2" onClick={() => alert('Camera integration will be opened here')}>
              <Camera size={18} />
              Scan via Camera (Mobile)
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScannerHome;
