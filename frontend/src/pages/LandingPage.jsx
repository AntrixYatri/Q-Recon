import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, ArrowRight, FileCheck, Layers, Award, Sun, Moon } from 'lucide-react';
import RuralRoadBackground from '../components/RuralRoadBackground';
import { useTheme } from '../context/useTheme';

export default function LandingPage() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col justify-between relative overflow-hidden transition-colors duration-300">
      {/* Subtle rural road background with natural curves, trees, and animated moving cars */}
      <RuralRoadBackground />

      {/* Atmospheric accent glow */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#C7EAFC]/40 dark:bg-[#53B7E8]/10 rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="absolute bottom-10 left-1/4 w-80 h-80 bg-[#99CA84]/20 dark:bg-[#3A801C]/10 rounded-full blur-3xl pointer-events-none -z-10" />

      {/* Top Bar with Branding & Theme Switcher */}
      <header className="max-w-7xl w-full mx-auto px-6 py-6 flex items-center justify-between z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#53B7E8] text-white flex items-center justify-center shadow-xs">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <span className="font-bold text-lg tracking-tight text-slate-900 dark:text-white">
              Q-Recon
            </span>
            <span className="ml-2 text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-[#C7EAFC] dark:bg-sky-950 text-[#0c4a6e] dark:text-[#53B7E8] border border-[#53B7E8]/40">
              QC AI
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-xs font-medium text-slate-500 dark:text-slate-400 hidden sm:block">
            Ministry of Rural Development • PMGSY
          </div>
          <button
            type="button"
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition shadow-2xs cursor-pointer"
            aria-label="Toggle Light/Dark Theme"
          >
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-600" />}
          </button>
        </div>
      </header>

      {/* Main Hero Container with Staggered Entrance Animations */}
      <main className="max-w-3xl mx-auto px-6 py-12 sm:py-16 text-center flex flex-col items-center justify-center z-10">
        {/* Verification Authority Badge (Fade In) */}
        <div className="animate-fade-in-up inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/90 dark:bg-slate-900/90 backdrop-blur-xs border border-slate-200 dark:border-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-300 shadow-2xs mb-8">
          <span className="w-2 h-2 rounded-full bg-[#3A801C]" />
          <span>Rural Road Quality Control Verification Engine</span>
        </div>

        {/* Product Name (Fade In Up, Delay 100ms) */}
        <h1 className="animate-fade-in-up animation-delay-100 text-5xl sm:text-6xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-tight">
          Q-Recon
        </h1>

        {/* Subtitle (Fade In Up, Delay 200ms) */}
        <p className="animate-fade-in-up animation-delay-200 mt-4 text-lg sm:text-xl text-slate-600 dark:text-slate-300 font-medium max-w-xl leading-relaxed">
          AI-Assisted Quality Control & Road Record Verification
        </p>

        {/* Secondary Context Callout (Fade In Up, Delay 300ms) */}
        <p className="animate-fade-in-up animation-delay-300 mt-2 text-xs text-slate-500 dark:text-slate-400 max-w-md">
          Tri-source automated cross-examination across QM E-Forms, Laboratory Test Datasheets, and Contractor Quality Control Registers (QCRs).
        </p>

        {/* CTA Button (Fade In Up, Delay 400ms) */}
        <div className="animate-fade-in-up animation-delay-400 mt-10">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-3 px-8 py-3.5 bg-[#53B7E8] hover:bg-[#3aa3d8] active:scale-[0.99] text-white rounded-xl text-base font-semibold transition-all shadow-md shadow-[#53B7E8]/20 hover:shadow-lg hover:shadow-[#53B7E8]/30 cursor-pointer"
          >
            <span>Get Started</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>

        {/* Micro Feature Highlight Cards (Fade In Up, Delay 500ms) */}
        <div className="animate-fade-in-up animation-delay-500 mt-14 pt-8 border-t border-slate-200/80 dark:border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-5 text-left w-full">
          <div className="flex items-start gap-3 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xs p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800 shadow-2xs">
            <div className="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-100 dark:border-emerald-900/50 text-[#3A801C] shrink-0">
              <FileCheck className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-semibold text-slate-800 dark:text-slate-200">Tri-Source Audit</div>
              <div className="text-[11px] text-slate-500 dark:text-slate-400">QM, QCR & Lab Data</div>
            </div>
          </div>

          <div className="flex items-start gap-3 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xs p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800 shadow-2xs">
            <div className="p-2 rounded-lg bg-sky-50 dark:bg-sky-950/50 border border-sky-100 dark:border-sky-900/50 text-[#53B7E8] shrink-0">
              <Layers className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-semibold text-slate-800 dark:text-slate-200">IRC Standard Compliance</div>
              <div className="text-[11px] text-slate-500 dark:text-slate-400">Automated Bounds Check</div>
            </div>
          </div>

          <div className="flex items-start gap-3 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xs p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-800 shadow-2xs">
            <div className="p-2 rounded-lg bg-amber-50 dark:bg-amber-950/50 border border-amber-100 dark:border-amber-900/50 text-[#D4A700] shrink-0">
              <Award className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-semibold text-slate-800 dark:text-slate-200">Confidence Scoring</div>
              <div className="text-[11px] text-slate-500 dark:text-slate-400">Evidence-Backed Reports</div>
            </div>
          </div>
        </div>
      </main>

      {/* Minimal Footer */}
      <footer className="max-w-7xl w-full mx-auto px-6 py-6 text-center text-xs text-slate-400 dark:text-slate-500 border-t border-slate-200/60 dark:border-slate-800/80 z-10">
        Q-Recon • Smart India Hackathon 2024 / Quality Assurance System
      </footer>
    </div>
  );
}
