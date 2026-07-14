import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import ProductsTabs from './components/ProductsTabs';
import MasterDataForm from './components/MasterDataForm';
import { useProductMaster } from '../../hooks/useProductMaster';
import { productMasterService } from '../../api/services/productMasterService';

const MASTER_TABS = [
  { id: 'types', label: 'Types', title: 'Product Type' },
  { id: 'categories', label: 'Categories', title: 'Category' },
  { id: 'motifs', label: 'Motifs', title: 'Motif' },
  { id: 'sub-motifs', label: 'Sub Motifs', title: 'Sub Motif' },
  { id: 'colors', label: 'Colors', title: 'Color' },
  { id: 'locations', label: 'Locations', title: 'Location' },
];

const MasterData = () => {
  const [activeTab, setActiveTab] = useState(MASTER_TABS[0].id);
  const activeTabConfig = MASTER_TABS.find(t => t.id === activeTab);
  
  const { data, loading, refetch } = useProductMaster(activeTab);
  
  const [formModal, setFormModal] = useState({ isOpen: false, data: null });
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, data: null });

  const openFormModal = (item = null) => setFormModal({ isOpen: true, data: item });
  const closeFormModal = () => setFormModal({ isOpen: false, data: null });
  
  const openDeleteModal = (item) => setDeleteModal({ isOpen: true, data: item });
  const closeDeleteModal = () => setDeleteModal({ isOpen: false, data: null });

  const handleFormSubmit = async (formData) => {
    try {
      const res = formModal.data
        ? await productMasterService.update(activeTab, formModal.data.id, formData)
        : await productMasterService.create(activeTab, formData);

      if (res.success) {
        toastSuccess(`${activeTabConfig.title} ${formModal.data ? 'updated' : 'created'} successfully!`);
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
      const res = await productMasterService.delete(activeTab, deleteModal.data.id);
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

  return (
    <div>
      <PageHeader 
        title="Products" 
        description="Manage your product catalog, movements, and master data."
      />
      
      <ProductsTabs />

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col md:flex-row">
        
        {/* Vertical Tabs Sidebar for Master Data */}
        <div className="w-full md:w-64 border-b md:border-b-0 md:border-r border-slate-200 bg-slate-50/50">
          <div className="p-4 border-b border-slate-200">
            <h3 className="font-semibold text-slate-800">Master Data</h3>
            <p className="text-xs text-slate-500 mt-1">Configure product attributes</p>
          </div>
          <nav className="flex flex-row md:flex-col overflow-x-auto md:overflow-x-visible">
            {MASTER_TABS.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex-shrink-0 text-left px-5 py-3 text-sm font-medium transition-colors border-b-2 md:border-b-0 md:border-l-2
                  ${activeTab === tab.id 
                    ? 'border-brand-500 text-brand-600 bg-brand-50/50' 
                    : 'border-transparent text-slate-600 hover:bg-slate-100'
                  }
                `}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content Area */}
        <div className="flex-1 min-h-[400px] flex flex-col">
          <div className="p-4 border-b border-slate-200 flex justify-between items-center">
            <h4 className="font-semibold text-slate-800">{activeTabConfig.label}</h4>
            <Button variant="primary" size="sm" className="gap-2" onClick={() => openFormModal()}>
              <Plus size={16} />
              Add {activeTabConfig.title}
            </Button>
          </div>

          <div className="flex-1 overflow-x-auto p-4">
            {loading ? (
              <div className="flex justify-center items-center h-48">
                <LoadingSpinner size="md" />
              </div>
            ) : (
              <table className="w-full text-left border-collapse border border-slate-200 rounded-lg overflow-hidden">
                <thead>
                  <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                    <th className="p-3 font-medium border-b border-slate-200 w-24">ID</th>
                    {activeTab !== 'locations' && <th className="p-3 font-medium border-b border-slate-200 w-32">Code</th>}
                    <th className="p-3 font-medium border-b border-slate-200">Name</th>
                    <th className="p-3 font-medium border-b border-slate-200 hidden sm:table-cell">Description</th>
                    <th className="p-3 font-medium border-b border-slate-200 text-right w-24">Actions</th>
                  </tr>
                </thead>
                <tbody className="text-sm divide-y divide-slate-100">
                  {data.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="p-3 text-slate-500">#{item.id}</td>
                      {activeTab !== 'locations' && <td className="p-3 font-semibold text-slate-700">{item.code}</td>}
                      <td className="p-3 font-medium text-slate-900">{item.name}</td>
                      <td className="p-3 text-slate-500 hidden sm:table-cell">{item.description || '-'}</td>
                      <td className="p-3 text-right">
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
                  {data.length === 0 && (
                    <tr>
                      <td colSpan="5" className="p-8 text-center text-slate-500">
                        No {activeTabConfig.label.toLowerCase()} found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>

      <Modal 
        isOpen={formModal.isOpen} 
        onClose={closeFormModal} 
        title={formModal.data ? `Edit ${activeTabConfig.title}` : `New ${activeTabConfig.title}`}
      >
        <MasterDataForm 
          entityTitle={activeTabConfig.title}
          entityId={activeTabConfig.id}
          initialData={formModal.data}
          onSubmit={handleFormSubmit} 
          onCancel={closeFormModal} 
        />
      </Modal>

      <ConfirmDialog 
        isOpen={deleteModal.isOpen}
        onClose={closeDeleteModal}
        onConfirm={handleDeleteConfirm}
        title="Delete Item"
        description={`Are you sure you want to delete "${deleteModal.data?.name}"?`}
        isDanger={true}
        confirmText="Delete"
      />

    </div>
  );
};

export default MasterData;
