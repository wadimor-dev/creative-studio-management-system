import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import Badge from '../../components/common/Badge';
import { Plus, Edit2, Trash2, Search, Image as ImageIcon, Package } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import ProductsTabs from './components/ProductsTabs';
import ProductForm from './components/ProductForm';
import GlobalFilter from '../../components/common/GlobalFilter';
import { useProducts } from '../../hooks/useProducts';
import { productService } from '../../api/services/productService';

const Catalog = () => {
  const [filters, setFilters] = useState({});
  const { data: products, loading, refetch } = useProducts(filters);
  const [searchTerm, setSearchTerm] = useState('');
  
  const [formModal, setFormModal] = useState({ isOpen: false, data: null });
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, data: null });

  const openFormModal = (item = null) => setFormModal({ isOpen: true, data: item });
  const closeFormModal = () => setFormModal({ isOpen: false, data: null });
  
  const openDeleteModal = (item) => setDeleteModal({ isOpen: true, data: item });
  const closeDeleteModal = () => setDeleteModal({ isOpen: false, data: null });

  const handleFormSubmit = async (formData) => {
    try {
      const res = formModal.data
        ? await productService.update(formModal.data.id, formData)
        : await productService.create(formData);

      if (res.success) {
        toastSuccess(`Product ${formModal.data ? 'updated' : 'created'} successfully!`);
        closeFormModal();
        refetch();
      } else {
        toastError(res.message);
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      const res = await productService.delete(deleteModal.data.id);
      if (res.success) {
        toastSuccess("Deleted successfully!");
        closeDeleteModal();
        refetch();
      } else {
        toastError(res.message);
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    }
  };

  // Safe array check because paginated response might return data inside .data (res.data.data) depending on interceptor
  const productArray = Array.isArray(products) ? products : (products?.data || []);

  const filteredProducts = productArray.filter(p => 
    p.display_name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    p.sku.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <PageHeader 
        title="Products" 
        description="Manage your product catalog, movements, and master data."
      />
      
      <ProductsTabs />

      <GlobalFilter 
        availableFilters={['type', 'category', 'motif', 'sub_motif', 'color']} 
        onApply={setFilters} 
      />

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
        <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row justify-between gap-4">
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text"
              placeholder="Search SKU or Name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
            />
          </div>
          <Button variant="primary" size="sm" className="gap-2" onClick={() => openFormModal()}>
            <Plus size={16} />
            New Product
          </Button>
        </div>

        <div className="overflow-x-auto">
          {loading ? (
            <div className="flex justify-center items-center h-48">
              <LoadingSpinner size="md" />
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                  <th className="p-4 font-medium border-b border-slate-200 w-16">Image</th>
                  <th className="p-4 font-medium border-b border-slate-200">Product Info</th>
                  <th className="p-4 font-medium border-b border-slate-200">Classification</th>
                  <th className="p-4 font-medium border-b border-slate-200">Status</th>
                  <th className="p-4 font-medium border-b border-slate-200 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="text-sm divide-y divide-slate-100">
                {filteredProducts.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="p-4">
                      {item.image_url ? (
                        <img src={item.image_url} alt={item.display_name} className="w-10 h-10 rounded-md object-cover border border-slate-200" />
                      ) : (
                        <div className="w-10 h-10 rounded-md bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-400">
                          <ImageIcon size={18} />
                        </div>
                      )}
                    </td>
                    <td className="p-4">
                      <div className="font-semibold text-slate-900">{item.display_name}</div>
                      <div className="text-xs font-mono text-slate-500 mt-0.5 bg-slate-100 inline-block px-1.5 py-0.5 rounded">{item.sku}</div>
                    </td>
                    <td className="p-4">
                      <div className="flex flex-wrap gap-1">
                        <Badge variant="default" className="text-[10px] py-0">{item.type?.name}</Badge>
                        <Badge variant="default" className="text-[10px] py-0">{item.category?.name}</Badge>
                        <Badge variant="default" className="text-[10px] py-0 bg-blue-50 text-blue-600 border-blue-200">{item.motif?.name}</Badge>
                        <Badge variant="default" className="text-[10px] py-0 bg-rose-50 text-rose-600 border-rose-200">{item.color?.name}</Badge>
                        {item.variant && <Badge variant="warning" className="text-[10px] py-0">{item.variant}</Badge>}
                      </div>
                    </td>
                    <td className="p-4">
                      <Badge variant={item.status === 'ACTIVE' ? 'success' : 'default'}>{item.status}</Badge>
                    </td>
                    <td className="p-4 text-right">
                      <div className="flex justify-end gap-1">
                        <button 
                          onClick={() => openFormModal(item)}
                          className="p-1.5 text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded transition-colors"
                        >
                          <Edit2 size={14} />
                        </button>
                        <button 
                          onClick={() => openDeleteModal(item)}
                          className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded transition-colors"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
                {filteredProducts.length === 0 && (
                  <tr>
                    <td colSpan="5" className="p-12 text-center">
                      <div className="text-slate-400 mb-2 flex justify-center"><Package size={32} /></div>
                      <div className="text-slate-600 font-medium">No products found</div>
                      <div className="text-slate-500 text-sm mt-1">Try adjusting your search or add a new product.</div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <Modal 
        isOpen={formModal.isOpen} 
        onClose={closeFormModal} 
        title={formModal.data ? `Edit Product` : `New Product`}
      >
        <ProductForm 
          initialData={formModal.data}
          onSubmit={handleFormSubmit} 
          onCancel={closeFormModal} 
        />
      </Modal>

      <ConfirmDialog 
        isOpen={deleteModal.isOpen}
        onClose={closeDeleteModal}
        onConfirm={handleDeleteConfirm}
        title="Delete Product"
        description={`Are you sure you want to delete "${deleteModal.data?.display_name}"?`}
        isDanger={true}
        confirmText="Delete"
      />

    </div>
  );
};

export default Catalog;
