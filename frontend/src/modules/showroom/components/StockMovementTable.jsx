import React from 'react';
import DataTable from '../../../components/common/DataTable';
import Badge from '../../../components/common/Badge';

const StockMovementTable = ({ data, isLoading }) => {
  const typeVariant = {
    IN: 'success',
    OUT: 'danger',
    TRANSFER: 'info',
  };

  const statusVariant = {
    completed: 'success',
    pending: 'warning',
    cancelled: 'danger',
    in_transit: 'info',
  };

  const columns = [
    {
      header: 'ID',
      accessor: 'id',
      className: 'font-mono text-xs',
    },
    {
      header: 'Produk',
      accessor: 'product',
      cell: (row) => (
        <div>
          <p className="font-medium text-neutral-900">{row.product.name}</p>
          <p className="text-xs text-neutral-500">{row.product.sku}</p>
        </div>
      ),
    },
    {
      header: 'Tipe',
      accessor: 'type',
      cell: (row) => (
        <Badge variant={typeVariant[row.type] || 'default'}>
          {row.type === 'IN' ? 'Masuk' : row.type === 'OUT' ? 'Keluar' : 'Transfer'}
        </Badge>
      ),
    },
    {
      header: 'Quantity',
      accessor: 'quantity',
      cell: (row) => (
        <span className={`font-medium ${row.type === 'IN' ? 'text-emerald-600' : 'text-rose-600'}`}>
          {row.type === 'IN' ? '+' : '-'}{row.quantity}
        </span>
      ),
    },
    {
      header: 'Lokasi',
      accessor: 'location',
    },
    {
      header: 'Tanggal',
      accessor: 'date',
      cell: (row) => new Date(row.date).toLocaleDateString('id-ID'),
    },
    {
      header: 'Status',
      accessor: 'status',
      cell: (row) => (
        <Badge variant={statusVariant[row.status] || 'default'}>
          {row.status === 'completed' ? 'Selesai' : 
           row.status === 'pending' ? 'Pending' :
           row.status === 'cancelled' ? 'Dibatalkan' :
           row.status === 'in_transit' ? 'Dalam Perjalanan' : row.status}
        </Badge>
      ),
    },
  ];

  return (
    <DataTable
      columns={columns}
      data={data}
      isLoading={isLoading}
      emptyStateTitle="Tidak ada data pergerakan stok"
      emptyStateDescription="Belum ada pergerakan stok untuk ditampilkan"
    />
  );
};

export default StockMovementTable;
