import React from 'react';

const StatusBadge = ({ label, className }) => (
  <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${className || 'bg-slate-100 text-slate-600'}`}>
    {label}
  </span>
);

export default StatusBadge;
