import React from 'react';
import StatWidget from '../../Dashboard/components/StatWidget';
import { Users, UserCheck, UserMinus } from 'lucide-react';

const UserStats = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 mb-6">
      <StatWidget 
        title="Total Users" 
        value={stats.total} 
        icon={Users} 
        color="brand"
      />
      <StatWidget 
        title="Active" 
        value={stats.active} 
        icon={UserCheck} 
        color="emerald"
      />
      <StatWidget 
        title="Inactive" 
        value={stats.inactive} 
        icon={UserMinus} 
        color="slate"
      />
    </div>
  );
};

export default UserStats;
