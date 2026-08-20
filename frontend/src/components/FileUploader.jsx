import React from 'react';
import { UploadCloud, FileText, CheckCircle2, X } from 'lucide-react';

function formatFileSize(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

export default function FileUploader({
  title = 'Upload Document',
  description = 'Supports PDF, Scan copies, CSV or Excel files',
  accept = '.pdf,.xlsx,.xls,.csv',
  fileTypeLabel = 'Document',
  selectedFile = null,
  onFileSelect,
  onFileRemove,
  error = null,
  className = '',
}) {
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      if (onFileSelect) {
        onFileSelect(e.target.files[0]);
      }
      // Reset input value so re-selecting same file triggers onChange
      e.target.value = '';
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-5 transition-all flex flex-col justify-between ${
        selectedFile
          ? 'border-[#99CA84] bg-[#99CA84]/10 dark:bg-[#99CA84]/5'
          : error
          ? 'border-rose-300 bg-rose-50/40 dark:bg-rose-950/20 dark:border-rose-800'
          : 'border-slate-300 dark:border-slate-700 hover:border-[#53B7E8] bg-slate-50/50 dark:bg-slate-900/50'
      } ${className}`}
    >
      <div className="flex flex-col items-center text-center">
        {/* Status Icon */}
        <div
          className={`w-11 h-11 rounded-full flex items-center justify-center mb-2.5 ${
            selectedFile
              ? 'bg-[#3A801C]/15 text-[#3A801C] dark:text-[#99CA84]'
              : error
              ? 'bg-rose-100 dark:bg-rose-950 text-rose-600 dark:text-rose-400'
              : 'bg-[#C7EAFC]/60 dark:bg-sky-950/60 text-[#53B7E8]'
          }`}
        >
          {selectedFile ? <CheckCircle2 className="w-5 h-5" /> : <UploadCloud className="w-5 h-5" />}
        </div>

        <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">{title}</h4>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-xs">{description}</p>
      </div>

      {/* Uploaded State Box vs Select Button */}
      <div className="mt-4 flex flex-col items-center">
        {selectedFile ? (
          <div className="w-full flex items-center justify-between gap-2 px-3 py-2 bg-white dark:bg-slate-800 border border-[#99CA84] dark:border-[#99CA84]/60 rounded-lg shadow-2xs">
            <div className="flex items-center gap-2 min-w-0">
              <FileText className="w-4 h-4 text-[#3A801C] dark:text-[#99CA84] shrink-0" />
              <div className="truncate text-left">
                <div className="text-xs font-medium text-slate-800 dark:text-slate-200 truncate">
                  {selectedFile.name}
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400">
                  {formatFileSize(selectedFile.size)}
                </div>
              </div>
            </div>

            {onFileRemove && (
              <button
                type="button"
                onClick={onFileRemove}
                className="p-1 rounded-md text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/50 transition cursor-pointer"
                title="Remove file"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        ) : (
          <label className="inline-flex items-center gap-2 px-3.5 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 rounded-lg text-xs font-medium text-slate-700 dark:text-slate-200 shadow-2xs cursor-pointer transition">
            <span>Select {fileTypeLabel}</span>
            <input
              type="file"
              accept={accept}
              className="sr-only"
              onChange={handleFileChange}
            />
          </label>
        )}

        {/* Validation Error */}
        {error && !selectedFile && (
          <span className="text-[11px] font-medium text-rose-600 dark:text-rose-400 mt-2">
            {error}
          </span>
        )}
      </div>
    </div>
  );
}
