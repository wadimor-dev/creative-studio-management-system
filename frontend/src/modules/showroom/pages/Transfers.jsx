import React from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import StockCard from '../components/StockCard';
import Badge from '../../../components/common/Badge';
import DataTable from '../../../components/common/DataTable';
import { useShowroomTransfers } from '../../../hooks/useShowroom';
import {
  Truck,
  Clock,
  CheckCircle,
  XCircle,
  Plus,
  ArrowUpRight,
  Eye,
  X,
} from 'lucide-react';

const statusVariant = {
  pending: 'warning',
  in_transit: 'info',
  completed: 'success',
  cancelled: 'danger',
};

const Transfers = () => {
  const [selectedStatus, setSelectedStatus] = React.useState('all');
  const { stats, transfers, loading, error, refetch, cancelTransfer, confirmReceipt } = useShowroomTransfers(
    selectedStatus !== 'all' ? { status: selectedStatus } : {}
  );

  const handleStatusFilter = (status) => {
    setSelectedStatus(status);
  };

  const handleCancelTransfer = async (id) => {
    try {
      await cancelTransfer(id);
    } catch (err) {
      console.error('Failed to cancel transfer:', err);
    }
  };

  const handleConfirmReceipt = async (id) => {
    try {
      await confirmReceipt(id);
    } catch (err) {
      console.error('Failed to confirm receipt:', err);
    }
  };

  const columns = [
    {
      header: 'ID Transfer',
      accessor: 'id',
      className: 'font-mono text-xs',
    },
    {
      header: 'Dari Lokasi',
      accessor: 'fromLocation',
    },
    {
      header: 'Ke Lokasi',
      accessor: 'toLocation',
    },
    {
      header: 'Items',
      accessor: 'items',
      cell: (row) => (
        <div>
          <p className="font-medium text-neutral-900">{row.totalQuantity} item</p>
          <p className="text-xs text-neutral-500">{row.items.length} jenis produk</p>
        </div>
      ),
    },
    {
      header: 'Tanggal',
      accessor: 'createdAt',
      cell: (row) => new Date(row.createdAt).toLocaleDateString('id-ID'),
    },
    {
      header: 'Estimasi Tiba',
      accessor: 'estimatedArrival',
      cell: (row) => new Date(row.estimatedArrival).toLocaleDateString('id-ID'),
    },
    {
      header: 'Status',
      accessor: 'status',
      cell: (row) => (
        <Badge variant={statusVariant[row.status] || 'default'}>
          {row.status === 'pending' ? 'Pending' :
           row.status === 'in_transit' ? 'Dalam Perjalanan' :
           row.status === 'completed' ? 'Selesai' :
           row.status === 'cancelled' ? 'Dibatalkan' : row.status}
        </Badge>
      ),
    },
    {
      header: 'Aksi',
      accessor: 'actions',
      cell: (row) => (
        <div className="flex items-center gap-2">
          <Button variant="edit" size="sm" title="Lihat Detail">
            <Eye size={16} />
          </Button>
          {row.status === 'pending' && (
            <Button 
              variant="delete" 
              size="sm" 
              title="Batalkan Transfer"
              onClick={() => handleCancelTransfer(row.id)}
            >
              <X size={16} />
            </Button>
          )}
          {row.status === 'in_transit' && (
            <Button 
              variant="primary" 
              size="sm" 
              title="Konfirmasi Penerimaan"
              onClick={() => handleConfirmReceipt(row.id)}
            >
              <CheckCircle size={16} />
            </Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Manajemen Transfer"
        description="Monitoring dan manajemen transfer stok antar lokasi showroom."
        actions={
          <Button variant="primary" size="sm" className="gap-2">
            <Plus size={16} />
            Transfer Baru
          </Button>
        }
      />

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StockCard
          label="Transfer Pending"
          value={stats?.pendingTransfer || '0'}
          icon={Clock}
          trend="Menunggu konfirmasi"
          color="amber"
        />
        <StockCard
          label="Dalam Perjalanan"
          value={stats?.inTransit || '0'}
          icon={Truck}
          trend="Sedang dikirim"
          color="blue"
        />
        <StockCard
          label="Selesai Hari Ini"
          value={stats?.completedToday || '0'}
          icon={CheckCircle}
          trend="Transfer diterima"
          color="emerald"
        />
        <StockCard
          label="Total Bulan Ini"
          value={stats?.totalThisMonth || '0'}
          icon={ArrowUpRight}
          trend="Semua lokasi"
          color="rose"
        />
      </div>

      {/* Status Filter */}
      <div className="flex items-center gap-2">
        <Button
          variant={selectedStatus === 'all' ? 'primary' : 'outline'}
          size="sm"
          onClick={() => handleStatusFilter('all')}
        >
          Semua
        </Button>
        <Button
          variant={selectedStatus === 'pending' ? 'primary' : 'outline'}
          size="sm"
          onClick={() => handleStatusFilter('pending')}
        >
          Pending
        </Button>
        <Button
          variant={selectedStatus === 'in_transit' ? 'primary' : 'outline'}
          size="sm"
          onClick={() => handleStatusFilter('in_transit')}
        >
          Dalam Perjalanan
        </Button>
        <Button
          variant={selectedStatus === 'completed' ? 'primary' : 'outline'}
          size="sm"
          onClick={() => handleStatusFilter('completed')}
        >
          Selesai
        </Button>
        <Button
          variant={selectedStatus === 'cancelled' ? 'primary' : 'outline'}
          size="sm"
          onClick={() => handleStatusFilter('cancelled')}
        >
          Dibatalkan
        </Button>
      </div>

      {/* Transfers Table */}
      <div className="rounded-xl border border-stone-200 bg-white overflow-hidden">
        <div className="flex items-center justify-between border-b border-stone-100 px-5 py-4">
          <h3 className="text-sm font-semibold text-neutral-900">Daftar Transfer</h3>
        </div>
        <DataTable
          columns={columns}
          data={transfers || []}
          isLoading={loading}
          emptyStateTitle="Tidak ada data transfer"
          emptyStateDescription="Tidak ada transfer yang sesuai dengan filter yang dipilih"
        />
      </div>
    </div>
  );
};

export default Transfers;
