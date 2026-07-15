import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Menu, ArrowLeft } from 'lucide-react';

const ScannerLayout = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-screen h-screen bg-slate-900 text-slate-50 overflow-hidden w-full m-0 p-0 fixed inset-0">
      {/* Mini header just for Back/Menu */}
      <div className="flex items-center justify-between p-4 bg-slate-900 border-b border-slate-800 shrink-0">
        <button 
          onClick={() => navigate(-1)} 
          className="p-2 -ml-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-full transition-colors"
        >
          <ArrowLeft size={24} />
        </button>
        <span className="font-semibold text-slate-300">Scanner Mode</span>
        <button 
          onClick={() => navigate('/dashboard')} 
          className="p-2 -mr-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-full transition-colors"
        >
          <Menu size={24} />
        </button>
      </div>

      {/* Main Scanner Area - Takes up remaining space */}
      <div className="flex-1 overflow-y-auto relative w-full flex flex-col items-center">
        <div className="w-full max-w-lg min-h-full flex flex-col p-4">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default ScannerLayout;
