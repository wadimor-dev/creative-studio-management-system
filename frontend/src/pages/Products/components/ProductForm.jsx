import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import Input from '../../../components/common/Input';
import Button from '../../../components/common/Button';
import { useProductMaster } from '../../../hooks/useProductMaster';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import { compressToWebP } from '../../../utils/imageCompress';
import { Upload, X, Loader2 } from 'lucide-react';
import apiClient from '../../../api/axios';

const ProductForm = ({ initialData, onSubmit, onCancel }) => {
  const { data: types, loading: loadingTypes } = useProductMaster('types', { paginated: false });
  const { data: categories, loading: loadingCategories } = useProductMaster('categories', { paginated: false });
  const { data: motifs, loading: loadingMotifs } = useProductMaster('motifs', { paginated: false });
  const { data: subMotifs, loading: loadingSubMotifs } = useProductMaster('sub-motifs', { paginated: false });

  const { register, handleSubmit, reset, setValue, formState: { errors } } = useForm({
    defaultValues: initialData || {
      type_id: '',
      category_id: '',
      motif_id: '',
      sub_motif_id: '',
      variant: '',
      image_url: ''
    }
  });

  const [imagePreview, setImagePreview] = useState(initialData?.image_url || null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const defaults = initialData || {
      type_id: '',
      category_id: '',
      motif_id: '',
      sub_motif_id: '',
      variant: '',
      image_url: ''
    };
    reset(defaults);
    setImagePreview(defaults.image_url || null);
    setUploadError(null);
  }, [initialData, reset]);

  const handleFileSelect = useCallback(async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const localUrl = URL.createObjectURL(file);
    setImagePreview(localUrl);
    setUploadError(null);

    setUploading(true);
    try {
      const webpBlob = await compressToWebP(file);
      const formData = new FormData();
      formData.append('file', webpBlob, 'image.webp');

      const res = await apiClient.post('/product-images/upload-image', formData);
      const url = res.data.url;

      setValue('image_url', url);
      setImagePreview(url);
    } catch (err) {
      const msg = err.response?.data?.message || err.message || 'Upload failed';
      setUploadError(msg);
      setImagePreview(initialData?.image_url || null);
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  }, [initialData, setValue]);

  const handleRemoveImage = useCallback(() => {
    setValue('image_url', '');
    setImagePreview(null);
    setUploadError(null);
  }, [setValue]);

  const handleFormSubmit = (data) => {
    const payload = {
      type_id: parseInt(data.type_id),
      category_id: parseInt(data.category_id),
      motif_id: parseInt(data.motif_id),
      sub_motif_id: data.sub_motif_id ? parseInt(data.sub_motif_id) : null,
      variant: data.variant || null,
      image_url: data.image_url || null,
    };
    onSubmit(payload);
  };

  const isLoading = loadingTypes || loadingCategories || loadingMotifs || loadingSubMotifs;

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <LoadingSpinner size="md" text="Loading master data..." />
      </div>
    );
  }

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
            {categories.map(c => <option key={c.id} value={c.id}>{c.name} ({c.code})</option>)}
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
            {motifs.map(m => <option key={m.id} value={m.id}>{m.name} ({m.code})</option>)}
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
            {subMotifs.map(s => <option key={s.id} value={s.id}>{s.name} ({s.code})</option>)}
          </select>
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
        <label className="block text-sm font-medium text-slate-700 mb-1">Product Image</label>
        <input type="hidden" {...register('image_url')} />

        <div className="flex items-start gap-4">
          {imagePreview && (
            <div className="relative w-32 h-32 rounded-lg overflow-hidden border border-slate-200 bg-slate-50 flex-shrink-0">
              <img
                src={imagePreview}
                alt="Preview"
                className="w-full h-full object-cover"
                onError={(e) => { e.target.style.display = 'none'; }}
              />
              {!uploading && (
                <button
                  type="button"
                  onClick={handleRemoveImage}
                  className="absolute top-1 right-1 p-1 bg-white/80 rounded-full hover:bg-white shadow-sm transition-colors"
                >
                  <X size={14} />
                </button>
              )}
            </div>
          )}

          <div className="flex-1">
            {!imagePreview && !uploading && (
              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center cursor-pointer hover:border-brand-400 transition-colors"
              >
                <Upload size={24} className="mx-auto text-slate-400 mb-2" />
                <p className="text-sm text-slate-600">Click to upload image</p>
                <p className="text-xs text-slate-400 mt-1">Auto-compressed to WebP</p>
              </div>
            )}

            {uploading && (
              <div className="flex items-center gap-2 text-sm text-slate-600">
                <Loader2 size={16} className="animate-spin" />
                Compressing & uploading...
              </div>
            )}

            {uploadError && (
              <p className="text-xs text-rose-500 mt-1">{uploadError}</p>
            )}

            {imagePreview && !uploading && (
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="text-sm text-brand-600 hover:text-brand-700 mt-2"
              >
                Change image
              </button>
            )}

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>
        </div>
      </div>

      <div className="pt-4 flex justify-end gap-3 border-t border-slate-100">
        <Button type="button" variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button type="submit" variant="primary">Save Product</Button>
      </div>
    </form>
  );
};

export default ProductForm;
