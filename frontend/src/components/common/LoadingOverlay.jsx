import React from 'react';
import LoadingSpinner from './LoadingSpinner';

const LoadingOverlay = ({ message = 'Loading...' }) => {
  return (
    <div className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm">
      <LoadingSpinner size="lg" />
      {message && <p className="mt-4 text-sm font-medium text-slate-600">{message}</p>}
    </div>
  );
};

export default LoadingOverlay;
