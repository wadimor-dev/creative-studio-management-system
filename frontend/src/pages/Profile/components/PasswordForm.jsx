import React from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Button from '../../../components/common/Button';

const PasswordForm = ({ onSubmit }) => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  });

  const newPassword = watch('newPassword');

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Current Password</label>
        <Input 
          type="password"
          {...register('currentPassword', { required: 'Current password is required' })} 
          error={!!errors.currentPassword} 
        />
        {errors.currentPassword && <p className="mt-1 text-xs text-rose-500">{errors.currentPassword.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">New Password</label>
        <Input 
          type="password"
          {...register('newPassword', { 
            required: 'New password is required',
            minLength: { value: 6, message: 'Minimum 6 characters required' }
          })} 
          error={!!errors.newPassword} 
        />
        {errors.newPassword && <p className="mt-1 text-xs text-rose-500">{errors.newPassword.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Confirm New Password</label>
        <Input 
          type="password"
          {...register('confirmPassword', { 
            required: 'Please confirm your new password',
            validate: value => value === newPassword || 'Passwords do not match'
          })} 
          error={!!errors.confirmPassword} 
        />
        {errors.confirmPassword && <p className="mt-1 text-xs text-rose-500">{errors.confirmPassword.message}</p>}
      </div>
      
      <div className="pt-2">
        <Button type="submit" variant="primary">Update Password</Button>
      </div>
    </form>
  );
};

export default PasswordForm;
