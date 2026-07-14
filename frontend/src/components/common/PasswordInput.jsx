import React, { forwardRef, useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import Input from './Input';

const PasswordInput = forwardRef(({ ...props }, ref) => {
  const [showPassword, setShowPassword] = useState(false);

  const toggleVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <div className="relative">
      <Input
        ref={ref}
        type={showPassword ? 'text' : 'password'}
        {...props}
      />
      <button
        type="button"
        className="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600 focus:outline-none"
        onClick={toggleVisibility}
        tabIndex={-1}
      >
        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
      </button>
    </div>
  );
});

PasswordInput.displayName = 'PasswordInput';
export default PasswordInput;
