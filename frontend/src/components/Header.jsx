import React from 'react';
import { Menu, Bell, Shield, Search } from 'lucide-react';

export default function Header({ onMenuClick }) {
  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-4 sm:px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          className="p-2 rounded-lg text-slate-600 hover:bg-slate-100 lg:hidden"
          aria-label="Toggle Navigation Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200/60">
            <Shield className="w-3.5 h-3.5 text-blue-600" />
            PMGSY QC Engine v1.0
          </span>
          <span className="hidden md:inline-block text-xs text-slate-400 font-medium">
            • Rural Road Discrepancy Detection
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3 sm:gap-4">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-500 w-56">
          <Search className="w-3.5 h-3.5 text-slate-400" />
          <span>Search road pkg, QCR...</span>
        </div>

        <button
          type="button"
          className="relative p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700 transition"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-600 rounded-full" />
        </button>

        <div className="h-6 w-px bg-slate-200" />

        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-semibold shadow-xs">
            SQ
          </div>
          <div className="hidden md:block text-left">
            <div className="text-xs font-semibold text-slate-900 leading-tight">
              State Quality Monitor
            </div>
            <div className="text-[10px] text-slate-500">Ministry of Rural Dev.</div>
          </div>
        </div>
      </div>
    </header>
  );
}
