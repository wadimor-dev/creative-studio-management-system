import React from 'react';
import Badge from './Badge';

const RoleBadge = ({ role, className = '' }) => {
  const getRoleConfig = (roleType) => {
    switch (roleType?.toUpperCase()) {
      case 'ADMIN':
        return { variant: 'danger', label: 'Admin' };
      case 'MANAGER':
        return { variant: 'info', label: 'Manager' };
      case 'STAFF':
        return { variant: 'success', label: 'Staff' };
      default:
        return { variant: 'default', label: roleType || 'Unknown' };
    }
  };

  const config = getRoleConfig(role);

  return (
    <Badge variant={config.variant} className={className}>
      {config.label}
    </Badge>
  );
};

export default RoleBadge;
