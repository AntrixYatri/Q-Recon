import React from 'react';
import { Link } from 'react-router-dom';
import { FolderArchive, PlusCircle, ArrowLeft } from 'lucide-react';

export default function Records() {
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
              Audit Archive
            </span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            Records
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            View and manage previously analyzed road quality-control records.
          </p>
        </div>

        <Link
          to="/analysis/new"
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#53B7E8] hover:bg-[#3aa3d8] text-white rounded-lg text-xs font-semibold transition shadow-xs cursor-pointer"
        >
          <PlusCircle className="w-4 h-4" />
          <span>New Analysis</span>
        </Link>
      </div>

      {/* Clean Structural Empty State */}
      <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-12 text-center shadow-xs transition-colors duration-200">
        <div className="w-14 h-14 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-400 dark:text-slate-500 mx-auto mb-4">
          <FolderArchive className="w-7 h-7" />
        </div>
        <h2 className="text-base font-semibold text-slate-800 dark:text-slate-200">
          No records available yet.
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-md mx-auto">
          Analyzed records will appear here once the backend is connected.
        </p>

        <div className="mt-6 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-xs font-mono text-slate-600 dark:text-slate-400">
          <span>Backend Target:</span>
          <code className="text-[#53B7E8]">GET /api/records</code>
        </div>
      </div>
    </div>
  );
}
