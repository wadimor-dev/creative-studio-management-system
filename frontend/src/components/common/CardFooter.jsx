import React, { forwardRef } from 'react';

const CardFooter = forwardRef(({ className = '', ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={`flex items-center p-6 pt-0 ${className}`}
      {...props}
    />
  );
});

CardFooter.displayName = 'CardFooter';
export default CardFooter;
