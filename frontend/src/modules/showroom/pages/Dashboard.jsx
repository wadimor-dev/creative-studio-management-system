import React from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Badge from '../../../components/common/Badge';
import Button from '../../../components/common/Button';
import { useShowroomDashboard } from '../../../hooks/useShowroom';
import { TYPE_VARIANT, STATUS_VARIANT } from '../constants';
import { formatMovementType, formatStatus } from '../helpers';
import {
  Package,
  Users,
  ShoppingCart,
  Truck,
  ArrowUpRight,
  Plus,
  ArrowDownRight,
  RefreshCw,
} from 'lucide-react';

const Dashboard = () => {
  const { stats, movements, loading, error, refetch } = useShowroomDashboard();
  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard Showroom"
        description="Ringkasan aktivitas stok, transfer, dan pergerakan barang showroom hari ini."
        actions={
          <Button variant="primary" size="sm" className="gap-2">
            <Plus size={16} />
            Barang Masuk
          </Button>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Stok', value: stats?.totalStock || '0', icon: Package, trend: 'Semua lokasi', color: 'blue' },
          { label: 'Stok Masuk Hari Ini', value: stats?.stockInToday || '+0', icon: ArrowUpRight, trend: stats?.stockInCount || '0 transaksi', color: 'emerald' },
          { label: 'Stok Keluar Hari Ini', value: stats?.stockOutToday || '-0', icon: ArrowDownRight, trend: stats?.stockOutCount || '0 transaksi', color: 'rose' },
          { label: 'Transfer Pending', value: stats?.pendingTransfer || '0', icon: Truck, trend: stats?.inTransit || '0 dalam perjalanan', color: 'amber' },
        ].map(({ label, value, icon: Icon, trend, color }) => {
          const colorVariants = {
            blue: 'bg-blue-50 text-blue-600',
            emerald: 'bg-emerald-50 text-emerald-600',
            rose: 'bg-rose-50 text-rose-600',
            amber: 'bg-amber-50 text-amber-600',
          };
          const colors = colorVariants[color] || colorVariants.blue;
          
          return (
            <div
              key={label}
              className="rounded-xl border border-stone-200 bg-white p-5"
            >
              <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${colors}`}>
                <Icon size={20} />
              </div>
              <p className="mt-4 text-2xl font-semibold text-neutral-900">{value}</p>
              <p className="text-sm text-neutral-500">{label}</p>
              <p className="mt-2 text-xs text-neutral-400">{trend}</p>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 rounded-xl border border-stone-200 bg-white overflow-hidden">
          <div className="flex items-center justify-between border-b border-stone-100 px-5 py-4">
            <h3 className="text-sm font-semibold text-neutral-900">Pergerakan Stok Terbaru</h3>
            <button className="flex items-center gap-1 text-xs font-medium text-amber-600 hover:text-amber-700">
              Lihat semua <ArrowUpRight size={14} />
            </button>
          </div>

          <div className="divide-y divide-stone-100">
            {(movements || []).map((movement) => (
              <div
                key={movement.id}
                className="flex items-center justify-between px-5 py-3.5 hover:bg-stone-50 transition-colors"
              >
                <div>
                  <p className="text-sm font-medium text-neutral-900">{movement.product}</p>
                  <p className="mt-0.5 font-mono text-xs text-neutral-500">{movement.id}</p>
                </div>
                <div className="flex items-center gap-4">
                  <span className={`text-sm font-medium ${movement.type === 'IN' ? 'text-emerald-600' : movement.type === 'OUT' ? 'text-rose-600' : 'text-blue-600'}`}>
                    {movement.type === 'IN' ? '+' : movement.type === 'OUT' ? '-' : ''}{movement.quantity}
                  </span>
                  <Badge variant={TYPE_VARIANT[movement.type] || 'default'}>
                    {formatMovementType(movement.type)}
                  </Badge>
                  <Badge variant={STATUS_VARIANT[movement.status] || 'default'}>
                    {formatStatus(movement.status)}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-stone-200 bg-white p-5">
          <h3 className="mb-4 text-sm font-semibold text-neutral-900">Aksi Cepat</h3>
          <div className="space-y-2">
            <Button variant="outline" size="sm" className="w-full justify-start gap-2">
              <ArrowUpRight size={16} />
              Barang Masuk
            </Button>
            <Button variant="outline" size="sm" className="w-full justify-start gap-2">
              <ArrowDownRight size={16} />
              Barang Keluar
            </Button>
            <Button variant="outline" size="sm" className="w-full justify-start gap-2">
              <RefreshCw size={16} />
              Transfer Stok
            </Button>
            <Button variant="outline" size="sm" className="w-full justify-start gap-2">
              <Package size={16} />
              Lihat Stok
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;