import React, { useState, useEffect } from 'react';
import { getHealth } from '../services/api';
import { Shield, FileText, AlertTriangle, Play, RefreshCw, BarChart2, Cpu } from 'lucide-react';

export default function Home({ navigateTo }) {
  const [healthStatus, setHealthStatus] = useState({ loading: true, online: false, info: null });

  const checkHealth = async () => {
    setHealthStatus(prev => ({ ...prev, loading: true }));
    const health = await getHealth();
    if (health && (health.status === 'ok' || health.status === 'online' || health.status === 'healthy')) {
      setHealthStatus({ loading: false, online: true, info: health });
    } else {
      setHealthStatus({ loading: false, online: false, info: health });
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '1rem 0' }}>
      {/* Hero Section */}
      <div className="glass-card" style={{
        background: 'linear-gradient(135deg, rgba(14, 25, 44, 0.8), rgba(20, 40, 72, 0.7))',
        border: '1px solid rgba(59, 130, 246, 0.25)',
        padding: '3rem 2rem',
        borderRadius: '24px',
        textAlign: 'center',
        marginBottom: '2.5rem',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{
          position: 'absolute',
          top: '-50px',
          right: '-50px',
          width: '200px',
          height: '200px',
          background: 'radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, transparent 70%)',
          pointerEvents: 'none'
        }} />
        
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          border: '1px solid rgba(59, 130, 246, 0.3)',
          color: '#3b82f6',
          padding: '0.4rem 1rem',
          borderRadius: '9999px',
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
          marginBottom: '1.5rem'
        }}>
          <Cpu size={14} /> SIH 2026 Smart Infrastructure Platform
        </div>
        
        <h1 style={{
          fontSize: '3rem',
          fontWeight: '800',
          lineHeight: '1.15',
          letterSpacing: '-0.03em',
          marginBottom: '1rem',
          background: 'linear-gradient(to right, #ffffff, #93c5fd, #22d3ee)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          QCR AI
        </h1>
        <h2 style={{
          fontSize: '1.4rem',
          color: '#e2e8f0',
          fontWeight: '600',
          marginBottom: '1.2rem',
          letterSpacing: '-0.01em'
        }}>
          Quality Control Record Discrepancy Detection System
        </h2>
        <p style={{
          color: 'var(--text-secondary)',
          fontSize: '1.05rem',
          maxWidth: '750px',
          margin: '0 auto 2.5rem',
          lineHeight: '1.6'
        }}>
          Automated multi-document ingestion and compliance audit engine for PMGSY road construction. 
          Extract parameters, normalize measurement metrics, link road project registers, and flag structural discrepancies with high-precision confidence scoring.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <button 
            className="btn-primary" 
            style={{ padding: '0.85rem 2rem', fontSize: '0.95rem' }}
            onClick={() => navigateTo('upload')}
          >
            <Play size={18} /> Ingest Inspection Documents
          </button>
          <button 
            className="btn-secondary" 
            style={{ padding: '0.85rem 2rem', fontSize: '0.95rem' }}
            onClick={() => navigateTo('dashboard')}
          >
            <BarChart2 size={18} /> Open Analysis Dashboard
          </button>
        </div>
      </div>

      {/* Backend Status Bar */}
      <div className="glass-card" style={{
        padding: '0.85rem 1.5rem',
        borderRadius: '14px',
        marginBottom: '2.5rem',
        display: 'flex',
        justifyContent: 'between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flex: 1 }}>
          <div style={{
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            backgroundColor: healthStatus.online ? 'var(--color-success)' : 'var(--color-critical)',
            boxShadow: healthStatus.online ? '0 0 10px var(--color-success)' : '0 0 10px var(--color-critical)',
            transition: 'all 0.3s'
          }} />
          <span style={{ fontSize: '0.85rem', fontWeight: '600' }}>
            System Core: {healthStatus.online ? 'CONNECTED (FastAPI Online)' : 'OFFLINE (Client Fallback Active)'}
          </span>
          {healthStatus.info && healthStatus.info.service && (
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
              | Engine: {healthStatus.info.service}
            </span>
          )}
        </div>
        <button 
          onClick={checkHealth} 
          disabled={healthStatus.loading}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            fontSize: '0.8rem',
            fontWeight: '600'
          }}
        >
          <RefreshCw size={12} className={healthStatus.loading ? 'glow-active' : ''} /> Refresh Connection
        </button>
      </div>

      {/* Feature Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        <div className="glass-card">
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '10px',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-primary)',
            marginBottom: '1.25rem'
          }}>
            <FileText size={22} />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '0.5rem' }}>Multi-Doc Ingestion</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.5' }}>
            Ingests standard Quality Control Registers (QCR), Test Datasheets, and QM E-Forms. Handles both scanned text overlays and physical layout geometry using OCR processors.
          </p>
        </div>

        <div className="glass-card">
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '10px',
            backgroundColor: 'rgba(6, 182, 212, 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-accent)',
            marginBottom: '1.25rem'
          }}>
            <Cpu size={22} />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '0.5rem' }}>Standardized Normalization</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.5' }}>
            Converts variations in measuring scales (e.g. centimeters to millimeters), date formats, and layout coordinates into a unified data schema model prior to running comparisons.
          </p>
        </div>

        <div className="glass-card">
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '10px',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--color-critical)',
            marginBottom: '1.25rem'
          }}>
            <AlertTriangle size={22} />
          </div>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700', marginBottom: '0.5rem' }}>Discrepancy Resolver</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: '1.5' }}>
            Applies cross-document comparison rules. Automatically identifies discrepancies in core parameters like layer thickness, material grading, and field strength.
          </p>
        </div>
      </div>
    </div>
  );
}
