import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeProvider';
import DashboardLayout from './layouts/DashboardLayout';
import LandingPage from './pages/LandingPage';
import Dashboard from './pages/Dashboard';
import NewAnalysis from './pages/NewAnalysis';
import Processing from './pages/Processing';
import Results from './pages/Results';
import DiscrepancyDetails from './pages/DiscrepancyDetails';
import Records from './pages/Records';
import Reports from './pages/Reports';

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          {/* Landing Page at Root Route */}
          <Route path="/" element={<LandingPage />} />

          {/* Application Layout with Two-Level Horizontal Navbar */}
          <Route element={<DashboardLayout />}>
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="analysis/new" element={<NewAnalysis />} />
            <Route path="analysis/processing" element={<Processing />} />
            <Route path="analysis/results" element={<Results />} />
            <Route path="analysis/discrepancy/:id" element={<DiscrepancyDetails />} />
            <Route path="records" element={<Records />} />
            <Route path="reports" element={<Reports />} />
          </Route>

          {/* Catch-all fallback redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
