import React from 'react';

const Avatar = ({ src, alt, name, size = 'md', className = '' }) => {
  const sizes = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-16 w-16 text-lg',
    xl: 'h-24 w-24 text-2xl',
  };

  const getInitials = (fullName) => {
    if (!fullName) return 'U';
    const parts = fullName.trim().split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    }
    return fullName.substring(0, 2).toUpperCase();
  };

  const baseStyles = 'inline-flex items-center justify-center rounded-full flex-shrink-0 overflow-hidden';
  const colorStyles = 'bg-brand-100 text-brand-700 font-medium border border-brand-200';

  if (src) {
    return (
      <img
        src={src}
        alt={alt || name || 'User Avatar'}
        className={`${baseStyles} ${sizes[size]} object-cover ${className}`}
      />
    );
  }

  return (
    <div className={`${baseStyles} ${sizes[size]} ${colorStyles} ${className}`}>
      {getInitials(name)}
    </div>
  );
};

export default Avatar;
