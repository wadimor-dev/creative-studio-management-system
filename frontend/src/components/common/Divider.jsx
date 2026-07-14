import React from 'react';

const Divider = ({ className = '' }) => {
  return <div className={`h-px w-full bg-slate-200 my-6 ${className}`} />;
};

export default Divider;
