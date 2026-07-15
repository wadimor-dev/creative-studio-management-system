import React, { useEffect, useRef, useState } from 'react';
import { Html5Qrcode } from 'html5-qrcode';
import { Camera, RefreshCw, AlertCircle } from 'lucide-react';
import Button from './Button';

const Html5QrcodePlugin = ({ fps = 10, qrbox = 250, qrCodeSuccessCallback, qrCodeErrorCallback }) => {
  const [hasPermission, setHasPermission] = useState(false);
  const [cameras, setCameras] = useState([]);
  const [activeCameraId, setActiveCameraId] = useState(null);
  const [error, setError] = useState(null);
  
  const html5QrCodeRef = useRef(null);
  const scannerId = "qr-reader-custom";

  useEffect(() => {
    // Initialize scanner instance
    html5QrCodeRef.current = new Html5Qrcode(scannerId);
    
    // Check permissions and get cameras on mount
    Html5Qrcode.getCameras().then(devices => {
      if (devices && devices.length) {
        setHasPermission(true);
        setCameras(devices);
        
        // Try to find a back camera
        const backCamera = devices.find(d => d.label.toLowerCase().includes('back') || d.label.toLowerCase().includes('rear'));
        const defaultCameraId = backCamera ? backCamera.id : devices[0].id;
        setActiveCameraId(defaultCameraId);
      } else {
        setError("No cameras found on your device.");
      }
    }).catch(err => {
      // Permission denied or not supported
      setHasPermission(false);
    });

    return () => {
      stopScanning();
    };
  }, []);

  // Start scanning when camera is selected and we have permission
  useEffect(() => {
    if (hasPermission && activeCameraId) {
      startScanning(activeCameraId);
    }
  }, [hasPermission, activeCameraId]);

  const startScanning = (cameraId) => {
    if (!html5QrCodeRef.current) return;

    const config = {
      fps,
      qrbox: { width: 250, height: 250 },
      aspectRatio: 1.0, // Force square/responsive ratio
    };

    // If scanner is currently running, stop it first
    if (html5QrCodeRef.current.isScanning) {
      html5QrCodeRef.current.stop().then(() => {
        startActual(cameraId, config);
      }).catch(err => console.error("Error stopping scanner", err));
    } else {
      startActual(cameraId, config);
    }
  };

  const startActual = (cameraId, config) => {
    html5QrCodeRef.current.start(
      cameraId, 
      config, 
      (decodedText, decodedResult) => {
        if (qrCodeSuccessCallback) qrCodeSuccessCallback(decodedText, decodedResult);
      },
      (errorMessage) => {
        if (qrCodeErrorCallback) qrCodeErrorCallback(errorMessage);
      }
    ).catch(err => {
      setError("Failed to start camera. Please ensure permissions are granted.");
      console.error(err);
    });
  };

  const stopScanning = () => {
    if (html5QrCodeRef.current && html5QrCodeRef.current.isScanning) {
      html5QrCodeRef.current.stop().catch(err => console.error("Failed to stop", err));
    }
  };

  const requestPermission = () => {
    Html5Qrcode.getCameras().then(devices => {
      if (devices && devices.length) {
        setHasPermission(true);
        setCameras(devices);
        const backCamera = devices.find(d => d.label.toLowerCase().includes('back') || d.label.toLowerCase().includes('rear'));
        setActiveCameraId(backCamera ? backCamera.id : devices[0].id);
        setError(null);
      }
    }).catch(err => {
      setError("Camera permission denied. Please allow camera access in your browser settings.");
    });
  };

  const switchCamera = () => {
    if (cameras.length > 1) {
      const currentIndex = cameras.findIndex(c => c.id === activeCameraId);
      const nextIndex = (currentIndex + 1) % cameras.length;
      setActiveCameraId(cameras[nextIndex].id);
    }
  };

  return (
    <div className="w-full flex flex-col relative bg-slate-900 rounded-xl overflow-hidden aspect-square md:aspect-video">
      
      {!hasPermission && !error && (
        <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-10 bg-slate-900">
          <Camera size={48} className="text-slate-500 mb-4" />
          <h3 className="text-white font-semibold mb-2">Camera Access Required</h3>
          <p className="text-slate-400 text-sm mb-6">We need access to your camera to scan barcodes and QR codes.</p>
          <Button variant="primary" onClick={requestPermission}>Grant Permission</Button>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-10 bg-slate-900">
          <AlertCircle size={48} className="text-rose-500 mb-4" />
          <h3 className="text-white font-semibold mb-2">Camera Error</h3>
          <p className="text-slate-400 text-sm">{error}</p>
          <Button variant="outline" className="mt-4" onClick={requestPermission}>Try Again</Button>
        </div>
      )}

      {/* The actual reader element. Html5Qrcode injects <video> inside this */}
      <div id={scannerId} className="w-full h-full object-cover" />

      {/* Custom UI Overlays */}
      {hasPermission && !error && cameras.length > 1 && (
        <div className="absolute bottom-4 left-0 right-0 flex justify-center z-10">
          <button 
            onClick={switchCamera}
            className="flex items-center gap-2 bg-slate-800/80 hover:bg-slate-700 backdrop-blur text-white px-4 py-2 rounded-full shadow-lg border border-slate-600 transition-all text-sm font-medium"
          >
            <RefreshCw size={16} />
            Switch Camera
          </button>
        </div>
      )}
    </div>
  );
};

export default Html5QrcodePlugin;
