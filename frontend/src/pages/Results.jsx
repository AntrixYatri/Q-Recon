import React from 'react';
import { ArrowLeft, AlertTriangle, AlertOctagon, Info, CheckCircle, Download, FileSpreadsheet, FileJson } from 'lucide-react';

export default function Results({ navigateTo, projectData }) {
  // If no project selected, direct to dashboard
  if (!projectData) {
    return (
      <div style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center', padding: '3rem 1.5rem' }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>No project selected for review</h3>
        <button className="btn-primary" style={{ margin: '0 auto' }} onClick={() => navigateTo('dashboard')}>
          Go to Dashboard
        </button>
      </div>
    );
  }

  const handleDownloadJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(projectData, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `QCR_Audit_${projectData.package_id}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
      {/* Back button and title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <button 
          className="btn-secondary" 
          style={{ padding: '0.5rem', borderRadius: '50%' }}
          onClick={() => navigateTo('dashboard')}
        >
          <ArrowLeft size={16} />
        </button>
        <div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '600', textTransform: 'uppercase' }}>Audit Result Details</span>
          <h2 style={{ fontSize: '1.35rem', fontWeight: '800', color: 'var(--text-primary)' }}>{projectData.road_name}</h2>
        </div>
      </div>

      {/* Project Meta Card */}
      <div className="glass-card" style={{
        padding: '1.25rem 1.5rem',
        marginBottom: '2rem',
        background: 'linear-gradient(135deg, rgba(14, 25, 44, 0.5), rgba(15, 23, 42, 0.5))',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1.5rem'
      }}>
        <div>
          <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Package ID</span>
          <div style={{ fontWeight: '700', marginTop: '0.2rem', fontFamily: 'var(--font-mono)' }}>{projectData.package_id}</div>
        </div>
        <div>
          <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Location Details</span>
          <div style={{ fontWeight: '700', marginTop: '0.2rem' }}>{projectData.district}, {projectData.state}</div>
        </div>
        <div>
          <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)' }}>Compliance State</span>
          <div style={{ marginTop: '0.2rem' }}>
            <span className={`badge ${projectData.status === 'CONSISTENT' ? 'badge-success' : 'badge-critical'}`}>
              {projectData.status}
            </span>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'end' }}>
          <button 
            className="btn-secondary" 
            style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            onClick={handleDownloadJSON}
          >
            <FileJson size={14} /> Export JSON
          </button>
        </div>
      </div>

      {/* Discrepancy List / Consistent Message */}
      {projectData.total_discrepancies > 0 ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <AlertTriangle size={18} style={{ color: 'var(--color-warning)' }} /> 
            Detected Discrepancies ({projectData.total_discrepancies})
          </h3>

          {projectData.discrepancies.map((disc, idx) => {
            const isCrit = disc.severity === 'critical';
            return (
              <div 
                key={disc.id} 
                className="glass-card" 
                style={{
                  borderLeft: `4px solid ${isCrit ? 'var(--color-critical)' : 'var(--color-warning)'}`,
                  padding: '1.5rem',
                  position: 'relative'
                }}
              >
                {/* Header */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'between',
                  alignItems: 'start',
                  flexWrap: 'wrap',
                  gap: '0.5rem',
                  marginBottom: '1rem'
                }}>
                  <div>
                    <span className={`badge ${isCrit ? 'badge-critical' : 'badge-warning'}`} style={{ marginBottom: '0.5rem' }}>
                      {disc.severity} • {disc.discrepancy_type}
                    </span>
                    <h4 style={{ fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-primary)' }}>{disc.field}</h4>
                  </div>
                  <div style={{ textAlign: 'right', fontSize: '0.8rem' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Match Confidence:</span>
                    <div style={{ fontWeight: '700', fontSize: '1rem', color: 'var(--color-accent)' }}>{disc.confidence}%</div>
                  </div>
                </div>

                {/* Values Comparison View */}
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                  gap: '1rem',
                  marginBottom: '1.25rem',
                  backgroundColor: 'rgba(0, 0, 0, 0.25)',
                  padding: '1rem',
                  borderRadius: '8px',
                  border: '1px solid var(--border-color)'
                }}>
                  <div style={{ borderRight: '1px solid var(--border-color)', paddingRight: '0.5rem' }}>
                    <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: '700' }}>
                      Source A: {disc.document_a}
                    </div>
                    <div style={{ fontSize: '1.1rem', fontWeight: '800', marginTop: '0.25rem', color: 'var(--text-primary)' }}>
                      {disc.value_a}
                    </div>
                  </div>
                  <div style={{ paddingLeft: '0.5rem' }}>
                    <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: '700' }}>
                      Source B: {disc.document_b}
                    </div>
                    <div style={{ fontSize: '1.1rem', fontWeight: '800', marginTop: '0.25rem', color: isCrit ? 'var(--color-critical)' : 'var(--color-warning)' }}>
                      {disc.value_b}
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                <div style={{
                  display: 'flex',
                  gap: '0.6rem',
                  alignItems: 'start',
                  fontSize: '0.85rem',
                  color: 'var(--text-secondary)',
                  lineHeight: '1.5'
                }}>
                  <Info size={16} style={{ color: 'var(--color-primary)', flexShrink: 0, marginTop: '0.15rem' }} />
                  <p>{disc.explanation}</p>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="glass-card" style={{
          padding: '3rem 2rem',
          textAlign: 'center',
          borderLeft: '4px solid var(--color-success)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <CheckCircle size={48} style={{ color: 'var(--color-success)' }} />
          <h3 style={{ fontSize: '1.25rem', fontWeight: '700' }}>Project Records fully Compliant</h3>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', fontSize: '0.9rem', lineHeight: '1.6' }}>
            AI engines scanned and mapped both the Quality Control Registers (QCR) and Material Test Datasheets. No numerical mismatches, layout variations, or anomalous values were found. The road metrics align with structural standards.
          </p>
        </div>
      )}
    </div>
  );
}
