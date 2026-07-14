import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Button from '../../../components/common/Button';
import { useProductMaster } from '../../../hooks/useProductMaster';
import LoadingSpinner from '../../../components/common/LoadingSpinner';

const ProductForm = ({ initialData, onSubmit, onCancel }) => {
  const { data: types, loading: loadingTypes } = useProductMaster('types');
  const { data: categories, loading: loadingCategories } = useProductMaster('categories');
  const { data: motifs, loading: loadingMotifs } = useProductMaster('motifs');
  const { data: subMotifs, loading: loadingSubMotifs } = useProductMaster('sub-motifs');
  const { data: colors, loading: loadingColors } = useProductMaster('colors');

  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    defaultValues: initialData || {
      type_id: '',
      category_id: '',
      motif_id: '',
      sub_motif_id: '',
      color_id: '',
      variant: '',
      image_url: ''
    }
  });

  useEffect(() => {
    reset(initialData || {
      type_id: '',
      category_id: '',
      motif_id: '',
      sub_motif_id: '',
      color_id: '',
      variant: '',
      image_url: ''
    });
  }, [initialData, reset]);

  const isLoading = loadingTypes || loadingCategories || loadingMotifs || loadingSubMotifs || loadingColors;

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <LoadingSpinner size="md" text="Loading master data..." />
      </div>
    );
  }

  const handleFormSubmit = (data) => {
    // Transform string IDs to integers and handle empty sub_motif
    const payload = {
      type_id: parseInt(data.type_id),
      category_id: parseInt(data.category_id),
      motif_id: parseInt(data.motif_id),
      color_id: parseInt(data.color_id),
      sub_motif_id: data.sub_motif_id ? parseInt(data.sub_motif_id) : null,
      variant: data.variant || null,
      image_url: data.image_url || null,
    };
    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 mt-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Product Type *</label>
          <select 
            className={`w-full rounded-lg border ${errors.type_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
            {...register('type_id', { required: 'Type is required' })}
          >
            <option value="">Select Type</option>
            {types.map(t => <option key={t.id} value={t.id}>{t.name} ({t.code})</option>)}
          </select>
          {errors.type_id && <p className="mt-1 text-xs text-rose-500">{errors.type_id.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Category *</label>
          <select 
            className={`w-full rounded-lg border ${errors.category_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
            {...register('category_id', { required: 'Category is required' })}
          >
            <option value="">Select Category</option>
            {categories.map(t => <option key={t.id} value={t.id}>{t.name} ({t.code})</option>)}
          </select>
          {errors.category_id && <p className="mt-1 text-xs text-rose-500">{errors.category_id.message}</p>}
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Motif *</label>
          <select 
            className={`w-full rounded-lg border ${errors.motif_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
            {...register('motif_id', { required: 'Motif is required' })}
          >
            <option value="">Select Motif</option>
            {motifs.map(t => <option key={t.id} value={t.id}>{t.name} ({t.code})</option>)}
          </select>
          {errors.motif_id && <p className="mt-1 text-xs text-rose-500">{errors.motif_id.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Sub Motif</label>
          <select 
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            {...register('sub_motif_id')}
          >
            <option value="">- None -</option>
            {subMotifs.map(t => <option key={t.id} value={t.id}>{t.name} ({t.code})</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Color *</label>
          <select 
            className={`w-full rounded-lg border ${errors.color_id ? 'border-rose-500' : 'border-slate-300'} px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500`}
            {...register('color_id', { required: 'Color is required' })}
          >
            <option value="">Select Color</option>
            {colors.map(t => <option key={t.id} value={t.id}>{t.name} ({t.code})</option>)}
          </select>
          {errors.color_id && <p className="mt-1 text-xs text-rose-500">{errors.color_id.message}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Variant (Size/Package)</label>
          <Input 
            {...register('variant')} 
            placeholder="e.g. Reguler, Box"
          />
        </div>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Image URL</label>
        <Input 
          {...register('image_url')} 
          placeholder="https://..."
        />
        <p className="text-xs text-slate-500 mt-1">Optional. Direct link to image file.</p>
      </div>
      
      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">Save Product</Button>
      </div>
    </form>
  );
};

export default ProductForm;
