import React from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import Card from '../../../components/common/Card';

const AnalyticsChart = ({ type = 'bar', title, subtitle, data, dataKeys = [] }) => {
  const renderChart = () => {
    const commonProps = {
      data,
      margin: { top: 10, right: 10, left: -20, bottom: 0 },
    };

    const colors = ['#6366f1', '#cbd5e1', '#38bdf8', '#fbbf24'];

    switch (type) {
      case 'pie':
        const pieColors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#ec4899'];
        return (
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
              ))}
            </Pie>
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '12px', paddingTop: '20px' }} />
          </PieChart>
        );
      case 'line':
        return (
          <LineChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '12px', paddingTop: '20px' }} />
            {dataKeys.map((key, i) => (
              <Line key={key} type="monotone" dataKey={key} stroke={colors[i % colors.length]} strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
            ))}
          </LineChart>
        );
      case 'area':
        return (
          <AreaChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
            <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '12px', paddingTop: '20px' }} />
            {dataKeys.map((key, i) => (
              <Area key={key} type="monotone" dataKey={key} fill={colors[i % colors.length]} stroke={colors[i % colors.length]} fillOpacity={0.3} />
            ))}
          </AreaChart>
        );
      case 'bar':
      default:
        return (
          <BarChart {...commonProps}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
            <Tooltip cursor={{ fill: '#f8fafc' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: '12px', paddingTop: '20px' }} />
            {dataKeys.map((key, i) => (
              <Bar key={key} dataKey={key} fill={colors[i % colors.length]} radius={[4, 4, 0, 0]} maxBarSize={50} />
            ))}
          </BarChart>
        );
    }
  };

  return (
    <Card className="h-full flex flex-col p-4 sm:p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
        {subtitle && <p className="text-sm text-slate-500">{subtitle}</p>}
      </div>
      <div className="flex-1 w-full min-h-[220px] sm:min-h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          {renderChart()}
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

export default AnalyticsChart;
