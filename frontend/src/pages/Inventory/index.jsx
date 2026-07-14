import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Plus, ArrowUpRight, ArrowDownRight, CornerUpLeft } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import InventoryTabs from './components/InventoryTabs';
import InventoryStats from './components/InventoryStats';
import RecentTransactions from './components/RecentTransactions';
import TransactionForm from './components/TransactionForm';
import InventoryExportButton from './components/InventoryExportButton';
import GlobalFilter from '../../components/common/GlobalFilter';

import { useInventory } from '../../hooks/useInventory';
import { useLocations } from '../../hooks/useLocations';
import { inventoryService } from '../../api/services/inventoryService';

const InventoryDashboard = () => {
  const [filters, setFilters] = useState({});
  const { data: transactions, loading: txLoading, refetch: refetchTx } = useInventory('transactions', filters);
  const { data: itemsList, loading: itemsLoading, refetch: refetchItems } = useInventory('items', filters);
  const { locations, loading: locLoading } = useLocations();
  const [modalState, setModalState] = useState({ isOpen: false, type: null });

  const openModal = (type) => setModalState({ isOpen: true, type });
  const closeModal = () => setModalState({ isOpen: false, type: null });

  const loading = txLoading || itemsLoading || locLoading;
  
  const refetch = () => {
    refetchTx();
    refetchItems();
  };

  const handleTransactionSubmit = async (data) => {
    try {
      const res = await inventoryService.createTransaction(data);
      if (res.success) {
        toastSuccess(`Transaction processed successfully!`);
        closeModal();
        refetch();
      } else {
        toastError(res.message || "Failed to process transaction");
      }
    } catch (err) {
      toastError("Failed to connect to server");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full min-h-[400px]">
        <LoadingSpinner size="lg" text="Loading inventory overview..." />
      </div>
    );
  }

  // Ensure itemsList and transactions are arrays
  const safeTransactions = Array.isArray(transactions) ? transactions : [];
  const availableItems = Array.isArray(itemsList) ? itemsList : [];
  
  // Calculate stats from availableItems
  const locationArray = Array.isArray(locations) ? locations : (locations?.data || []);

  return (
    <div>
      <PageHeader 
        title="Inventory" 
        description="Manage your items, track stock movements, and review history."
        action={<InventoryExportButton filters={filters} />}
      />
      
      <InventoryTabs />

      <GlobalFilter 
        availableFilters={['inventory_category', 'location', 'user', 'date']} 
        onApply={setFilters} 
      />

      <div className="space-y-6">
        <InventoryStats locations={locationArray} items={availableItems} />

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
          <Button variant="secondary" className="h-24 flex-col gap-2 shadow-sm" onClick={() => openModal('IN')}>
            <ArrowDownRight size={24} className="text-emerald-500" />
            <span>Stock In</span>
          </Button>
          <Button variant="secondary" className="h-24 flex-col gap-2 shadow-sm" onClick={() => openModal('OUT')}>
            <ArrowUpRight size={24} className="text-rose-500" />
            <span>Stock Out</span>
          </Button>
          <Button variant="secondary" className="h-24 flex-col gap-2 shadow-sm" onClick={() => openModal('TRANSFER')}>
            <CornerUpLeft size={24} className="text-blue-500" />
            <span>Transfer</span>
          </Button>
          <Button variant="secondary" className="h-24 flex-col gap-2 shadow-sm" onClick={() => openModal('ADJUSTMENT')}>
            <Plus size={24} className="text-amber-500" />
            <span>Adjustment</span>
          </Button>
        </div>

        <RecentTransactions data={safeTransactions} />
      </div>

      <Modal 
        isOpen={modalState.isOpen} 
        onClose={closeModal} 
        title={
          modalState.type === 'IN' ? 'Stock In' : 
          modalState.type === 'OUT' ? 'Stock Out' : 
          modalState.type === 'TRANSFER' ? 'Transfer Stock' : 'Stock Adjustment'
        }
      >
        <TransactionForm 
          type={modalState.type} 
          items={availableItems}
          locations={locations || []}
          onSubmit={handleTransactionSubmit} 
          onCancel={closeModal} 
        />
      </Modal>
    </div>
  );
};

export default InventoryDashboard;
