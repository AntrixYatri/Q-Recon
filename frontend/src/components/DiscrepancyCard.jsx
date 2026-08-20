import React from 'react';
import { AlertTriangle, ArrowRight } from 'lucide-react';
import StatusBadge from './StatusBadge';
import { Link } from 'react-router-dom';

export default function DiscrepancyCard({
  id = '1',
  itemCode = 'QC-AGG-04',
  title = 'Aggregate Gradation Inconsistency',
  description = 'QCR reported 20mm aggregate passing rate of 94%, whereas Laboratory Datasheet recorded 81%.',
  severity = 'critical',
  confidence = 94,
  sources = ['QCR Register', 'Lab Test Sheet'],
  roadName = 'PMGSY Road - Package RJ-04-102',
  className = '',
}) {
  return (
    <div
      className={`bg-white dark:bg-slate-900 rounded-xl border border-slate-200/90 dark:border-slate-800 p-5 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition-all ${className}`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3">
          <div
            className={`p-2 rounded-lg mt-0.5 ${
              severity === 'critical'
                ? 'bg-rose-50 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400'
                : severity === 'warning'
                ? 'bg-amber-50 dark:bg-amber-950/60 text-[#D4A700] dark:text-[#FFF200]'
                : 'bg-sky-50 dark:bg-sky-950/60 text-[#53B7E8]'
            }`}
          >
            <AlertTriangle className="w-5 h-5" />
          </div>

          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-semibold px-2 py-0.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded border border-slate-200 dark:border-slate-700">
                {itemCode}
              </span>
              <StatusBadge status={severity} label={severity.toUpperCase()} />
              <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                AI Confidence: <strong className="text-slate-900 dark:text-white">{confidence}%</strong>
              </span>
            </div>

            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mt-1.5">{title}</h4>
            <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">{description}</p>

            <div className="mt-2.5 text-[11px] text-slate-500 dark:text-slate-400">
              <span className="font-medium text-slate-600 dark:text-slate-300">Location:</span> {roadName}
            </div>

            <div className="mt-2 flex items-center gap-2 text-[11px] text-slate-500 dark:text-slate-400">
              <span className="font-medium text-slate-600 dark:text-slate-300">Cross-Referenced:</span>
              {sources.map((src, idx) => (
                <span
                  key={idx}
                  className="px-2 py-0.5 bg-slate-50 dark:bg-slate-800 rounded border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300"
                >
                  {src}
                </span>
              ))}
            </div>
          </div>
        </div>

        <Link
          to={`/analysis/discrepancy/${id}`}
          className="shrink-0 inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-[#53B7E8] hover:bg-[#3aa3d8] text-white rounded-lg text-xs font-semibold transition shadow-xs cursor-pointer"
        >
          <span>Inspect</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
}
