import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import { Download, Users, CheckCircle, Package, Clock, Timer, Filter } from 'lucide-react';
import LoadingSpinner from '../../components/common/LoadingSpinner';

import DashboardSection from './components/DashboardSection';
import StatWidget from './components/StatWidget';
import AnalyticsChart from './components/AnalyticsChart';
import RecentActivities from './components/RecentActivities';
import QuickSummary from './components/QuickSummary';
import CurrentStudioActivity from './components/CurrentStudioActivity';
import StudioStatus from './components/StudioStatus';

import { useDashboard } from '../../hooks/useDashboard';

const Dashboard = () => {
  const [daysFilter, setDaysFilter] = useState(7);
  const { metrics, loading, error } = useDashboard(daysFilter);

  if (loading && !metrics) {
    return (
      <div className="flex justify-center items-center h-full min-h-[400px]">
        <LoadingSpinner size="lg" text="Loading dashboard..." />
      </div>
    );
  }

  const kpi = metrics?.kpi || {};
  const studioStatus = metrics?.studio_status || {};
  const currentActivity = metrics?.current_activity || [];
  const charts = metrics?.charts || { volume: [], category: [] };
  const recentActivity = metrics?.recent_activity || [];
  const summary = metrics?.summary || {};

  const dashboardStats = [
    { title: "Active Workers", value: kpi.active_workers?.toString() || "0", icon: Users, color: "emerald", subtitle: "Working right now" },
    { title: "Completed Tasks", value: kpi.completed_tasks_today?.toString() || "0", icon: CheckCircle, color: "brand", subtitle: "Today" },
    { title: "Assets Out", value: kpi.assets_out?.toString() || "0", icon: Package, color: "amber", subtitle: "Borrowed" },
    { title: "Working Hours", value: kpi.current_working_hours || "0", icon: Clock, color: "blue", subtitle: "Total elapsed today" },
    { title: "Avg Completion", value: kpi.average_completion_time || "0", icon: Timer, color: "purple", subtitle: "Time per task" }
  ];

  return (
    <div className="space-y-6 pb-10">
      <PageHeader 
        title="Dashboard Overview" 
        description="Real-time monitoring of Creative Studio activities."
        action={
          <div className="flex gap-2 sm:gap-3 items-center">
            <select 
              value={daysFilter} 
              onChange={(e) => setDaysFilter(Number(e.target.value))}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-white"
            >
              <option value={7}>7 Hari</option>
              <option value={30}>30 Hari</option>
              <option value={90}>90 Hari</option>
            </select>
          </div>
        }
      />

      <StudioStatus data={studioStatus} />
      
      {/* --------------------------------- KPI Cards --------------------------------- */}
      <DashboardSection>
        <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:gap-6 lg:grid-cols-5">
          {dashboardStats.map((stat, i) => (
            <StatWidget
              key={i}
              title={stat.title}
              value={stat.value}
              subtitle={stat.subtitle}
              icon={stat.icon}
              color={stat.color}
            />
          ))}
        </div>
      </DashboardSection>

      {/* --------------------------------- Current Studio Activity --------------------------------- */}
      <DashboardSection title="Current Studio Activity" subtitle="Who is working right now?">
        <CurrentStudioActivity data={currentActivity} />
      </DashboardSection>
      
      {/* --------------------------------- Analytics --------------------------------- */}
      <DashboardSection title="Activity Analytics" subtitle={`Last ${daysFilter} days`}>
        <div className="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-2">
          <AnalyticsChart 
            type="bar" 
            title="Volume Aktivitas" 
            data={charts.volume}
            dataKeys={['completed']}
          />
          <AnalyticsChart 
            type="pie" 
            title="Kategori Aktivitas" 
            data={charts.category}
          />
        </div>
      </DashboardSection>

      {/* --------------------------------- Activities & Summary --------------------------------- */}
      <DashboardSection>
        <div className="grid grid-cols-1 gap-4 sm:gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <RecentActivities data={recentActivity} />
          </div>
          <div className="lg:col-span-1 space-y-6">
            <QuickSummary data={summary} />
          </div>
        </div>
      </DashboardSection>
    </div>
  );
};

export default Dashboard;
