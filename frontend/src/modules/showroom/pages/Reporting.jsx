import React from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Badge from '../../../components/common/Badge';
import Button from '../../../components/common/Button';
import Card from '../../../components/common/Card';
import StatCard from '../../../components/common/StatCard';
import BarChart from '../../../components/charts/BarChart';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import { useShowroomReports } from '../../../hooks/useShowroomV2';
import { TYPE_LABEL, TYPE_VARIANT } from '../constants';
import { Package, ArrowLeftRight, Users, BarChart3, MapPin, RefreshCw, AlertTriangle } from 'lucide-react';

const Reporting = () => {
  const { kpi, movementSummary, stockByLocation, loading, refetch } = useShowroomReports();

  if (loading) return <LoadingSpinner />;

  const movementChartData = (movementSummary || []).map((m) => ({
    name: TYPE_LABEL[m.type] || m.type,
    value: m.total_quantity,
  }));

  const stockChartData = (stockByLocation || []).map((s) => ({
    name: s.location_name,
    value: s.total_quantity,
  }));

  return (
    <div className="space-y-6">
      <PageHeader
        title="Pelaporan"
        description="KPI, ringkasan pergerakan, stok per lokasi"
        actions={
          <Button onClick={refetch} variant="secondary" size="sm">
            <RefreshCw className="mr-1.5 h-4 w-4" />
            Refresh
          </Button>
        }
      />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
        <StatCard label="Active Samples" value={kpi?.total_sample ?? '-'} icon={Package} color="brand" />
        <StatCard label="At Showroom" value={kpi?.at_showroom ?? '-'} icon={MapPin} color="emerald" />
        <StatCard label="Borrowed" value={kpi?.borrowed ?? '-'} icon={ArrowLeftRight} color="amber" />
        <StatCard label="Released" value={kpi?.released_this_month ?? '-'} icon={Users} color="violet" />
        <StatCard label="Need Restock" value={kpi?.need_restock ?? '-'} icon={AlertTriangle} color="rose" />
        <StatCard label="Overdue" value={kpi?.overdue_borrowing ?? '-'} icon={Package} color="rose" />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <div className="rounded-lg bg-brand-50 p-2">
              <BarChart3 className="h-4 w-4 text-brand-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-700">Ringkasan Pergerakan (30 Hari)</h3>
          </div>
          {movementChartData.length > 0 ? (
            <BarChart data={movementChartData} height={220} />
          ) : (
            <EmptyState title="Belum ada data" description="Belum ada data pergerakan" />
          )}
        </Card>

        <Card className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <div className="rounded-lg bg-emerald-50 p-2">
              <MapPin className="h-4 w-4 text-emerald-600" />
            </div>
            <h3 className="text-sm font-semibold text-slate-700">Stok per Lokasi</h3>
          </div>
          {stockChartData.length > 0 ? (
            <BarChart data={stockChartData} height={220} colors={['#10b981', '#34d399', '#6ee7b7', '#a7f3d0']} />
          ) : (
            <EmptyState title="Belum ada data" description="Belum ada data stok" />
          )}
        </Card>
      </div>

      <Card className="p-5">
        <div className="mb-4 flex items-center gap-2">
          <div className="rounded-lg bg-violet-50 p-2">
            <Users className="h-4 w-4 text-violet-600" />
          </div>
          <h3 className="text-sm font-semibold text-slate-700">Detail Pergerakan</h3>
        </div>
        {movementSummary?.length > 0 ? (
          <div className="space-y-3">
            {movementSummary.map((m) => (
              <div key={m.type} className="flex items-center justify-between border-b border-slate-100 pb-2">
                <div className="flex items-center gap-2">
                  <Badge variant={TYPE_VARIANT[m.type] || 'secondary'}>{TYPE_LABEL[m.type] || m.type}</Badge>
                </div>
                <div className="text-right">
                  <span className="text-sm font-semibold text-slate-900">{m.total_quantity} pcs</span>
                  <span className="ml-2 text-xs text-slate-500">({m.count} transaksi)</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <EmptyState title="Belum ada data" description="Belum ada data pergerakan" />
        )}
      </Card>
    </div>
  );
};

export default Reporting;
