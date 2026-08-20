import React from 'react';
import { NavLink, Link } from 'react-router-dom';
import {
  ShieldCheck,
  LayoutDashboard,
  PlusCircle,
  FolderArchive,
  FileBarChart2,
  Search,
  Sun,
  Moon,
  ChevronDown,
} from 'lucide-react';
import { useTheme } from '../context/useTheme';

export default function Navbar() {
  const { isDark, toggleTheme } = useTheme();

  const navItems = [
    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: LayoutDashboard,
      disabled: false,
    },
    {
      name: 'New Analysis',
      path: '/analysis/new',
      icon: PlusCircle,
      disabled: false,
    },
    {
      name: 'Records',
      path: '/records',
      icon: FolderArchive,
      disabled: false,
    },
    {
      name: 'Reports',
      path: '/reports',
      icon: FileBarChart2,
      disabled: false,
    },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-xs transition-colors duration-200">
      {/* ========================================================
          ROW 1: BRAND + USER PROFILE
          ======================================================== */}
      <div className="border-b border-slate-100 dark:border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
          {/* Left: Brand Identity */}
          <Link to="/dashboard" className="flex items-center gap-3 group">
            <div className="w-8 h-8 rounded-lg bg-[#53B7E8] text-white flex items-center justify-center shadow-2xs group-hover:bg-[#3aa3d8] transition">
              <ShieldCheck className="w-4.5 h-4.5" />
            </div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base tracking-tight text-slate-900 dark:text-white">
                Q-Recon
              </span>
              <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-[#C7EAFC] dark:bg-sky-950 text-[#0c4a6e] dark:text-[#53B7E8] border border-[#53B7E8]/40">
                QC AI
              </span>
            </div>
          </Link>

          {/* Right: State Quality Monitor User Section */}
          <div className="flex items-center gap-3 sm:gap-4">
            <div className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 dark:bg-emerald-950/60 text-[#3A801C] dark:text-[#99CA84] border border-[#99CA84]/60 dark:border-emerald-800">
              <span className="w-1.5 h-1.5 rounded-full bg-[#3A801C] dark:bg-[#99CA84] animate-pulse" />
              PMGSY QC Engine Active
            </div>

            <div className="flex items-center gap-2.5 pl-2">
              <div className="w-8 h-8 rounded-full bg-slate-900 dark:bg-slate-800 text-white flex items-center justify-center text-xs font-semibold ring-2 ring-slate-100 dark:ring-slate-700 shadow-2xs">
                SQ
              </div>
              <div className="text-left hidden md:block">
                <div className="text-xs font-semibold text-slate-900 dark:text-slate-100 leading-tight">
                  State Quality Monitor
                </div>
                <div className="text-[10px] text-slate-500 dark:text-slate-400">
                  PMGSY QC Division
                </div>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500 hidden md:block" />
            </div>
          </div>
        </div>
      </div>

      {/* ========================================================
          ROW 2: NAVIGATION TABS + SEARCH + THEME TOGGLE
          ======================================================== */}
      <div className="bg-slate-50/70 dark:bg-slate-900/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-12 flex items-center justify-between gap-4">
          {/* Horizontal Navigation Items */}
          <nav className="flex items-center gap-1 sm:gap-2 overflow-x-auto no-scrollbar py-1">
            {navItems.map((item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  key={item.name}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                      isActive
                        ? 'bg-[#53B7E8] text-white font-semibold shadow-xs'
                        : 'text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-white dark:hover:bg-slate-800'
                    }`
                  }
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{item.name}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Right Controls: Search + Dark Mode Toggle */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            <div className="hidden lg:flex items-center gap-2 px-2.5 py-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-xs text-slate-500 dark:text-slate-400 w-52 shadow-2xs">
              <Search className="w-3.5 h-3.5 text-slate-400" />
              <input
                type="text"
                placeholder="Search package, QCR..."
                className="bg-transparent text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none w-full text-xs"
                readOnly
              />
            </div>

            {/* Dark/Light Mode Switcher Button */}
            <button
              type="button"
              onClick={toggleTheme}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-700 dark:text-slate-200 transition shadow-2xs cursor-pointer"
              title={isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              {isDark ? (
                <>
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  <span className="hidden sm:inline">Light</span>
                </>
              ) : (
                <>
                  <Moon className="w-3.5 h-3.5 text-slate-600" />
                  <span className="hidden sm:inline">Dark</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
