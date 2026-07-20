import React from 'react';
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

const COLORS = ['#6366f1', '#818cf8', '#a5b4fc', '#c7d2fe', '#4f46e5', '#4338ca'];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-slate-200 bg-white px-3 py-2 shadow-lg">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      {payload.map((entry, i) => (
        <p key={i} className="text-sm font-semibold text-slate-900">
          {entry.name}: {entry.value}
        </p>
      ))}
    </div>
  );
};

const BarChart = ({
  data,
  dataKey = 'value',
  nameKey = 'name',
  label,
  height = 250,
  showGrid = true,
  colors,
  className = '',
}) => {
  if (!data?.length) {
    return (
      <div className={`flex items-center justify-center text-sm text-slate-400 ${className}`} style={{ height }}>
        No data available
      </div>
    );
  }

  const barColors = colors || COLORS;

  return (
    <div className={className}>
      {label && (
        <p className="mb-3 text-sm font-semibold text-slate-700">{label}</p>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart data={data} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
          {showGrid && (
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
          )}
          <XAxis
            dataKey={nameKey}
            tick={{ fontSize: 12, fill: '#64748b' }}
            axisLine={{ stroke: '#e2e8f0' }}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 12, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(99, 102, 241, 0.05)' }} />
          <Bar dataKey={dataKey} radius={[4, 4, 0, 0]} maxBarSize={48}>
            {data.map((_, index) => (
              <Cell key={index} fill={barColors[index % barColors.length]} />
            ))}
          </Bar>
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChart;
