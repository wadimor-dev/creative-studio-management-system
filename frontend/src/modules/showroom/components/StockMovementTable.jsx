import React from 'react';
import DataTable from '../../../components/common/DataTable';
import Badge from '../../../components/common/Badge';
import { TYPE_VARIANT, STATUS_VARIANT, MOVEMENT_TYPE } from '../constants';
import { formatDate, formatMovementType, formatStatus, formatQuantity } from '../helpers';

const StockMovementTable = ({ data, isLoading }) => {
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
        <Badge variant={TYPE_VARIANT[row.type] || 'default'}>
          {formatMovementType(row.type)}
        </Badge>
      ),
    },
    {
      header: 'Quantity',
      accessor: 'quantity',
      cell: (row) => (
        <span className={`font-medium ${row.type === MOVEMENT_TYPE.IN ? 'text-emerald-600' : 'text-rose-600'}`}>
          {formatQuantity(row.quantity, row.type)}
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
      cell: (row) => formatDate(row.date),
    },
    {
      header: 'Status',
      accessor: 'status',
      cell: (row) => (
        <Badge variant={STATUS_VARIANT[row.status] || 'default'}>
          {formatStatus(row.status)}
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
