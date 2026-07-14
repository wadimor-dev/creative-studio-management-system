import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import InventoryTabs from './components/InventoryTabs';
import CategoryForm from './components/CategoryForm';
import { useCategories } from '../../hooks/useCategories';
import { categoryService } from '../../api/services/categoryService';

const Categories = () => {
  const { categories, loading, refetch } = useCategories();
  const [modalState, setModalState] = useState({ isOpen: false, data: null });

  const openModal = (data = null) => setModalState({ isOpen: true, data });
  const closeModal = () => setModalState({ isOpen: false, data: null });

  const handleCategorySubmit = async (data) => {
    try {
      const res = modalState.data
        ? await categoryService.update(modalState.data.id, data)
        : await categoryService.create(data);

      if (res.success) {
        toastSuccess(`Category ${modalState.data ? 'updated' : 'created'} successfully!`);
        closeModal();
        refetch();
      } else {
        toastError(res.message || "Failed to save category");
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message || "An error occurred");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this category?")) {
      try {
        const res = await categoryService.delete(id);
        if (res.success) {
          toastSuccess("Category deleted successfully");
          refetch();
        } else {
          toastError(res.message);
        }
      } catch (err) {
        toastError(err.response?.data?.message || err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full min-h-[400px]">
        <LoadingSpinner size="lg" text="Loading categories..." />
      </div>
    );
  }

  return (
    <div>
      <PageHeader 
        title="Inventory" 
        description="Manage your items, track stock movements, and review history."
      />
      
      <InventoryTabs />

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
          <h3 className="font-semibold text-slate-800">Master Categories</h3>
          <Button variant="primary" size="sm" className="gap-2" onClick={() => openModal()}>
            <Plus size={16} />
            Add Category
          </Button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                <th className="p-4 font-medium border-b border-slate-200">ID</th>
                <th className="p-4 font-medium border-b border-slate-200">Name</th>
                <th className="p-4 font-medium border-b border-slate-200">Description</th>
                <th className="p-4 font-medium border-b border-slate-200 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="text-sm divide-y divide-slate-100">
              {categories.map((cat) => (
                <tr key={cat.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="p-4 text-slate-500">#{cat.id}</td>
                  <td className="p-4 font-medium text-slate-900">{cat.name}</td>
                  <td className="p-4 text-slate-500">{cat.description || '-'}</td>
                  <td className="p-4 text-right">
                    <div className="flex justify-end gap-2">
                      <button 
                        onClick={() => openModal(cat)}
                        className="p-1.5 text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                      >
                        <Edit2 size={16} />
                      </button>
                      <button 
                        onClick={() => handleDelete(cat.id)}
                        className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {categories.length === 0 && (
                <tr>
                  <td colSpan="4" className="p-8 text-center text-slate-500">
                    No categories found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <Modal 
        isOpen={modalState.isOpen} 
        onClose={closeModal} 
        title={modalState.data ? 'Edit Category' : 'New Category'}
      >
        <CategoryForm 
          initialData={modalState.data}
          onSubmit={handleCategorySubmit} 
          onCancel={closeModal} 
        />
      </Modal>

    </div>
  );
};

export default Categories;
