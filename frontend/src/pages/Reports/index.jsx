import React, { useState, useEffect } from 'react';
import PageHeader from '../../components/common/PageHeader';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import Card from '../../components/common/Card';
import { FileText, Calendar, TrendingUp } from 'lucide-react';

import ReportPeriodSelector from './components/ReportPeriodSelector';
import ReportFilter from './components/ReportFilter';
import ExportButton from './components/ExportButton';
import ReportSummary from './components/ReportSummary';
import ReportTable from './components/ReportTable';

import { useReports } from '../../hooks/useReports';

const Reports = () => {
  const [activePeriod, setActivePeriod] = useState('daily');
  const [filters, setFilters] = useState({});
  const { data, loading, refetch } = useReports();

  const normalizeFilters = (rawFilters) => {
    const cleaned = {};
    if (activePeriod === 'daily' && rawFilters.date) cleaned.date = rawFilters.date;
    if (activePeriod === 'weekly' && rawFilters.date) cleaned.date = rawFilters.date;
    if (activePeriod === 'monthly') {
      if (rawFilters.month) cleaned.month = rawFilters.month;
      if (rawFilters.year) cleaned.year = rawFilters.year;
    }
    if (rawFilters.user_id) cleaned.user_id = rawFilters.user_id;
    if (rawFilters.category_id) cleaned.category_id = rawFilters.category_id;
    if (rawFilters.status) cleaned.status = rawFilters.status;
    if (rawFilters.division) cleaned.division = rawFilters.division;
    return cleaned;
  };

  useEffect(() => {
    const params = { type: activePeriod, ...normalizeFilters(filters) };
    refetch(params);
  }, [activePeriod, filters, refetch]);

  // Format period label for display
  const getPeriodLabel = () => {
    const now = new Date();
    switch (activePeriod) {
      case 'daily':
        return now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
      case 'weekly':
        return `Week of ${now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
      case 'monthly':
        return now.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      default:
        return '';
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(normalizeFilters(newFilters));
  };

  return (
    <div>
      <PageHeader 
        title="Analytics & Reports" 
        description="Auto-generated reports from studio work activities."
        action={<ExportButton activePeriod={activePeriod} filters={filters} />}
      />

      <div className="space-y-6">
        {/* Controls */}
        <Card className="overflow-hidden">
          <div className="h-1 bg-gradient-to-r from-brand-500 via-brand-400 to-indigo-400"></div>
          
          <div className="p-4 sm:p-6">
            <div className="flex flex-col gap-5">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600">
                    <Calendar size={20} />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">Report Period</h3>
                    <p className="text-xs text-slate-500 mt-0.5">{getPeriodLabel()}</p>
                  </div>
                </div>
                <ReportPeriodSelector activePeriod={activePeriod} onChange={setActivePeriod} />
              </div>

              <div className="border-t border-slate-100"></div>

              <ReportFilter activePeriod={activePeriod} onChange={handleFilterChange} />
            </div>
          </div>
        </Card>

        {/* Summary */}
        <section>
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={18} className="text-slate-400" />
            <h3 className="text-sm font-semibold text-slate-900 uppercase tracking-wider">Summary Overview</h3>
          </div>
          <ReportSummary summary={data?.summary || {}} />
        </section>

        {/* Table */}
        <section>
          <Card className="overflow-hidden">
            <div className="px-4 sm:px-6 py-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 text-slate-500">
                  <FileText size={18} />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-slate-900">Work Activities Detail</h3>
                  <p className="text-xs text-slate-500">{data?.summary?.total_activity || 0} record(s) found</p>
                </div>
              </div>
              {data?.activities && data.activities.length > 0 && (
                <span className="inline-flex items-center rounded-full bg-brand-50 px-3 py-1 text-xs font-medium text-brand-700 ring-1 ring-inset ring-brand-600/10 capitalize">
                  {activePeriod} Report
                </span>
              )}
            </div>
            <div className="p-0">
              <ReportTable data={data?.activities || []} isLoading={loading} />
            </div>
          </Card>
        </section>
      </div>
    </div>
  );
};

export default Reports;
