import React from 'react';
import DataTable from '../../../components/common/DataTable';
import Badge from '../../../components/common/Badge';
import Button from '../../../components/common/Button';
import { Edit2, Trash2 } from 'lucide-react';

const ItemTable = ({ data, isLoading, onEdit, onDelete }) => {
  const getStatusBadge = (status) => {
    switch(status) {
      case 'READY': return <Badge variant="success">READY</Badge>;
      case 'IN_USE': return <Badge variant="warning">IN USE</Badge>;
      case 'MAINTENANCE': return <Badge variant="danger">MAINTENANCE</Badge>;
      default: return <Badge variant="default">{status}</Badge>;
    }
  };

  const columns = [
    {
      header: 'Code',
      accessor: 'sku',
      cellClassName: 'font-medium text-slate-900'
    },
    {
      header: 'Name',
      accessor: 'name',
    },
    {
      header: 'Category',
      cell: (row) => row.category?.name || '-'
    },
    {
      header: 'Stock',
      cell: (row) => `${row.stock_qty} ${row.unit?.name || 'pcs'}`
    },
    {
      header: 'Status',
      cell: (row) => getStatusBadge(row.is_active ? 'READY' : 'MAINTENANCE')
    },
    {
      header: 'Action',
      cellClassName: 'text-right',
      cell: (row) => (
        <div className="flex justify-end gap-2">
          <Button variant="edit" onClick={() => onEdit(row)}>
            <Edit2 size={14} />
          </Button>
          <Button variant="delete" onClick={() => onDelete(row)}>
            <Trash2 size={14} />
          </Button>
        </div>
      )
    }
  ];

  return (
    <DataTable 
      columns={columns} 
      data={data} 
      isLoading={isLoading} 
      emptyStateTitle="No items found"
      emptyStateDescription="Try adjusting your search or filters."
    />
  );
};

export default ItemTable;
