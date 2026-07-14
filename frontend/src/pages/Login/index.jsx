import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { Mail } from 'lucide-react';
import FormField from '../../components/forms/FormField';
import Input from '../../components/common/Input';
import PasswordInput from '../../components/common/PasswordInput';
import Button from '../../components/common/Button';
import { useAuth } from '../../contexts/AuthContext';

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false
    }
  });

  const onSubmit = async (data) => {
    setIsSubmitting(true);
    const res = await login(data);
    setIsSubmitting(false);
    
    if (res.success) {
      toast.success('Successfully logged in!');
      navigate('/dashboard');
    } else {
      toast.error(res.message || 'Login failed. Please check your credentials.');
    }
  };

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Welcome to</h1>
        <p className="text-sm text-slate-500 mt-2">Creative Division Management System</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        <FormField label="Email address" error={errors.email?.message}>
          <Input 
            {...register('email', { 
              required: 'Email is required',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Invalid email address'
              }
            })}
            type="email" 
            placeholder="admin@studio.com"
            icon={Mail}
            error={!!errors.email}
          />
        </FormField>

        <FormField label="Password" error={errors.password?.message}>
          <PasswordInput 
            {...register('password', { 
              required: 'Password is required',
              minLength: {
                value: 6,
                message: 'Password must be at least 6 characters'
              }
            })}
            placeholder="••••••••"
            error={!!errors.password}
          />
        </FormField>

        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              {...register('rememberMe')}
              id="rememberMe"
              type="checkbox"
              className="h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-600"
            />
            <label htmlFor="rememberMe" className="ml-2 block text-sm text-slate-700">
              Remember me
            </label>
          </div>
          <div className="text-sm">
            <a href="#" className="font-semibold text-brand-600 hover:text-brand-500" onClick={(e) => { e.preventDefault(); toast.info("Reset password flow not implemented yet"); }}>
              Forgot password?
            </a>
          </div>
        </div>

        <div>
          <Button
            type="submit"
            isFullWidth
            isLoading={isSubmitting}
          >
            Sign in to account
          </Button>
        </div>
      </form>
    </div>
  );
};

export default Login;
