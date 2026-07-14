import React, { forwardRef } from 'react';

const CardContent = forwardRef(({ className = '', ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={`p-6 pt-0 ${className}`}
      {...props}
    />
  );
});

CardContent.displayName = 'CardContent';
export default CardContent;
