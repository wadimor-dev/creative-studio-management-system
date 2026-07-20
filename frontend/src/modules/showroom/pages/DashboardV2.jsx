import React, { useState, useEffect } from 'react';

import PageHeader from '../../../components/common/PageHeader';
import Badge from '../../../components/common/Badge';
import Button from '../../../components/common/Button';
import Card from '../../../components/common/Card';
import StatCard from '../../../components/common/StatCard';
import BarChart from '../../../components/charts/BarChart';
import LoadingSpinner from '../../../components/common/LoadingSpinner';

import { useShowroomDashboardKPI } from '../../../hooks/useShowroomV2';
import { showroomService } from '../../../api/services/showroomService';
import { formatDate } from '../helpers';
import {
  Package, ArrowLeftRight, Users, AlertTriangle,
  Clock, TrendingUp, RefreshCw, MapPin,
} from 'lucide-react';

const Dashboard = () => {
  const { kpi, borrowingStats, guestStats, overdueBorrowings, loading, refetch } = useShowroomDashboardKPI();
  const [heatmap, setHeatmap] = useState([]);

  useEffect(() => {
    showroomService.getHeatmapData().then((res) => {
      if (res.success) setHeatmap(res.data);
    }).catch(() => {});
  }, []);

  if (loading) return <LoadingSpinner />;

  const movementChartData = [
    { name: 'Dipinjam', value: borrowingStats?.borrowed ?? 0 },
    { name: 'Overdue', value: borrowingStats?.overdue ?? 0 },
    { name: 'Dikembalikan', value: borrowingStats?.returned_this_month ?? 0 },
    { name: 'Release', value: guestStats?.released_this_month ?? 0 },
    { name: 'Menunggu', value: guestStats?.pending_approval ?? 0 },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Showroom Dashboard"
        description="KPI overview sample lifecycle"
        actions={
          <Button onClick={refetch} variant="secondary" size="sm">
            <RefreshCw className="mr-1.5 h-4 w-4" />
            Refresh
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Active Samples" value={kpi?.total_sample ?? '-'} icon={Package} color="brand" />
        <StatCard label="At Showroom" value={kpi?.at_showroom ?? '-'} icon={Package} color="emerald" />
        <StatCard label="Borrowed" value={kpi?.borrowed ?? '-'} icon={ArrowLeftRight} color="amber" />
        <StatCard label="Released" value={kpi?.released_this_month ?? '-'} icon={Users} color="violet" />
        <StatCard label="Need Restock" value={kpi?.need_restock ?? '-'} icon={AlertTriangle} color="rose" />
        <StatCard label="Overdue" value={kpi?.overdue_borrowing ?? '-'} icon={Clock} color="rose" />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <div className="rounded-lg bg-brand-50 p-2">
              <ArrowLeftRight className="h-4 w-4 text-brand-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-700">Peminjaman</h3>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Dipinjam</span>
              <span className="text-sm font-semibold text-slate-900">{borrowingStats?.borrowed ?? 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Overdue</span>
              <span className="text-sm font-semibold text-rose-600">{borrowingStats?.overdue ?? 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Dikembalikan (bulan ini)</span>
              <span className="text-sm font-semibold text-emerald-600">{borrowingStats?.returned_this_month ?? 0}</span>
            </div>
          </div>
        </Card>

        <Card className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <div className="rounded-lg bg-violet-50 p-2">
              <Users className="h-4 w-4 text-violet-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-700">Tamu</h3>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Menunggu Persetujuan</span>
              <span className="text-sm font-semibold text-amber-600">{guestStats?.pending_approval ?? 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Released (bulan ini)</span>
              <span className="text-sm font-semibold text-slate-900">{guestStats?.released_this_month ?? 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-500">Total Tamu</span>
              <span className="text-sm font-semibold text-slate-900">{guestStats?.total_guests ?? 0}</span>
            </div>
          </div>
        </Card>

        <Card className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <div className="rounded-lg bg-rose-50 p-2">
              <Clock className="h-4 w-4 text-rose-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-700">Peminjaman Overdue</h3>
          </div>
          {overdueBorrowings?.length > 0 ? (
            <div className="space-y-2">
              {overdueBorrowings.slice(0, 5).map((b) => (
                <div key={b.id} className="flex items-center justify-between border-b border-slate-100 py-2 last:border-0">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-slate-900">{b.product?.display_name}</p>
                    <p className="text-xs text-slate-500">{b.borrower_name} &middot; {b.quantity} pcs</p>
                  </div>
                  <Badge variant="danger" size="sm">{formatDate(b.expected_return_date)}</Badge>
                </div>
              ))}
            </div>
          ) : (
            <p className="py-4 text-center text-sm text-slate-400">Tidak ada overdue</p>
          )}
        </Card>
      </div>

      <Card className="p-5">
        <div className="mb-4 flex items-center gap-2">
          <div className="rounded-lg bg-brand-50 p-2">
            <TrendingUp className="h-4 w-4 text-brand-600" />
          </div>
          <h3 className="text-sm font-semibold text-slate-700">Aktivitas Overview</h3>
        </div>
        <BarChart data={movementChartData} height={200} />
      </Card>

      {heatmap.length > 0 && (
        <Card className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <div className="rounded-lg bg-emerald-50 p-2">
              <MapPin className="h-4 w-4 text-emerald-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-700">Stock per Lokasi</h3>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {heatmap.map((loc) => {
              const maxQty = Math.max(...heatmap.map(h => h.total), 1);
              const intensity = Math.round((loc.total / maxQty) * 100);
              const bg = intensity > 80 ? 'bg-red-100 border-red-300' :
                         intensity > 50 ? 'bg-amber-100 border-amber-300' :
                         intensity > 20 ? 'bg-emerald-100 border-emerald-300' :
                         'bg-slate-50 border-slate-200';
              return (
                <div key={loc.location_id} className={`rounded-lg border p-3 text-center ${bg}`}>
                  <p className="text-lg font-bold text-slate-800">{loc.total}</p>
                  <p className="text-xs font-medium text-slate-600 truncate">{loc.location_name}</p>
                  <p className="text-[10px] text-slate-400">{loc.products} produk</p>
                </div>
              );
            })}
          </div>
        </Card>
      )}
    </div>
  );
};

export default Dashboard;
