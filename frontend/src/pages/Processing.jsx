import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Loader2, ArrowRight, ArrowLeft } from 'lucide-react';

export default function Processing() {
  const location = useLocation();
  const packageNumber = location.state?.packageNumber || 'Pending Package';
  const stateScheme = location.state?.stateScheme || 'PMGSY Scheme';

  // TODO: Connect to backend API for polling analysis status
  // Example integration:
  // useEffect(() => {
  //   const interval = setInterval(async () => {
  //     const status = await analysisService.getAnalysisStatus(analysisId);
  //     if (status?.completed) {
  //       navigate('/analysis/results', { state: { analysisId } });
  //     }
  //   }, 3000);
  //   return () => clearInterval(interval);
  // }, [analysisId]);

  return (
    <div className="space-y-6 max-w-3xl mx-auto py-6 sm:py-10">
      {/* Back Link */}
      <div className="flex items-center gap-2">
        <Link
          to="/analysis/new"
          className="inline-flex items-center gap-1 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>New Analysis</span>
        </Link>
        <span className="text-slate-300 dark:text-slate-700">/</span>
        <span className="text-xs text-slate-500 dark:text-slate-400 font-mono truncate">
          {packageNumber}
        </span>
      </div>

      {/* Page Header */}
      <div className="text-center space-y-1">
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          Analysis in Progress
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto">
          Q-Recon is processing and cross-examining uploaded documents for discrepancies against IRC standards.
        </p>
      </div>

      {/* Processing State Card */}
      <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-8 shadow-xs text-center space-y-6 transition-colors duration-200">
        {/* Animated Spinner Icon */}
        <div className="flex justify-center">
          <div className="w-16 h-16 rounded-full bg-[#C7EAFC]/50 dark:bg-sky-950/60 border border-[#53B7E8]/40 flex items-center justify-center text-[#53B7E8]">
            <Loader2 className="w-8 h-8 animate-spin" />
          </div>
        </div>

        <div>
          <h2 className="text-base font-semibold text-slate-900 dark:text-white">
            Tri-Source Cross-Examination
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">
            Comparing QM E-Forms, Laboratory Datasheets, and Quality Control Registers for {packageNumber}.
          </p>
        </div>

        {/* Informational Scope Checklist (No fake progress/timers) */}
        <div className="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4 border border-slate-200 dark:border-slate-700/60 max-w-md mx-auto text-left text-xs space-y-2.5">
          <div className="flex items-center gap-2 text-slate-700 dark:text-slate-300 font-medium">
            <span className="w-2 h-2 rounded-full bg-[#53B7E8] animate-pulse" />
            <span>Target Package: <strong className="font-mono">{packageNumber}</strong></span>
          </div>
          <div className="text-[11px] text-slate-500 dark:text-slate-400 pl-4">
            Scheme: {stateScheme}
          </div>
          <div className="text-[11px] text-slate-500 dark:text-slate-400 pl-4 border-t border-slate-200/60 dark:border-slate-700 pt-2">
            Verification includes: Sieve Gradation Analysis, Compaction Density Ratios, Bitumen Binder Ratios, and Test Date Log Sequence.
          </div>
        </div>

        {/* Backend Integration Placeholder Callout */}
        <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3">
          <span className="text-[11px] text-slate-400 dark:text-slate-500 font-mono">
            // TODO: Awaiting backend processing completion
          </span>

          <Link
            to="/analysis/results"
            className="inline-flex items-center gap-2 px-5 py-2 bg-[#53B7E8] hover:bg-[#3aa3d8] text-white rounded-lg text-xs font-semibold transition shadow-xs cursor-pointer"
          >
            <span>Proceed to Results Page</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
