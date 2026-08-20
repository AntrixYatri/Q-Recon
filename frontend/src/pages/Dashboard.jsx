import React from 'react';
import { Link } from 'react-router-dom';
import {
  PlusCircle,
  FileSpreadsheet,
  AlertTriangle,
  CheckCircle2,
  ShieldCheck,
  ArrowRight,
  Filter,
} from 'lucide-react';
import StatCard from '../components/StatCard';
import StatusBadge from '../components/StatusBadge';
import VerificationLineChart from '../components/VerificationLineChart';
import VerificationBarChart from '../components/VerificationBarChart';
import {
  kpiMetrics,
  weeklyActivityData,
  documentStatusData,
  recentVerifications,
} from '../mocks/dashboardData';

export default function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Overview of road quality-control verification and discrepancy detection.
          </p>
        </div>

        <Link
          to="/analysis/new"
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-[#53B7E8] hover:bg-[#3aa3d8] text-white rounded-lg text-sm font-semibold transition shadow-xs cursor-pointer"
        >
          <PlusCircle className="w-4 h-4" />
          <span>New Analysis</span>
        </Link>
      </div>

      {/* 1. Four KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title={kpiMetrics.totalDocuments.label}
          value={kpiMetrics.totalDocuments.value}
          subtitle={kpiMetrics.totalDocuments.subtext}
          trend="+12 this week"
          trendDirection="up"
          accentColor="#53B7E8"
          icon={FileSpreadsheet}
        />
        <StatCard
          title={kpiMetrics.verifiedDocuments.label}
          value={kpiMetrics.verifiedDocuments.value}
          subtitle={kpiMetrics.verifiedDocuments.subtext}
          trend="+8.4% rate"
          trendDirection="up"
          accentColor="#3A801C"
          icon={CheckCircle2}
        />
        <StatCard
          title={kpiMetrics.activeDiscrepancies.label}
          value={kpiMetrics.activeDiscrepancies.value}
          subtitle={kpiMetrics.activeDiscrepancies.subtext}
          trend="3 requires action"
          trendDirection="warning"
          accentColor="#D4A700"
          icon={AlertTriangle}
        />
        <StatCard
          title={kpiMetrics.verificationAccuracy.label}
          value={kpiMetrics.verificationAccuracy.value}
          subtitle={kpiMetrics.verificationAccuracy.subtext}
          trend="Target >95%"
          trendDirection="up"
          accentColor="#99CA84"
          icon={ShieldCheck}
        />
      </div>

      {/* 2. Verification Activity — Line Chart */}
      <VerificationLineChart data={weeklyActivityData} />

      {/* 3. Bar Chart + Recent Verifications Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Document Verification Status Bar Chart */}
        <div className="lg:col-span-1 h-full">
          <VerificationBarChart data={documentStatusData} />
        </div>

        {/* Recent Quality Verifications Table */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-xs transition-colors duration-200">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-white">
                Recent Quality Verifications
              </h2>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Audit logs across PMGSY rural road packages
              </p>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-md border border-slate-200 dark:border-slate-700 transition"
              >
                <Filter className="w-3 h-3 text-slate-400" />
                <span>All Schemes</span>
              </button>
            </div>
          </div>

          <div className="overflow-x-auto mt-2">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 font-semibold uppercase tracking-wider">
                  <th className="py-3 px-2">Package ID</th>
                  <th className="py-3 px-2">Road / Scheme</th>
                  <th className="py-3 px-2">Date</th>
                  <th className="py-3 px-2">Documents</th>
                  <th className="py-3 px-2">Discrepancies</th>
                  <th className="py-3 px-2">Status</th>
                  <th className="py-3 px-2 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
                {recentVerifications.map((item) => (
                  <tr key={item.packageId} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/50 transition">
                    <td className="py-3.5 px-2 font-mono font-medium text-slate-900 dark:text-white">
                      {item.packageId}
                    </td>
                    <td
                      className="py-3.5 px-2 max-w-[200px] truncate font-medium text-slate-800 dark:text-slate-200"
                      title={item.roadScheme}
                    >
                      {item.roadScheme}
                    </td>
                    <td className="py-3.5 px-2 text-slate-500 dark:text-slate-400 font-mono text-[11px] whitespace-nowrap">
                      {item.date}
                    </td>
                    <td className="py-3.5 px-2 text-slate-600 dark:text-slate-400 text-[11px]">
                      {item.documents}
                    </td>
                    <td className="py-3.5 px-2 font-medium">
                      <span
                        className={
                          item.discrepancies.startsWith('0')
                            ? 'text-[#3A801C] dark:text-[#99CA84]'
                            : 'text-[#D4A700] dark:text-[#FFF200]'
                        }
                      >
                        {item.discrepancies}
                      </span>
                    </td>
                    <td className="py-3.5 px-2">
                      <StatusBadge status={item.status} label={item.status} />
                    </td>
                    <td className="py-3.5 px-2 text-right">
                      <Link
                        to="/analysis/results"
                        className="inline-flex items-center gap-1 text-[#0c4a6e] dark:text-[#53B7E8] hover:text-[#53B7E8] dark:hover:text-[#C7EAFC] font-semibold text-xs transition"
                      >
                        <span>View Results</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
