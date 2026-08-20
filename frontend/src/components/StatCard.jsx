import React from 'react';

export default function StatCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendDirection = 'neutral',
  accentColor,
  className = '',
}) {
  return (
    <div
      className={`bg-white dark:bg-slate-900 rounded-xl border border-slate-200/90 dark:border-slate-800 p-5 shadow-xs transition-all hover:border-slate-300 dark:hover:border-slate-700 hover:shadow-2xs ${className}`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          {title}
        </span>
        {Icon && (
          <div
            className="p-2 rounded-lg border text-slate-700 dark:text-slate-200 bg-slate-50 dark:bg-slate-800/80 border-slate-100 dark:border-slate-700/60"
            style={accentColor ? { color: accentColor, backgroundColor: `${accentColor}15` } : {}}
          >
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="mt-3">
        <div className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          {value}
        </div>
        {(subtitle || trend) && (
          <div className="mt-1.5 flex items-center gap-2 text-xs">
            {trend && (
              <span
                className={`font-semibold ${
                  trendDirection === 'up'
                    ? 'text-[#3A801C] dark:text-[#99CA84]'
                    : trendDirection === 'warning'
                    ? 'text-[#D4A700] dark:text-[#FFF200]'
                    : trendDirection === 'down'
                    ? 'text-rose-600 dark:text-rose-400'
                    : 'text-slate-600 dark:text-slate-300'
                }`}
              >
                {trend}
              </span>
            )}
            {subtitle && <span className="text-slate-500 dark:text-slate-400">{subtitle}</span>}
          </div>
        )}
      </div>
    </div>
  );
}
