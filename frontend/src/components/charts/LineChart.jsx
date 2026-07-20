import React from 'react';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

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

const LineChart = ({
  data,
  dataKey = 'value',
  nameKey = 'name',
  label,
  height = 250,
  color = '#6366f1',
  showGrid = true,
  className = '',
}) => {
  if (!data?.length) {
    return (
      <div className={`flex items-center justify-center text-sm text-slate-400 ${className}`} style={{ height }}>
        No data available
      </div>
    );
  }

  return (
    <div className={className}>
      {label && (
        <p className="mb-3 text-sm font-semibold text-slate-700">{label}</p>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsLineChart data={data} margin={{ top: 5, right: 10, left: -10, bottom: 5 }}>
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
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey={dataKey}
            stroke={color}
            strokeWidth={2}
            dot={{ fill: color, r: 4, strokeWidth: 2, stroke: '#fff' }}
            activeDot={{ r: 6, strokeWidth: 2, stroke: '#fff' }}
          />
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LineChart;
