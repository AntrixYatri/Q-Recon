import React from 'react';
import { Link } from 'react-router-dom';
import {
  PlusCircle,
  FileSpreadsheet,
  AlertTriangle,
  CheckCircle,
  Download,
  ArrowLeft,
  Inbox,
} from 'lucide-react';
import StatCard from '../components/StatCard';

export default function Results() {
  // TODO: Connect to backend API
  // Example:
  // const [results, setResults] = useState(null);
  // useEffect(() => {
  //   async function fetchResults() {
  //     const data = await analysisService.getAnalysisResults(analysisId);
  //     setResults(data);
  //   }
  //   fetchResults();
  // }, [analysisId]);

  const results = null; // No hardcoded fake data

  return (
    <div className="space-y-6">
      {/* Header & Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link
              to="/dashboard"
              className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 flex items-center gap-1"
            >
              <ArrowLeft className="w-3 h-3" />
              Dashboard
            </Link>
            <span className="text-slate-300 dark:text-slate-700">/</span>
            <span className="text-xs font-mono font-semibold text-[#0c4a6e] dark:text-[#53B7E8] bg-[#C7EAFC]/60 dark:bg-sky-950/60 px-1.5 py-0.5 rounded border border-[#53B7E8]/40">
              Analysis Results
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            Analysis Results
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Tri-source discrepancy report across QM E-Form, Laboratory Datasheets, and QCR Register.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            disabled
            className="inline-flex items-center gap-2 px-3.5 py-2 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs font-semibold text-slate-400 dark:text-slate-500 cursor-not-allowed shadow-2xs"
          >
            <Download className="w-4 h-4" />
            <span>Export Summary</span>
          </button>
          <Link
            to="/analysis/new"
            className="inline-flex items-center gap-2 px-4 py-2 bg-[#53B7E8] hover:bg-[#3aa3d8] text-white rounded-lg text-xs font-semibold transition shadow-xs cursor-pointer"
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Analysis</span>
          </Link>
        </div>
      </div>

      {/* Structural Summary Metric Cards (Placeholders) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Documents Analyzed"
          value={results ? results.documentsCount : '—'}
          subtitle="QM, Datasheets, QCR"
          accentColor="#53B7E8"
          icon={FileSpreadsheet}
        />
        <StatCard
          title="Fields Compared"
          value={results ? results.fieldsCompared : '—'}
          subtitle="Tri-source parameters"
          accentColor="#99CA84"
          icon={CheckCircle}
        />
        <StatCard
          title="Discrepancies Found"
          value={results ? results.discrepancyCount : '—'}
          subtitle="Flagged inconsistencies"
          accentColor="#D4A700"
          icon={AlertTriangle}
        />
        <StatCard
          title="Confidence Score"
          value={results ? results.confidenceScore : '—'}
          subtitle="AI verification rating"
          accentColor="#53B7E8"
          icon={CheckCircle}
        />
      </div>

      {/* Discrepancy List Section (Clean Empty/Placeholder State) */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold text-slate-900 dark:text-white">
            Identified Discrepancies
          </h2>
          <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
            // TODO: GET /api/analysis/:id/results
          </span>
        </div>

        {/* Empty State / Integration Placeholder */}
        <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-12 text-center shadow-xs transition-colors duration-200">
          <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-400 dark:text-slate-500 mx-auto mb-3">
            <Inbox className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
            No Discrepancies Loaded
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">
            Analysis results will appear here once processing is complete and the backend API is connected.
          </p>

          <div className="mt-6 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-mono text-slate-600 dark:text-slate-400">
            <span>Integration Target:</span>
            <code className="text-[#53B7E8]">analysisService.getAnalysisResults()</code>
          </div>
        </div>
      </div>
    </div>
  );
}
