import React from 'react';
import { Outlet } from 'react-router-dom';
import logoUrl from '../assets/logo/logo.webp';

const AuthLayout = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 relative overflow-hidden">
      {/* Decorative background elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-brand-400/20 blur-3xl"></div>
        <div className="absolute bottom-[-10%] right-[-5%] w-[50%] h-[50%] rounded-full bg-indigo-400/10 blur-3xl"></div>
      </div>
      
      <div className="z-10 w-full max-w-md p-1">
        <div className="flex justify-center mb-6">
          <div className="flex items-center gap-2 font-bold text-3xl text-slate-800 tracking-tight">
            <div className="flex h-30 w-30 items-center justify-center text-white overflow-hidden">
              <img src={logoUrl} alt="Logo" className="h-full w-full object-cover" />
            </div>
          </div>
        </div>
        
        <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-xl shadow-slate-200/50 border border-white/50 p-8">
          <Outlet />
        </div>
        
        <p className="text-center text-sm text-slate-500 mt-8">
          &copy; {new Date().getFullYear()} Wadimor Creative Division.
        </p>
      </div>
    </div>
  );
};

export default AuthLayout;
