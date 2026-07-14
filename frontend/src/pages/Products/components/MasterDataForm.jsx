import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Textarea from '../../../components/common/Textarea';
import Button from '../../../components/common/Button';

const MasterDataForm = ({ initialData, onSubmit, onCancel, entityTitle, entityId }) => {
  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: initialData || {
      name: '',
      code: '',
      description: ''
    }
  });

  useEffect(() => {
    reset(initialData || { name: '', code: '', description: '' });
  }, [initialData, reset]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
      <div className={`grid grid-cols-1 ${entityId !== 'locations' ? 'sm:grid-cols-2' : ''} gap-4`}>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">{entityTitle} Name *</label>
          <Input 
            {...register('name', { required: 'Name is required' })} 
            error={!!errors.name} 
            placeholder={`e.g. ${entityTitle === 'Color' ? 'Merah' : entityTitle === 'Type' ? 'Sarung' : 'Value'}`}
          />
          {errors.name && <p className="mt-1 text-xs text-rose-500">{errors.name.message}</p>}
        </div>
        {entityId !== 'locations' && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Code *</label>
            <Input 
              {...register('code', { required: 'Code is required' })} 
              error={!!errors.code} 
              placeholder="e.g. MRH, SRG"
            />
            {errors.code && <p className="mt-1 text-xs text-rose-500">{errors.code.message}</p>}
          </div>
        )}
      </div>
      
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
        <Textarea 
          {...register('description')} 
          rows={2} 
          placeholder="Optional description..." 
        />
      </div>
      
      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">Save {entityTitle}</Button>
      </div>
    </form>
  );
};

export default MasterDataForm;
