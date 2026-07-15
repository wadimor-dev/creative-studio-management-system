import React from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Textarea from '../../../components/common/Textarea';
import Button from '../../../components/common/Button';

const LocationForm = ({ initialData, onSubmit, onCancel }) => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: initialData || {
      name: '',
      description: ''
    }
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Location Name *</label>
        <Input 
          {...register('name', { required: 'Location name is required' })} 
          error={!!errors.name} 
          placeholder="e.g. Studio A, Warehouse 1"
        />
        {errors.name && <p className="mt-1 text-xs text-rose-500">{errors.name.message}</p>}
      </div>
      
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
        <Textarea 
          {...register('description')} 
          rows={3} 
          placeholder="Optional description..." 
        />
      </div>
      
      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">Save Location</Button>
      </div>
    </form>
  );
};

export default LocationForm;
