import React, { forwardRef } from 'react';

const CardTitle = forwardRef(({ className = '', ...props }, ref) => {
  return (
    <h3
      ref={ref}
      className={`font-semibold leading-none tracking-tight text-slate-900 ${className}`}
      {...props}
    />
  );
});

CardTitle.displayName = 'CardTitle';
export default CardTitle;
