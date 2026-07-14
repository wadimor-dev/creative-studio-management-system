import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Button from '../../../components/common/Button';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import { useProducts } from '../../../hooks/useProducts';
import { useLocations } from '../../../hooks/useLocations';

const MovementForm = ({ onSubmit, onCancel }) => {
  const { data: productsData, loading: loadingProducts } = useProducts();
  const { locations, loading: loadingLocations } = useLocations();

  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    defaultValues: {
      type: 'IN',
      product_id: '',
      quantity: 1,
      source_location_id: '',
      destination_location_id: '',
      reference: '',
      notes: ''
    }
  });

  const type = watch('type');
  const isLoading = loadingProducts || loadingLocations;

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <LoadingSpinner size="md" text="Loading data..." />
      </div>
    );
  }

  const handleFormSubmit = (data) => {
    const payload = {
      ...data,
      product_id: parseInt(data.product_id),
      quantity: parseInt(data.quantity),
      source_location_id: data.source_location_id ? parseInt(data.source_location_id) : null,
      destination_location_id: data.destination_location_id ? parseInt(data.destination_location_id) : null,
    };
    onSubmit(payload);
  };

  // Check if products is paginated response or array
  const productArray = Array.isArray(productsData) ? productsData : (productsData?.data || []);
  const locationArray = Array.isArray(locations) ? locations : (locations?.data || []);

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 mt-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="sm:col-span-2">
          <label className="block text-sm font-medium text-slate-700 mb-1">Movement Type *</label>
          <div className="flex gap-4">
            {['IN', 'OUT', 'TRANSFER'].map(t => (
              <label key={t} className="flex items-center gap-2 cursor-pointer">
                <input 
                  type="radio" 
                  value={t} 
                  {...register('type')} 
                  className="text-brand-600 focus:ring-brand-500" 
                />
                <span className="text-sm text-slate-700 font-medium">{t}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="sm:col-span-2">
          <label className="block text-sm font-medium text-slate-700 mb-1">Product *</label>
          <select 
            className={`w-full rounded-lg border ${errors.product_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
            {...register('product_id', { required: 'Product is required' })}
          >
            <option value="">Select Product...</option>
            {productArray.map(p => <option key={p.id} value={p.id}>{p.sku} - {p.display_name}</option>)}
          </select>
          {errors.product_id && <p className="mt-1 text-xs text-rose-500">{errors.product_id.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Quantity *</label>
          <Input 
            type="number"
            min="1"
            {...register('quantity', { required: 'Quantity is required', min: 1 })}
          />
          {errors.quantity && <p className="mt-1 text-xs text-rose-500">{errors.quantity.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Reference / PO Number</label>
          <Input {...register('reference')} placeholder="Optional..." />
        </div>

        {(type === 'OUT' || type === 'TRANSFER') && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Source Location *</label>
            <select 
              className={`w-full rounded-lg border ${errors.source_location_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
              {...register('source_location_id', { required: (type === 'OUT' || type === 'TRANSFER') ? 'Source is required' : false })}
            >
              <option value="">Select Source...</option>
              {locationArray.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
            </select>
            {errors.source_location_id && <p className="mt-1 text-xs text-rose-500">{errors.source_location_id.message}</p>}
          </div>
        )}

        {(type === 'IN' || type === 'TRANSFER') && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Destination Location *</label>
            <select 
              className={`w-full rounded-lg border ${errors.destination_location_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
              {...register('destination_location_id', { required: (type === 'IN' || type === 'TRANSFER') ? 'Destination is required' : false })}
            >
              <option value="">Select Destination...</option>
              {locationArray.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
            </select>
            {errors.destination_location_id && <p className="mt-1 text-xs text-rose-500">{errors.destination_location_id.message}</p>}
          </div>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Notes</label>
        <textarea 
          {...register('notes')} 
          rows="2"
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          placeholder="Optional notes..."
        ></textarea>
      </div>

      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">Record Movement</Button>
      </div>
    </form>
  );
};

export default MovementForm;
