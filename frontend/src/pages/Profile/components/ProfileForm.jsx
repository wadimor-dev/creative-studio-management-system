import React from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Button from '../../../components/common/Button';

const ProfileForm = ({ user, onSubmit }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      name: user?.name || '',
      email: user?.email || '',
    }
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
        <Input 
          {...register('name', { required: 'Name is required' })} 
          error={!!errors.name} 
        />
        {errors.name && <p className="mt-1 text-xs text-rose-500">{errors.name.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
        <Input 
          type="email"
          {...register('email', { 
            required: 'Email is required',
            pattern: { value: /^\S+@\S+$/i, message: 'Invalid email address' }
          })} 
          error={!!errors.email} 
        />
        {errors.email && <p className="mt-1 text-xs text-rose-500">{errors.email.message}</p>}
      </div>
      
      <div className="pt-2">
        <Button type="submit" variant="primary">Save Changes</Button>
      </div>
    </form>
  );
};

export default ProfileForm;
