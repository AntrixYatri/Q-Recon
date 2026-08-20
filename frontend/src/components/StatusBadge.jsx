import React from 'react';

const badgeStyles = {
  critical: 'bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-900/60 ring-rose-600/10',
  warning: 'bg-amber-50 dark:bg-amber-950/40 text-[#8c6d00] dark:text-[#FFF200] border-[#FFF200]/80 dark:border-amber-700/60 ring-amber-500/20',
  discrepant: 'bg-amber-50 dark:bg-amber-950/40 text-[#8c6d00] dark:text-[#FFF200] border-[#FFF200]/80 dark:border-amber-700/60 ring-amber-500/20',
  verified: 'bg-emerald-50 dark:bg-emerald-950/40 text-[#3A801C] dark:text-[#99CA84] border-[#99CA84]/60 dark:border-emerald-800/60 ring-emerald-600/10',
  passed: 'bg-emerald-50 dark:bg-emerald-950/40 text-[#3A801C] dark:text-[#99CA84] border-[#99CA84]/60 dark:border-emerald-800/60 ring-emerald-600/10',
  pending: 'bg-sky-50 dark:bg-sky-950/40 text-[#0c4a6e] dark:text-[#53B7E8] border-[#C7EAFC] dark:border-sky-800/60 ring-sky-500/10',
  'under review': 'bg-sky-50 dark:bg-sky-950/40 text-[#0c4a6e] dark:text-[#53B7E8] border-[#C7EAFC] dark:border-sky-800/60 ring-sky-500/10',
  info: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700 ring-slate-600/10',
};

const dotStyles = {
  critical: 'bg-rose-500',
  warning: 'bg-[#D4A700] dark:bg-[#FFF200]',
  discrepant: 'bg-[#D4A700] dark:bg-[#FFF200]',
  verified: 'bg-[#3A801C] dark:bg-[#99CA84]',
  passed: 'bg-[#3A801C] dark:bg-[#99CA84]',
  pending: 'bg-[#53B7E8]',
  'under review': 'bg-[#53B7E8]',
  info: 'bg-slate-400',
};

export default function StatusBadge({ status = 'info', label, showDot = true, className = '' }) {
  const normalizedStatus = status.toLowerCase();
  const style = badgeStyles[normalizedStatus] || badgeStyles.info;
  const dot = dotStyles[normalizedStatus] || dotStyles.info;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-xs font-medium border ring-1 ring-inset ${style} ${className}`}
    >
      {showDot && <span className={`w-1.5 h-1.5 rounded-full ${dot}`} />}
      {label || status}
    </span>
  );
}
