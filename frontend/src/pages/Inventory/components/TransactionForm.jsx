import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import Button from '../../../components/common/Button';

const TransactionForm = ({ type, items = [], locations = [], onSubmit, onCancel }) => {
  const { register, handleSubmit, formState: { errors }, reset, watch } = useForm({
    defaultValues: {
      type: type,
      item_id: '',
      quantity: 1,
      date: new Date().toISOString().split('T')[0],
      source_location_id: '',
      destination_location_id: '',
      reference: '',
      notes: ''
    }
  });

  // Re-sync form default values if type changes while modal is open
  useEffect(() => {
    reset({
      type: type,
      item_id: '',
      quantity: 1,
      date: new Date().toISOString().split('T')[0],
      source_location_id: '',
      destination_location_id: '',
      reference: '',
      notes: ''
    });
  }, [type, reset]);

  const getActionText = () => {
    switch(type) {
      case 'IN': return 'Stock In';
      case 'OUT': return 'Stock Out';
      case 'TRANSFER': return 'Transfer Stock';
      case 'ADJUSTMENT': return 'Stock Adjustment';
      default: return 'Process Transaction';
    }
  };

  const showSource = ['OUT', 'TRANSFER'].includes(type);
  const showDestination = ['IN', 'TRANSFER', 'ADJUSTMENT'].includes(type);

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 mt-4">
      <input type="hidden" {...register('type')} />

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Select Item *</label>
        <Select {...register('item_id', { required: 'Please select an item' })} error={!!errors.item_id}>
          <option value="">-- Choose Item --</option>
          {items.map(item => (
            <option key={item.id} value={item.id}>
              {item.sku} - {item.name} ({item.stock_qty || 0} available)
            </option>
          ))}
        </Select>
        {errors.item_id && <p className="mt-1 text-xs text-rose-500">{errors.item_id.message}</p>}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {showSource && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Source Location *</label>
            <Select 
              {...register('source_location_id', { required: showSource ? 'Source location is required' : false })} 
              error={!!errors.source_location_id}
            >
              <option value="">-- Select Source --</option>
              {locations.map(loc => (
                <option key={loc.id} value={loc.id}>{loc.name}</option>
              ))}
            </Select>
            {errors.source_location_id && <p className="mt-1 text-xs text-rose-500">{errors.source_location_id.message}</p>}
          </div>
        )}

        {showDestination && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Destination Location *</label>
            <Select 
              {...register('destination_location_id', { required: showDestination ? 'Destination location is required' : false })} 
              error={!!errors.destination_location_id}
            >
              <option value="">-- Select Destination --</option>
              {locations.map(loc => (
                <option key={loc.id} value={loc.id}>{loc.name}</option>
              ))}
            </Select>
            {errors.destination_location_id && <p className="mt-1 text-xs text-rose-500">{errors.destination_location_id.message}</p>}
          </div>
        )}
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Quantity *</label>
          <Input 
            type="number" 
            min="1"
            {...register('quantity', { required: 'Quantity is required', min: 1, valueAsNumber: true })} 
            error={!!errors.quantity} 
          />
          {errors.quantity && <p className="mt-1 text-xs text-rose-500">{errors.quantity.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Date *</label>
          <Input 
            type="date"
            {...register('date', { required: 'Date is required' })} 
            error={!!errors.date} 
          />
          {errors.date && <p className="mt-1 text-xs text-rose-500">{errors.date.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Reference</label>
          <Input 
            type="text"
            placeholder="PO-12345"
            {...register('reference')} 
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Notes</label>
        <Textarea {...register('notes')} rows={3} placeholder="Purpose of transaction, condition, or other details..." />
      </div>
      
      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">{getActionText()}</Button>
      </div>
    </form>
  );
};

export default TransactionForm;
