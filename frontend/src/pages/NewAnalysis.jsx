import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowRight, ArrowLeft, AlertCircle } from 'lucide-react';
import FileUploader from '../components/FileUploader';
import { analysisService } from '../services/analysisService';

export default function NewAnalysis() {
  const navigate = useNavigate();

  // Form Field States
  const [stateScheme, setStateScheme] = useState('PMGSY Phase-III (Rajasthan)');
  const [packageNumber, setPackageNumber] = useState('');
  const [qmFile, setQmFile] = useState(null);
  const [testDatasheetFile, setTestDatasheetFile] = useState(null);
  const [qcrFile, setQcrFile] = useState(null);

  // Validation State
  const [touched, setTouched] = useState(false);

  // Validation checks
  const isStateValid = Boolean(stateScheme && stateScheme.trim());
  const isPackageValid = Boolean(packageNumber && packageNumber.trim());
  const isQmFileValid = Boolean(qmFile);
  const isDatasheetValid = Boolean(testDatasheetFile);
  const isQcrValid = Boolean(qcrFile);

  const isFormValid =
    isStateValid && isPackageValid && isQmFileValid && isDatasheetValid && isQcrValid;

  const handleStartAnalysis = async (e) => {
    e.preventDefault();
    setTouched(true);

    if (!isFormValid) {
      return;
    }

    // 1. Gather form metadata & selected files in a clean structure
    const payload = {
      stateScheme: stateScheme.trim(),
      packageNumber: packageNumber.trim(),
      qmFile,
      testDatasheetFile,
      qcrFile,
    };

    try {
      // 2. Integration point: Call analysis service
      // TODO: Connect to backend API via analysisService.submitAnalysis
      await analysisService.submitAnalysis(payload);

      // 3. Navigate to Processing page
      navigate('/analysis/processing', {
        state: {
          packageNumber: payload.packageNumber,
          stateScheme: payload.stateScheme,
        },
      });
    } catch (err) {
      console.error('Failed to submit analysis:', err);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Navigation Breadcrumb */}
      <div className="flex items-center gap-2">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-1 text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Dashboard</span>
        </Link>
        <span className="text-slate-300 dark:text-slate-700">/</span>
        <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">
          New Inspection Analysis
        </span>
      </div>

      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          New Quality Analysis
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Upload Quality Control Registers (QCRs), Lab Test Datasheets, and QM E-Forms for
          tri-source cross-verification.
        </p>
      </div>

      {/* Form Container */}
      <form onSubmit={handleStartAnalysis} className="space-y-6">
        {/* Section 1: Road & Package Details */}
        <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-xs space-y-6 transition-colors duration-200">
          <div className="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h2 className="text-base font-semibold text-slate-900 dark:text-white">
              1. Road & Package Details
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Select rural road work metadata and package identifier.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                State / Scheme <span className="text-rose-500">*</span>
              </label>
              <select
                value={stateScheme}
                onChange={(e) => setStateScheme(e.target.value)}
                className="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-[#53B7E8]"
              >
                <option value="PMGSY Phase-III (Rajasthan)">PMGSY Phase-III (Rajasthan)</option>
                <option value="PMGSY Phase-III (Uttar Pradesh)">PMGSY Phase-III (Uttar Pradesh)</option>
                <option value="PMGSY Phase-II (Madhya Pradesh)">PMGSY Phase-II (Madhya Pradesh)</option>
                <option value="PMGSY Phase-III (Bihar)">PMGSY Phase-III (Bihar)</option>
              </select>
              {touched && !isStateValid && (
                <span className="text-[11px] text-rose-500 mt-1 block">State / Scheme is required</span>
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">
                Package Number / Road Name <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                value={packageNumber}
                onChange={(e) => setPackageNumber(e.target.value)}
                placeholder="e.g., RJ-04-102 (NH-62 to Kherapa Road)"
                className={`w-full px-3 py-2 bg-white dark:bg-slate-800 border rounded-lg text-sm text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-[#53B7E8] ${
                  touched && !isPackageValid
                    ? 'border-rose-400 bg-rose-50/20'
                    : 'border-slate-300 dark:border-slate-700'
                }`}
              />
              {touched && !isPackageValid && (
                <span className="text-[11px] text-rose-500 mt-1 block">
                  Package Number / Road Name is required
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Section 2: Source Documents Upload Dropzones */}
        <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-xs space-y-4 transition-colors duration-200">
          <div className="border-b border-slate-100 dark:border-slate-800 pb-4">
            <h2 className="text-base font-semibold text-slate-900 dark:text-white">
              2. Source Documents
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Upload all 3 required source documents for tri-source discrepancy detection.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* QM E-Form */}
            <FileUploader
              title="QM E-Form"
              description="Digital Quality Monitor field inspection report"
              fileTypeLabel="QM Form"
              selectedFile={qmFile}
              onFileSelect={(file) => setQmFile(file)}
              onFileRemove={() => setQmFile(null)}
              error={touched && !isQmFileValid ? 'QM E-Form is required' : null}
            />

            {/* Test Datasheet */}
            <FileUploader
              title="Test Datasheet"
              description="Laboratory compressive & gradation test logs"
              fileTypeLabel="Datasheet"
              selectedFile={testDatasheetFile}
              onFileSelect={(file) => setTestDatasheetFile(file)}
              onFileRemove={() => setTestDatasheetFile(null)}
              error={touched && !isDatasheetValid ? 'Test Datasheet is required' : null}
            />

            {/* Quality Control Register */}
            <FileUploader
              title="Quality Control Register"
              description="Contractor daily site QCR entry log"
              fileTypeLabel="QCR"
              selectedFile={qcrFile}
              onFileSelect={(file) => setQcrFile(file)}
              onFileRemove={() => setQcrFile(null)}
              error={touched && !isQcrValid ? 'QCR document is required' : null}
            />
          </div>
        </div>

        {/* Validation Summary Bar if missing fields */}
        {!isFormValid && (
          <div className="flex items-center gap-2 p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/60 rounded-xl text-xs text-[#8c6d00] dark:text-[#FFF200]">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>
              Please enter Package Number and upload all 3 source documents to enable Start Analysis.
            </span>
          </div>
        )}

        {/* Action Button */}
        <div className="flex justify-end gap-3">
          <button
            type="submit"
            disabled={!isFormValid}
            className={`inline-flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-semibold transition shadow-xs ${
              isFormValid
                ? 'bg-[#53B7E8] hover:bg-[#3aa3d8] text-white cursor-pointer'
                : 'bg-slate-200 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed'
            }`}
          >
            <span>Start Analysis</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
