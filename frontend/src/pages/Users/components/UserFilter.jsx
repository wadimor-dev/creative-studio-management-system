import React from 'react';
import SearchInput from '../../../components/common/SearchInput';
import Select from '../../../components/common/Select';
import Button from '../../../components/common/Button';
import { FilterX } from 'lucide-react';

const UserFilter = () => {
  return (
    <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-12">
      <div className="sm:col-span-5">
        <SearchInput placeholder="Search name or email..." />
      </div>
      <div className="sm:col-span-3">
        <Select defaultValue="">
          <option value="" disabled>Role</option>
          <option value="ALL">All Roles</option>
          <option value="ADMIN">Admin</option>
          <option value="MANAGER">Manager</option>
          <option value="STAFF">Staff</option>
        </Select>
      </div>
      <div className="sm:col-span-3">
        <Select defaultValue="">
          <option value="" disabled>Status</option>
          <option value="ALL">All Status</option>
          <option value="ACTIVE">Active</option>
          <option value="INACTIVE">Inactive</option>
        </Select>
      </div>
      <div className="sm:col-span-1">
        <Button variant="secondary" className="w-full" title="Reset Filters">
          <FilterX size={16} />
        </Button>
      </div>
    </div>
  );
};

export default UserFilter;
