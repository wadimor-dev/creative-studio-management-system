import React from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import StockCard from '../components/StockCard';
import DataTable from '../../../components/common/DataTable';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import Badge from '../../../components/common/Badge';
import { useShowroomStockIn } from '../../../hooks/useShowroom';
import { STATUS_VARIANT, LOCATION_OPTIONS, SUPPLIER_OPTIONS, PRODUCT_OPTIONS } from '../constants';
import { formatDate, formatStatus, getInitialStockInForm } from '../helpers';
import {
  ArrowUpRight,
  Plus,
  Package,
  Calendar,
  User,
} from 'lucide-react';

const StockIn = () => {
  const [showForm, setShowForm] = React.useState(false);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [formData, setFormData] = React.useState(getInitialStockInForm());

  const { stats, stockIn, loading, error, refetch, createStockIn } = useShowroomStockIn();

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setIsSubmitting(true);
      await createStockIn(formData);
      setShowForm(false);
      setFormData(getInitialStockInForm());
    } catch (err) {
      console.error('Failed to create stock in:', err);
    } finally {
      setIsSubmitting(false);
    }
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
      header: 'Quantity',
      accessor: 'quantity',
      cell: (row) => (
        <span className="font-medium text-emerald-600">+{row.quantity}</span>
      ),
    },
    {
      header: 'Supplier',
      accessor: 'supplier',
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
      header: 'Reference',
      accessor: 'reference',
      className: 'font-mono text-xs',
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
    <div className="space-y-6">
      <PageHeader
        title="Barang Masuk"
        description="Record dan monitoring barang masuk ke showroom."
        actions={
          <Button variant="primary" size="sm" className="gap-2" onClick={() => setShowForm(!showForm)}>
            <Plus size={16} />
            {showForm ? 'Tutup Form' : 'Barang Masuk Baru'}
          </Button>
        }
      />

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StockCard
          label="Hari Ini"
          value={stats?.todayIn || '0'}
          icon={ArrowUpRight}
          trend="Barang masuk"
          color="emerald"
        />
        <StockCard
          label="Minggu Ini"
          value={stats?.thisWeek || '0'}
          icon={Calendar}
          trend="7 hari terakhir"
          color="blue"
        />
        <StockCard
          label="Bulan Ini"
          value={stats?.thisMonth || '0'}
          icon={Package}
          trend="30 hari terakhir"
          color="amber"
        />
        <StockCard
          label="Total Supplier"
          value={stats?.totalSuppliers || '0'}
          icon={User}
          trend="Aktif"
          color="rose"
        />
      </div>

      {/* Stock In Form */}
      {showForm && (
        <div className="rounded-xl border border-stone-200 bg-white p-6">
          <h3 className="text-lg font-semibold text-neutral-900 mb-4">Form Barang Masuk</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Produk *
                </label>
                <Select
                  value={formData.product}
                  onChange={(e) => handleInputChange('product', e.target.value)}
                  options={PRODUCT_OPTIONS}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Quantity *
                </label>
                <Input
                  type="number"
                  value={formData.quantity}
                  onChange={(e) => handleInputChange('quantity', e.target.value)}
                  placeholder="Masukkan quantity"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Supplier *
                </label>
                <Select
                  value={formData.supplier}
                  onChange={(e) => handleInputChange('supplier', e.target.value)}
                  options={SUPPLIER_OPTIONS}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Lokasi *
                </label>
                <Select
                  value={formData.location}
                  onChange={(e) => handleInputChange('location', e.target.value)}
                  options={LOCATION_OPTIONS}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Tanggal *
                </label>
                <Input
                  type="date"
                  value={formData.date}
                  onChange={(e) => handleInputChange('date', e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Reference (PO/DO)
                </label>
                <Input
                  value={formData.reference}
                  onChange={(e) => handleInputChange('reference', e.target.value)}
                  placeholder="Nomor referensi"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-1">
                Catatan
              </label>
              <Textarea
                rows={3}
                value={formData.notes}
                onChange={(e) => handleInputChange('notes', e.target.value)}
                placeholder="Tambahkan catatan..."
              />
            </div>

            <div className="flex justify-end gap-2 pt-4 border-t border-stone-200">
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowForm(false)}
              >
                Batal
              </Button>
              <Button type="submit" variant="primary" isLoading={isSubmitting}>
                Simpan
              </Button>
            </div>
          </form>
        </div>
      )}

      {/* Stock In Table */}
      <div className="rounded-xl border border-stone-200 bg-white overflow-hidden">
        <div className="flex items-center justify-between border-b border-stone-100 px-5 py-4">
          <h3 className="text-sm font-semibold text-neutral-900">Riwayat Barang Masuk</h3>
        </div>
        <DataTable
          columns={columns}
          data={stockIn || []}
          isLoading={loading}
          emptyStateTitle="Tidak ada data barang masuk"
          emptyStateDescription="Belum ada barang masuk untuk ditampilkan"
        />
      </div>
    </div>
  );
};

export default StockIn;
