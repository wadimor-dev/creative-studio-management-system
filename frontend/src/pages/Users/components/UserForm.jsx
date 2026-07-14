import React from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Button from '../../../components/common/Button';

const UserForm = ({ initialData, onSubmit, onCancel }) => {
  const isEditing = !!initialData;
  const defaultValues = initialData ? {
    name: initialData.full_name || initialData.username || '',
    email: initialData.email || '',
    password: '',
    role: initialData.role?.name?.toUpperCase() || 'STAFF',
    status: initialData.is_active ? 'ACTIVE' : 'INACTIVE'
  } : {
    name: '',
    email: '',
    password: '',
    role: 'STAFF',
    status: 'ACTIVE'
  };

  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Name *</label>
        <Input 
          {...register('name', { required: 'Name is required' })} 
          error={!!errors.name} 
          placeholder="e.g. John Doe"
        />
        {errors.name && <p className="mt-1 text-xs text-rose-500">{errors.name.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Email *</label>
        <Input 
          type="email"
          {...register('email', { 
            required: 'Email is required',
            pattern: { value: /^\S+@\S+$/i, message: 'Invalid email address' }
          })} 
          error={!!errors.email} 
          placeholder="e.g. john@creativestudio.com"
        />
        {errors.email && <p className="mt-1 text-xs text-rose-500">{errors.email.message}</p>}
      </div>

      {/* Password field only shown during Add User */}
      {!isEditing && (
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Password *</label>
          <Input 
            type="password"
            {...register('password', { required: 'Password is required for new users', minLength: { value: 6, message: 'Minimum 6 characters' } })} 
            error={!!errors.password} 
          />
          {errors.password && <p className="mt-1 text-xs text-rose-500">{errors.password.message}</p>}
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Role *</label>
          <Select {...register('role', { required: 'Role is required' })}>
            <option value="Admin">Admin</option>
            <option value="Manager">Manager</option>
            <option value="Staff">Staff</option>
            <option value="Creative">Creative</option>
          </Select>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Status *</label>
          <Select {...register('status', { required: 'Status is required' })}>
            <option value="1">Active</option>
            <option value="0">Inactive</option>
          </Select>
        </div>
      </div>
      
      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">{isEditing ? 'Save Changes' : 'Create User'}</Button>
      </div>
    </form>
  );
};

export default UserForm;
