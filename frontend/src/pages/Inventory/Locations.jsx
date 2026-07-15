import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Plus, Edit2, Trash2 } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import InventoryTabs from './components/InventoryTabs';
import LocationForm from './components/LocationForm';
import { useLocations } from '../../hooks/useLocations';
import { locationService } from '../../api/services/locationService';

const Locations = () => {
  const { locations, loading, refetch } = useLocations();
  const [modalState, setModalState] = useState({ isOpen: false, data: null });

  const openModal = (data = null) => setModalState({ isOpen: true, data });
  const closeModal = () => setModalState({ isOpen: false, data: null });

  const handleLocationSubmit = async (data) => {
    try {
      const payload = { ...data };

      const res = modalState.data
        ? await locationService.update(modalState.data.id, payload)
        : await locationService.create(payload);

      if (res.success) {
        toastSuccess(`Location ${modalState.data ? 'updated' : 'created'} successfully!`);
        closeModal();
        refetch();
      } else {
        toastError(res.message || "Failed to save location");
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message || "An error occurred");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this location?")) {
      try {
        const res = await locationService.delete(id);
        if (res.success) {
          toastSuccess("Location deleted successfully");
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
        <LoadingSpinner size="lg" text="Loading locations..." />
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
          <h3 className="font-semibold text-slate-800">Master Locations</h3>
          <Button variant="primary" size="sm" className="gap-2" onClick={() => openModal()}>
            <Plus size={16} />
            Add Location
          </Button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                <th className="p-4 font-medium border-b border-slate-200">Name</th>
                <th className="p-4 font-medium border-b border-slate-200">Description</th>
                <th className="p-4 font-medium border-b border-slate-200 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="text-sm divide-y divide-slate-100">
              {locations.map((cat) => (
                <tr key={cat.id} className="hover:bg-slate-50/50 transition-colors">
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
              {locations.length === 0 && (
                <tr>
                  <td colSpan="3" className="p-8 text-center text-slate-500">
                    No locations found.
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
        title={modalState.data ? 'Edit Location' : 'New Location'}
      >
        <LocationForm 
          initialData={modalState.data}
          onSubmit={handleLocationSubmit} 
          onCancel={closeModal} 
        />
      </Modal>

    </div>
  );
};

export default Locations;
