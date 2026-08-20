import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, FileText, BookOpen, Inbox } from 'lucide-react';
import StatusBadge from '../components/StatusBadge';

export default function DiscrepancyDetails() {
  const { id } = useParams();

  // TODO: Connect to backend API
  // Example:
  // const [discrepancy, setDiscrepancy] = useState(null);
  // useEffect(() => {
  //   async function fetchDetails() {
  //     const data = await analysisService.getDiscrepancyDetails(analysisId, id);
  //     setDiscrepancy(data);
  //   }
  //   fetchDetails();
  // }, [analysisId, id]);

  const discrepancy = null; // No hardcoded fake data

  return (
    <div className="space-y-6">
      {/* Navigation Breadcrumb */}
      <div className="flex items-center gap-2">
        <Link
          to="/analysis/results"
          className="inline-flex items-center gap-1 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Analysis Results</span>
        </Link>
        <span className="text-slate-300 dark:text-slate-700">/</span>
        <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
          Discrepancy #{id || '—'}
        </span>
      </div>

      {/* Main Structural Details Layout */}
      <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-xs space-y-6 transition-colors duration-200">
        {/* Header Placeholders */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-6">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-semibold px-2 py-0.5 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded border border-slate-200 dark:border-slate-700">
                {discrepancy ? discrepancy.itemCode : 'FIELD-CODE'}
              </span>
              <StatusBadge
                status={discrepancy ? discrepancy.severity : 'info'}
                label={discrepancy ? discrepancy.severity.toUpperCase() : 'PENDING'}
              />
              <span className="text-xs font-mono text-slate-500 dark:text-slate-400">
                ID: {id || '—'}
              </span>
            </div>

            <h1 className="text-xl font-bold text-slate-900 dark:text-white mt-2">
              {discrepancy ? discrepancy.title : `Discrepancy Record #${id || '—'}`}
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              {discrepancy ? discrepancy.roadLocation : 'Awaiting cross-examination data from backend engine.'}
            </p>
          </div>

          <div className="px-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-center shrink-0">
            <div className="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400">
              AI Confidence
            </div>
            <div className="text-xl font-bold text-slate-900 dark:text-white">
              {discrepancy ? `${discrepancy.confidence}%` : '—'}
            </div>
          </div>
        </div>

        {/* Empty State / Integration Point when no backend data is provided */}
        {!discrepancy && (
          <div className="py-8 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-xl bg-slate-50/50 dark:bg-slate-900/50">
            <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-400 mx-auto mb-2.5">
              <Inbox className="w-5 h-5" />
            </div>
            <h3 className="text-xs font-semibold text-slate-800 dark:text-slate-200">
              Discrepancy Details Placeholder
            </h3>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 max-w-sm mx-auto mt-1">
              Side-by-side document evidence and AI explanation will populate automatically when the backend API response is provided.
            </p>
            <div className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[11px] font-mono text-slate-600 dark:text-slate-400">
              <span>Target Method:</span>
              <code className="text-[#53B7E8]">analysisService.getDiscrepancyDetails()</code>
            </div>
          </div>
        )}

        {/* Side-by-side Evidence Placeholders (Structural Layout) */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Source 1 Placeholder */}
          <div className="border border-slate-200 dark:border-slate-800 rounded-xl p-5 bg-slate-50/50 dark:bg-slate-900/60 space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#53B7E8]" />
                <h2 className="text-xs font-bold uppercase text-slate-800 dark:text-slate-200">
                  Source A: Quality Control Register (QCR)
                </h2>
              </div>
              <span className="text-[10px] font-mono bg-slate-200 dark:bg-slate-800 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">
                {discrepancy ? discrepancy.sourceA?.page : 'Page / Entry'}
              </span>
            </div>

            <div className="bg-white dark:bg-slate-800/80 p-4 rounded-lg border border-slate-200 dark:border-slate-700 text-xs space-y-2">
              <div className="flex justify-between text-slate-600 dark:text-slate-300">
                <span>Recorded Value:</span>
                <strong className="text-slate-900 dark:text-white font-mono">
                  {discrepancy ? discrepancy.sourceA?.value : '—'}
                </strong>
              </div>
              <div className="flex justify-between text-slate-600 dark:text-slate-300">
                <span>Log Date:</span>
                <span className="font-mono">{discrepancy ? discrepancy.sourceA?.date : '—'}</span>
              </div>
            </div>
          </div>

          {/* Source 2 Placeholder */}
          <div className="border border-slate-200 dark:border-slate-800 rounded-xl p-5 bg-slate-50/50 dark:bg-slate-900/60 space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-rose-500" />
                <h2 className="text-xs font-bold uppercase text-slate-800 dark:text-slate-200">
                  Source B: Laboratory Test Datasheet
                </h2>
              </div>
              <span className="text-[10px] font-mono bg-slate-200 dark:bg-slate-800 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">
                {discrepancy ? discrepancy.sourceB?.page : 'Sheet #'}
              </span>
            </div>

            <div className="bg-white dark:bg-slate-800/80 p-4 rounded-lg border border-slate-200 dark:border-slate-700 text-xs space-y-2">
              <div className="flex justify-between text-slate-600 dark:text-slate-300">
                <span>Recorded Value:</span>
                <strong className="text-slate-900 dark:text-white font-mono">
                  {discrepancy ? discrepancy.sourceB?.value : '—'}
                </strong>
              </div>
              <div className="flex justify-between text-slate-600 dark:text-slate-300">
                <span>Test Date:</span>
                <span className="font-mono">{discrepancy ? discrepancy.sourceB?.date : '—'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* IRC Code Reference / AI Explanation Placeholder */}
        <div className="p-4 bg-slate-900 dark:bg-slate-950 border border-slate-800 text-white rounded-xl text-xs space-y-2">
          <div className="flex items-center gap-2 font-semibold text-[#53B7E8]">
            <BookOpen className="w-4 h-4" />
            <span>IRC Standard Reference & AI Explanation</span>
          </div>
          <p className="text-slate-300 dark:text-slate-400 leading-relaxed">
            {discrepancy
              ? discrepancy.aiExplanation
              : 'Detailed clause compliance analysis, confidence breakdown, and recommendations will display here when connected to the backend inference engine.'}
          </p>
        </div>
      </div>
    </div>
  );
}
