import React, { useState } from 'react';
import Home from './pages/Home';
import UploadDocuments from './pages/UploadDocuments';
import Dashboard from './pages/Dashboard';
import Results from './pages/Results';
import { Home as HomeIcon, UploadCloud, BarChart3, Database, Layers, Brain, CheckSquare } from 'lucide-react';

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedProject, setSelectedProject] = useState(null);

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <Home navigateTo={setCurrentPage} />;
      case 'upload':
        return <UploadDocuments navigateTo={setCurrentPage} setProjectData={setSelectedProject} />;
      case 'dashboard':
        return <Dashboard navigateTo={setCurrentPage} setProjectData={setSelectedProject} />;
      case 'results':
        return <Results navigateTo={setCurrentPage} projectData={selectedProject} />;
      default:
        return <Home navigateTo={setCurrentPage} />;
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside style={{
        width: '260px',
        backgroundColor: 'var(--bg-secondary)',
        borderRight: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        padding: '1.5rem',
        flexShrink: 0
      }}>
        {/* Sidebar Brand */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          marginBottom: '2.5rem',
          paddingLeft: '0.5rem'
        }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, var(--color-primary), var(--color-accent))',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: '800',
            fontSize: '1rem',
            boxShadow: '0 0 12px rgba(59, 130, 246, 0.4)'
          }}>
            Q
          </div>
          <div>
            <h1 style={{ fontSize: '1.2rem', fontWeight: '800', tracking: '-0.02em', lineHeight: '1' }}>QCR AI</h1>
            <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', fontWeight: '700', textTransform: 'uppercase', tracking: '0.05em' }}>Audit Engine</span>
          </div>
        </div>

        {/* Sidebar Links */}
        <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
          <button 
            onClick={() => setCurrentPage('home')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              width: '100%',
              padding: '0.75rem 1rem',
              backgroundColor: currentPage === 'home' ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
              color: currentPage === 'home' ? 'var(--color-primary)' : 'var(--text-secondary)',
              border: 'none',
              borderRadius: '8px',
              textAlign: 'left',
              cursor: 'pointer',
              fontWeight: currentPage === 'home' ? '600' : '500',
              fontSize: '0.875rem',
              transition: 'all 0.2s'
            }}
          >
            <HomeIcon size={18} /> Home
          </button>
          
          <button 
            onClick={() => setCurrentPage('upload')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              width: '100%',
              padding: '0.75rem 1rem',
              backgroundColor: currentPage === 'upload' ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
              color: currentPage === 'upload' ? 'var(--color-primary)' : 'var(--text-secondary)',
              border: 'none',
              borderRadius: '8px',
              textAlign: 'left',
              cursor: 'pointer',
              fontWeight: currentPage === 'upload' ? '600' : '500',
              fontSize: '0.875rem',
              transition: 'all 0.2s'
            }}
          >
            <UploadCloud size={18} /> Ingest Documents
          </button>

          <button 
            onClick={() => setCurrentPage('dashboard')}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              width: '100%',
              padding: '0.75rem 1rem',
              backgroundColor: currentPage === 'dashboard' || currentPage === 'results' ? 'rgba(59, 130, 246, 0.1)' : 'transparent',
              color: currentPage === 'dashboard' || currentPage === 'results' ? 'var(--color-primary)' : 'var(--text-secondary)',
              border: 'none',
              borderRadius: '8px',
              textAlign: 'left',
              cursor: 'pointer',
              fontWeight: currentPage === 'dashboard' || currentPage === 'results' ? '600' : '500',
              fontSize: '0.875rem',
              transition: 'all 0.2s'
            }}
          >
            <BarChart3 size={18} /> Audit Dashboard
          </button>
        </nav>

        {/* Sidebar Footer */}
        <div style={{
          borderTop: '1px solid var(--border-color)',
          paddingTop: '1.25rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
            <Database size={14} />
            <span style={{ fontSize: '0.7rem', fontWeight: '600' }}>Local Database Online</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)' }}>
            <Brain size={14} />
            <span style={{ fontSize: '0.7rem', fontWeight: '600' }}>EasyOCR Active</span>
          </div>
        </div>
      </aside>

      {/* Main Container */}
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}
