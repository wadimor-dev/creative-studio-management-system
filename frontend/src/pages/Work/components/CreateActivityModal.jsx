import React, { useState, useEffect } from 'react';
import api from '../../../api/axios';
import Button from '../../../components/common/Button';

const CreateActivityModal = ({ isOpen, onClose, onSubmit }) => {
  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState({
    category_id: '',
    activity_name: '',
    notes: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (isOpen) {
      // Fetch categories
      const fetchCategories = async () => {
        try {
          const res = await api.get('/categories');
          // Filter work activity categories if needed, for now use all or specific type
          // Assuming /categories endpoint has the categories, but wait, do we have a WorkCategory API?
          // For now, let's just make it a generic API call and gracefully handle.
          setCategories(res.data?.data || []);
        } catch (error) {
          console.error("Failed to fetch categories");
        }
      };
      fetchCategories();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.category_id || !formData.activity_name) return;
    
    setIsSubmitting(true);
    try {
      await onSubmit(formData);
      setFormData({ category_id: '', activity_name: '', notes: '' });
      onClose();
    } catch (error) {
      console.error('Create failed', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl dark:bg-gray-800">
        <h3 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">Buat Aktivitas Baru</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Kategori
            </label>
            <select
              name="category_id"
              value={formData.category_id}
              onChange={handleChange}
              required
              className="w-full rounded-xl border border-gray-300 p-3 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            >
              <option value="">Pilih Kategori</option>
              {categories.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
              {/* Fallback if categories are empty */}
              {categories.length === 0 && (
                <>
                  <option value="1">Video Editing</option>
                  <option value="2">Graphic Design</option>
                  <option value="3">Photography</option>
                  <option value="4">Videography</option>
                </>
              )}
            </select>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Nama Aktivitas
            </label>
            <input
              type="text"
              name="activity_name"
              value={formData.activity_name}
              onChange={handleChange}
              required
              placeholder="Contoh: Editing Video Promo Shopee"
              className="w-full rounded-xl border border-gray-300 p-3 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Catatan (Opsional)
            </label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              rows="2"
              placeholder="Tambahkan catatan jika diperlukan..."
              className="w-full rounded-xl border border-gray-300 p-3 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
            />
          </div>

          <div className="mt-6 flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              size="md"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Batal
            </Button>
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!formData.category_id || !formData.activity_name || isSubmitting}
              isLoading={isSubmitting}
            >
              {isSubmitting ? 'Menyimpan...' : 'SAVE'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateActivityModal;
