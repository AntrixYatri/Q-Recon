import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  PlusCircle,
  FolderArchive,
  FileBarChart2,
  ShieldCheck,
  ChevronRight,
} from 'lucide-react';

export default function Sidebar({ isOpen, onClose }) {
  const navLinks = [
    {
      name: 'Dashboard',
      path: '/',
      icon: LayoutDashboard,
      activeExact: true,
      disabled: false,
    },
    {
      name: 'New Analysis',
      path: '/analysis/new',
      icon: PlusCircle,
      activeExact: false,
      disabled: false,
    },
    {
      name: 'Records',
      path: '/records',
      icon: FolderArchive,
      disabled: true,
      badge: 'Soon',
    },
    {
      name: 'Reports',
      path: '/reports',
      icon: FileBarChart2,
      disabled: true,
      badge: 'Soon',
    },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-900 text-slate-100 flex flex-col border-r border-slate-800 transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center gap-3 px-5 border-b border-slate-800/80">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-sm shadow-blue-500/30">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="font-bold text-sm tracking-tight text-white flex items-center gap-2">
              QCR-SIH
              <span className="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-400/30">
                QC AI
              </span>
            </div>
            <div className="text-[11px] text-slate-400 font-medium">
              AI-Assisted Quality Control
            </div>
          </div>
        </div>

        {/* Navigation Section */}
        <div className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
            Inspection Management
          </div>

          {navLinks.map((link) => {
            const Icon = link.icon;

            if (link.disabled) {
              return (
                <div
                  key={link.name}
                  className="flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium text-slate-400 cursor-not-allowed opacity-60"
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4" />
                    <span>{link.name}</span>
                  </div>
                  {link.badge && (
                    <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {link.badge}
                    </span>
                  )}
                </div>
              );
            }

            return (
              <NavLink
                key={link.name}
                to={link.path}
                end={link.activeExact}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white font-semibold shadow-xs'
                      : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="flex items-center gap-3">
                      <Icon className="w-4 h-4" />
                      <span>{link.name}</span>
                    </div>
                    {isActive && <ChevronRight className="w-3.5 h-3.5 text-blue-200" />}
                  </>
                )}
              </NavLink>
            );
          })}
        </div>

        {/* System Meta Footer */}
        <div className="p-4 border-t border-slate-800/80 bg-slate-950/40">
          <div className="rounded-lg p-3 bg-slate-800/60 border border-slate-700/60 text-xs">
            <div className="flex items-center gap-2 text-slate-300 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>National Rural QC Engine</span>
            </div>
            <p className="text-[11px] text-slate-400 mt-1">
              Cross-verification active for QM & QCR records.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}
