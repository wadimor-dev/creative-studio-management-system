import React, { forwardRef } from 'react';

const Card = forwardRef(({ className = '', ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={`rounded-xl border border-slate-200 bg-white shadow-sm ${className}`}
      {...props}
    />
  );
});

Card.displayName = 'Card';
export default Card;
