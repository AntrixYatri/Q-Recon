import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import { useTheme } from '../context/useTheme';

function CustomTooltip({ active, payload, label }) {
  if (active && payload && payload.length) {
    return (
      <div className="bg-slate-900 dark:bg-slate-800 text-white text-xs px-3.5 py-2.5 rounded-lg shadow-xl border border-slate-700">
        <div className="font-semibold text-slate-200">{label}</div>
        <div className="mt-1 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#53B7E8]" />
          <span className="text-slate-300">Verified:</span>
          <span className="font-bold text-white">{payload[0].value} documents</span>
        </div>
      </div>
    );
  }
  return null;
}

export default function VerificationLineChart({ data = [] }) {
  const { isDark } = useTheme();

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-xs transition-colors duration-200">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-900 dark:text-white">Verification Activity</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Daily volume of cross-verified road construction records
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
          <span className="inline-flex items-center gap-1.5 font-medium text-slate-700 dark:text-slate-300">
            <span className="w-2.5 h-2.5 rounded-full bg-[#53B7E8]" />
            Verified Records
          </span>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 16, left: -20, bottom: 0 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={isDark ? '#1e293b' : '#f1f5f9'}
              vertical={false}
            />
            <XAxis
              dataKey="day"
              tickLine={false}
              axisLine={{ stroke: isDark ? '#334155' : '#e2e8f0' }}
              tick={{ fill: isDark ? '#94a3b8' : '#64748b', fontSize: 12 }}
            />
            <YAxis
              tickLine={false}
              axisLine={false}
              tick={{ fill: isDark ? '#94a3b8' : '#64748b', fontSize: 12 }}
              allowDecimals={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="verified"
              stroke="#53B7E8"
              strokeWidth={3}
              dot={{ fill: '#53B7E8', r: 4, strokeWidth: 2, stroke: isDark ? '#0f172a' : '#ffffff' }}
              activeDot={{ fill: '#3A801C', r: 6, stroke: isDark ? '#0f172a' : '#ffffff', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
