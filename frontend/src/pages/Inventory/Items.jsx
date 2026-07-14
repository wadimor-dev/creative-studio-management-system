import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Plus } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import InventoryTabs from './components/InventoryTabs';
import GlobalFilter from '../../components/common/GlobalFilter';
import SearchInput from '../../components/common/SearchInput';
import ItemTable from './components/ItemTable';
import ItemForm from './components/ItemForm';

import { useInventory } from '../../hooks/useInventory';
import { inventoryService } from '../../api/services/inventoryService';

const ItemsPage = () => {
  const [filters, setFilters] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  
  // Combine searchTerm and filters for the API request
  const { data: items, loading, refetch } = useInventory('items', { ...filters, search: searchTerm });
  
  const [formModal, setFormModal] = useState({ isOpen: false, data: null });
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, data: null });

  const openAddModal = () => setFormModal({ isOpen: true, data: null });
  const openEditModal = (item) => {
    // Map backend response to frontend form fields
    const mappedData = {
      id: item.id,
      code: item.sku,
      name: item.name,
      category: item.category?.id?.toString() || '',
      quantity: item.stock_qty || 0,
      unit: item.unit?.id?.toString() || 'pcs',
      location: item.location?.id?.toString() || '',
      status: item.is_active ? 'READY' : 'MAINTENANCE',
      description: item.description || ''
    };
    setFormModal({ isOpen: true, data: mappedData });
  };
  const closeFormModal = () => setFormModal({ isOpen: false, data: null });

  const openDeleteModal = (item) => setDeleteModal({ isOpen: true, data: item });
  const closeDeleteModal = () => setDeleteModal({ isOpen: false, data: null });

  const handleFormSubmit = async (data) => {
    try {
      let res;
      
      const payload = {
        sku: data.code,
        name: data.name,
        description: data.description || null,
        is_active: data.status !== 'MAINTENANCE',
        category_id: data.category ? parseInt(data.category, 10) : null,
        unit_id: null, // Ignored since we don't have a reliable unit table in the form yet
        location_id: data.location ? parseInt(data.location, 10) : null,
        initial_stock: data.quantity ? parseInt(data.quantity, 10) : 0,
        stock_qty: data.quantity ? parseInt(data.quantity, 10) : 0
      };

      if (formModal.data?.id) {
        res = await inventoryService.updateItem(formModal.data.id, payload);
      } else {
        res = await inventoryService.createItem(payload);
      }

      if (res.success) {
        toastSuccess(formModal.data ? "Item updated successfully!" : "Item added successfully!");
        closeFormModal();
        refetch();
      } else {
        toastError(res.message || "Operation failed");
      }
    } catch (err) {
      toastError("Failed to connect to server");
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      if (deleteModal.data?.id) {
        const res = await inventoryService.deleteItem(deleteModal.data.id);
        if (res.success) {
          toastSuccess("Item deleted successfully!");
          closeDeleteModal();
          refetch();
        } else {
          toastError(res.message || "Failed to delete item");
        }
      }
    } catch (err) {
      toastError("Failed to connect to server");
    }
  };

  

  return (
    <div>
      <PageHeader 
        title="Inventory" 
        description="Manage your items, track stock movements, and review history."
        action={
          <Button variant="primary" className="gap-2" onClick={openAddModal}>
            <Plus size={16} />
            Add Item
          </Button>
        }
      />
      
      <InventoryTabs />

      <div className="space-y-6">
        <div className="flex flex-col gap-4">
          <div className="w-full sm:w-1/3">
            <SearchInput 
              placeholder="Search code, name..." 
              value={searchTerm} 
              onChange={(e) => setSearchTerm(e.target.value)} 
            />
          </div>
          <GlobalFilter 
            availableFilters={['inventory_category', 'location']} 
            onApply={setFilters} 
          />
        </div>
        
        {loading ? (
          <div className="flex justify-center p-12">
            <LoadingSpinner size="md" />
          </div>
        ) : (
          <ItemTable 
            data={Array.isArray(items) ? items : []} 
            onEdit={openEditModal} 
            onDelete={openDeleteModal} 
          />
        )}
      </div>

      <Modal 
        isOpen={formModal.isOpen} 
        onClose={closeFormModal} 
        title={formModal.data ? 'Edit Item' : 'Add New Item'}
      >
        <ItemForm 
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
        description={`Are you sure you want to delete "${deleteModal.data?.name}"? This action cannot be undone.`}
        isDanger={true}
        confirmText="Delete"
      />
    </div>
  );
};

export default ItemsPage;
