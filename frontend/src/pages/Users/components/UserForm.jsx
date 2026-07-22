import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Button from '../../../components/common/Button';
import apiClient from '../../../api/axios';
import { toastError } from '../../../utils/toast';

const UserForm = ({ initialData, onSubmit, onCancel }) => {
  const isEditing = !!initialData;
  const [roles, setRoles] = useState([]);
  const [loadingRoles, setLoadingRoles] = useState(true);

  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const res = await apiClient.get('/admin/roles');
        const roleList = res?.data || [];
        setRoles(roleList);
      } catch (err) {
        toastError('Failed to load roles');
        setRoles([]);
      } finally {
        setLoadingRoles(false);
      }
    };
    fetchRoles();
  }, []);

  const currentRoleIds = initialData?.roles
    ? initialData.roles.map(r => r.id)
    : [];

  const defaultValues = initialData
    ? {
        name: initialData.full_name || initialData.username || '',
        email: initialData.email || '',
        password: '',
        role_ids: currentRoleIds,
        status: initialData.is_active !== false ? '1' : '0',
      }
    : {
        name: '',
        email: '',
        password: '',
        role_ids: [],
        status: '1',
      };

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm({ defaultValues });

  const selectedRoleIds = watch('role_ids', []);

  const toggleRole = (roleId) => {
    const current = selectedRoleIds || [];
    if (current.includes(roleId)) {
      setValue('role_ids', current.filter(id => id !== roleId), { shouldValidate: true });
    } else {
      setValue('role_ids', [...current, roleId], { shouldValidate: true });
    }
  };

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
            pattern: { value: /^\S+@\S+$/i, message: 'Invalid email address' },
          })}
          error={!!errors.email}
          placeholder="e.g. john@creativestudio.com"
        />
        {errors.email && <p className="mt-1 text-xs text-rose-500">{errors.email.message}</p>}
      </div>

      {!isEditing && (
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Password *</label>
          <Input
            type="password"
            {...register('password', {
              required: 'Password is required for new users',
              minLength: { value: 6, message: 'Minimum 6 characters' },
            })}
            error={!!errors.password}
          />
          {errors.password && <p className="mt-1 text-xs text-rose-500">{errors.password.message}</p>}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Roles *</label>
        {loadingRoles ? (
          <p className="text-sm text-slate-400">Loading roles...</p>
        ) : roles.length === 0 ? (
          <p className="text-sm text-amber-600">No roles available</p>
        ) : (
          <div className="space-y-2 border border-slate-200 rounded-lg p-3">
            {roles.map(role => (
              <label key={role.id} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={(selectedRoleIds || []).includes(role.id)}
                  onChange={() => toggleRole(role.id)}
                  className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-slate-700">{role.name}</span>
                {role.description && (
                  <span className="text-xs text-slate-400">- {role.description}</span>
                )}
              </label>
            ))}
          </div>
        )}
        {selectedRoleIds && selectedRoleIds.length === 0 && (
          <p className="mt-1 text-xs text-rose-500">Select at least one role</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Status *</label>
        <select
          {...register('status', { required: 'Status is required' })}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
        >
          <option value="1">Active</option>
          <option value="0">Inactive</option>
        </select>
      </div>

      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">
          {isEditing ? 'Save Changes' : 'Create User'}
        </Button>
      </div>
    </form>
  );
};

export default UserForm;
