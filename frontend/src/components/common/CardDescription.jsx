import React, { forwardRef } from 'react';

const CardDescription = forwardRef(({ className = '', ...props }, ref) => {
  return (
    <p
      ref={ref}
      className={`text-sm text-slate-500 ${className}`}
      {...props}
    />
  );
});

CardDescription.displayName = 'CardDescription';
export default CardDescription;
