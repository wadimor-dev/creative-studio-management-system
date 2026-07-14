import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { categoryService } from '../../../api/services/categoryService';
import apiClient from '../../../api/axios'; // Or import specific services
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import Button from '../../../components/common/Button';
import { ENDPOINTS } from '../../../api/endpoints';

const ItemForm = ({ initialData, onSubmit, onCancel }) => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm({
    defaultValues: initialData || {
      code: '',
      name: '',
      category: '',
      quantity: 1,
      unit: '',
      location: '',
      status: 'READY',
      description: ''
    }
  });

  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  
  const isEditing = !!initialData?.id;

  useEffect(() => {
    // Fetch categories and locations, then reset form so that selects get the correct values
    Promise.all([
      categoryService.getAll(),
      apiClient.get(ENDPOINTS.LOCATIONS)
    ]).then(([catRes, locRes]) => {
      if(catRes.success) setCategories(catRes.data);
      if(locRes.success) setLocations(locRes.data);
      
      // Reset form after options are populated to ensure Selects bind correctly
      reset(initialData || {
        code: '',
        name: '',
        category: '',
        quantity: 1,
        unit: 'pcs',
        location: '',
        status: 'READY',
        description: ''
      });
    }).catch(console.error);
  }, [initialData, reset]);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Code/SKU *</label>
          <Input 
            {...register('code', { required: 'Code is required' })} 
            error={!!errors.code} 
            placeholder="e.g. CAM-001"
          />
          {errors.code && <p className="mt-1 text-xs text-rose-500">{errors.code.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Name *</label>
          <Input 
            {...register('name', { required: 'Name is required' })} 
            error={!!errors.name} 
            placeholder="e.g. Sony A7III"
          />
          {errors.name && <p className="mt-1 text-xs text-rose-500">{errors.name.message}</p>}
        </div>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Category *</label>
          <Select {...register('category', { required: 'Category is required' })} error={!!errors.category}>
            <option value="">Select Category</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </Select>
          {errors.category && <p className="mt-1 text-xs text-rose-500">{errors.category.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Status</label>
          <Select {...register('status')}>
            <option value="READY">READY</option>
            <option value="IN_USE">IN USE</option>
            <option value="MAINTENANCE">MAINTENANCE</option>
          </Select>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Unit</label>
          <Select {...register('unit')}>
            <option value="pcs">pcs</option>
            <option value="set">set</option>
            <option value="box">box</option>
            <option value="roll">roll</option>
          </Select>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Location *</label>
          <Select {...register('location', { required: 'Location is required' })} error={!!errors.location}>
            <option value="">Select Location</option>
            {locations.map(l => (
              <option key={l.id} value={l.id}>{l.name}</option>
            ))}
          </Select>
          {errors.location && <p className="mt-1 text-xs text-rose-500">{errors.location.message}</p>}
        </div>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-4 rounded-lg border border-slate-100">
        <div className="col-span-2">
          <h4 className="text-sm font-semibold text-slate-800">{isEditing ? 'Current Stock' : 'Initial Stock (Optional)'}</h4>
          <p className="text-xs text-slate-500">{isEditing ? 'You can adjust the total quantity here. This will generate an adjustment transaction automatically.' : 'You can set the starting quantity for this new item.'}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Quantity</label>
          <Input 
            type="number" 
            min="0"
            {...register('quantity', { valueAsNumber: true })} 
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
        <Textarea {...register('description')} rows={3} placeholder="Optional item details..." />
      </div>
      
      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">{isEditing ? 'Update Item' : 'Save Item'}</Button>
      </div>
    </form>
  );
};

export default ItemForm;
