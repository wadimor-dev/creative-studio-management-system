import React from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import StockCard from '../components/StockCard';
import StockMovementTable from '../components/StockMovementTable';
import Select from '../../../components/common/Select';
import { useShowroomStock, useShowroomLocations } from '../../../hooks/useShowroom';
import {
  Package,
  ArrowUpRight,
  ArrowDownRight,
  Truck,
  Plus,
  Filter,
} from 'lucide-react';

const Stock = () => {
  const [selectedLocation, setSelectedLocation] = React.useState('all');
  const { stats, movements, loading, error, refetch } = useShowroomStock(
    selectedLocation !== 'all' ? { location: selectedLocation } : {}
  );
  const { locations: locationOptions, loading: locationsLoading } = useShowroomLocations();

  const locationSelectOptions = [
    { value: 'all', label: 'Semua Lokasi' },
    ...(locationOptions || []).map(loc => ({
      value: loc.id || loc.value,
      label: loc.name || loc.label,
    })),
  ];

  const handleLocationChange = (e) => {
    setSelectedLocation(e.target.value);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Manajemen Stok"
        description="Monitoring dan manajemen stok produk di semua lokasi showroom."
        actions={
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="gap-2">
              <Filter size={16} />
              Filter
            </Button>
            <Button variant="primary" size="sm" className="gap-2">
              <Plus size={16} />
              Barang Masuk
            </Button>
          </div>
        }
      />

      {/* Location Filter */}
      <div className="flex items-center gap-4">
        <label className="text-sm font-medium text-neutral-700">Lokasi:</label>
        <Select
          value={selectedLocation}
          onChange={handleLocationChange}
          options={locationSelectOptions}
          className="w-64"
          disabled={locationsLoading}
        />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StockCard
          label="Total Stok"
          value={stats?.totalStock || '0'}
          icon={Package}
          trend="Semua lokasi"
          color="blue"
        />
        <StockCard
          label="Stok Masuk Hari Ini"
          value={stats?.stockInToday || '+0'}
          icon={ArrowUpRight}
          trend={stats?.stockInCount || '0 transaksi'}
          color="emerald"
        />
        <StockCard
          label="Stok Keluar Hari Ini"
          value={stats?.stockOutToday || '-0'}
          icon={ArrowDownRight}
          trend={stats?.stockOutCount || '0 transaksi'}
          color="rose"
        />
        <StockCard
          label="Transfer Pending"
          value={stats?.pendingTransfer || '0'}
          icon={Truck}
          trend={stats?.inTransit || '0 dalam perjalanan'}
          color="amber"
        />
      </div>

      {/* Stock Movements Table */}
      <div className="rounded-xl border border-stone-200 bg-white overflow-hidden">
        <div className="flex items-center justify-between border-b border-stone-100 px-5 py-4">
          <h3 className="text-sm font-semibold text-neutral-900">Riwayat Pergerakan Stok</h3>
          <button className="flex items-center gap-1 text-xs font-medium text-amber-600 hover:text-amber-700">
            Lihat semua <ArrowUpRight size={14} />
          </button>
        </div>
        <div className="p-5">
          <StockMovementTable data={movements || []} isLoading={loading} />
        </div>
      </div>
    </div>
  );
};

export default Stock;
