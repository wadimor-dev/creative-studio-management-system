import React from 'react';
import { CheckCircle, Clock, Timer, Box } from 'lucide-react';
import Card from '../../../components/common/Card';

const SummaryCard = ({ title, value, icon: Icon, colorClass, delay }) => (
  <Card className={`animate-fade-in-up border-none shadow-sm flex items-center p-4`} style={{ animationDelay: `${delay}ms` }}>
    <div className={`p-3 rounded-xl mr-4 ${colorClass}`}>
      <Icon size={24} />
    </div>
    <div>
      <p className="text-sm font-medium text-slate-500">{title}</p>
      <h3 className="text-2xl font-bold text-slate-800">{value}</h3>
    </div>
  </Card>
);

const ReportSummary = ({ summary }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <SummaryCard 
        title="Completed Tasks" 
        value={summary?.completed || 0} 
        icon={CheckCircle} 
        colorClass="bg-green-100 text-green-600"
        delay={100}
      />
      <SummaryCard 
        title="Working Hours" 
        value={summary?.total_duration_human || '0 Menit'} 
        icon={Clock} 
        colorClass="bg-blue-100 text-blue-600"
        delay={200}
      />
      <SummaryCard 
        title="Total Evidence" 
        value={summary?.total_evidence || 0} 
        icon={Timer} 
        colorClass="bg-purple-100 text-purple-600"
        delay={300}
      />
      <SummaryCard 
        title="Assets Used" 
        value={summary?.total_assets || 0} 
        icon={Box} 
        colorClass="bg-orange-100 text-orange-600"
        delay={400}
      />
    </div>
  );
};

export default ReportSummary;
