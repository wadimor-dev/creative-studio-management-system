import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import DataTable from '../../components/common/DataTable';
import Badge from '../../components/common/Badge';
import SearchInput from '../../components/common/SearchInput';
import Select from '../../components/common/Select';
import Button from '../../components/common/Button';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import GlobalFilter from '../../components/common/GlobalFilter';

import InventoryTabs from './components/InventoryTabs';
import { useInventory } from '../../hooks/useInventory';

const HistoryPage = () => {
  const [filters, setFilters] = useState({});
  const [searchTerm, setSearchTerm] = useState('');
  
  const { data: transactions, loading, refetch } = useInventory('transactions', { ...filters, search: searchTerm });

  const getStatusBadge = (type) => {
    switch(type) {
      case 'IN': return <Badge variant="success">IN</Badge>;
      case 'RETURN': return <Badge variant="info">RETURN</Badge>;
      case 'OUT': return <Badge variant="warning">OUT</Badge>;
      default: return <Badge variant="default">{type}</Badge>;
    }
  };

  const columns = [
    { header: 'Date', accessor: 'date' },
    { 
      header: 'Item', 
      cellClassName: 'font-medium text-slate-900',
      cell: (row) => `${row.itemCode} - ${row.itemName}`
    },
    { 
      header: 'Type', 
      cell: (row) => getStatusBadge(row.type)
    },
    { header: 'Qty', accessor: 'quantity' },
    { header: 'User', accessor: 'user' },
    { header: 'Notes', accessor: 'notes', cellClassName: 'max-w-[200px] truncate' },
  ];

  return (
    <div>
      <PageHeader 
        title="Inventory" 
        description="Manage your items, track stock movements, and review history."
      />
      
      <InventoryTabs />

      <div className="space-y-6">
        <div className="flex flex-col gap-4">
          <div className="w-full sm:w-1/3">
            <SearchInput 
              placeholder="Search item, type..." 
              value={searchTerm} 
              onChange={(e) => setSearchTerm(e.target.value)} 
            />
          </div>
          <GlobalFilter 
            availableFilters={['inventory_category', 'location', 'user', 'date']} 
            onApply={setFilters} 
          />
        </div>
        
        {loading ? (
          <div className="flex justify-center p-12">
            <LoadingSpinner size="md" />
          </div>
        ) : (
          <DataTable 
            columns={columns} 
            data={transactions?.items || []} 
          />
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
