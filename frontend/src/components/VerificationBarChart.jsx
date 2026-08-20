import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from 'recharts';
import { useTheme } from '../context/useTheme';

function CustomBarTooltip({ active, payload }) {
  if (active && payload && payload.length) {
    const item = payload[0].payload;
    return (
      <div className="bg-slate-900 dark:bg-slate-800 text-white text-xs px-3.5 py-2.5 rounded-lg shadow-xl border border-slate-700">
        <div className="font-semibold text-slate-200">{item.name}</div>
        <div className="mt-1 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.fill }} />
          <span className="text-slate-300">Documents:</span>
          <span className="font-bold text-white">{item.count}</span>
        </div>
        {item.description && (
          <div className="text-[10px] text-slate-400 mt-0.5">{item.description}</div>
        )}
      </div>
    );
  }
  return null;
}

export default function VerificationBarChart({ data = [] }) {
  const { isDark } = useTheme();

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-xs flex flex-col justify-between transition-colors duration-200">
      <div className="flex items-center justify-between gap-1 mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
            Document Verification Status
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Current triage across inspected rural road packages
          </p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 16, left: -20, bottom: 0 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={isDark ? '#1e293b' : '#f1f5f9'}
              vertical={false}
            />
            <XAxis
              dataKey="name"
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
            <Tooltip content={<CustomBarTooltip />} />
            <Bar dataKey="count" radius={[6, 6, 0, 0]} maxBarSize={56}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 grid grid-cols-3 gap-2 text-center text-[11px]">
        <div>
          <div className="font-bold text-[#3A801C] dark:text-[#99CA84] text-sm">114</div>
          <div className="text-slate-500 dark:text-slate-400 font-medium">Verified</div>
        </div>
        <div>
          <div className="font-bold text-[#D4A700] dark:text-[#FFF200] text-sm">14</div>
          <div className="text-slate-500 dark:text-slate-400 font-medium">Discrepant</div>
        </div>
        <div>
          <div className="font-bold text-[#53B7E8] text-sm">6</div>
          <div className="text-slate-500 dark:text-slate-400 font-medium">Pending</div>
        </div>
      </div>
    </div>
  );
}
