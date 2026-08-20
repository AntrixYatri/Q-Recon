import React, { useState, useEffect } from 'react';
import { getProjects } from '../services/api';
import { BarChart2, Shield, AlertOctagon, AlertTriangle, CheckCircle, FileText, ChevronRight, Search, Activity } from 'lucide-react';

export default function Dashboard({ navigateTo, setProjectData }) {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const data = await getProjects();
        setProjects(data);
      } catch (err) {
        console.error("Failed to load dashboard projects data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, []);

  const handleViewDetails = (project) => {
    setProjectData(project);
    navigateTo('results');
  };

  // Calculations
  const totalAnalyzed = projects.length;
  const totalDiscrepancies = projects.reduce((acc, p) => acc + p.total_discrepancies, 0);
  const criticalCount = projects.reduce((acc, p) => acc + p.critical, 0);
  const warningCount = projects.reduce((acc, p) => acc + p.warning, 0);
  const consistentCount = projects.filter(p => p.status === 'CONSISTENT').length;
  const avgConfidence = projects.length > 0 
    ? (projects.reduce((acc, p) => acc + p.ocr_confidence, 0) / projects.length).toFixed(1) 
    : '0';

  const filteredProjects = projects.filter(p => 
    p.road_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.package_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.district.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Loading dashboard statistics...</p>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div className="section-title">
        <BarChart2 size={22} style={{ color: 'var(--color-primary)' }} /> Audit Control & Analytics Dashboard
      </div>

      {/* Aggregate Stats Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '1.25rem',
        marginBottom: '2rem'
      }}>
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', minHeight: '100px' }}>
          <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>Total Projects</span>
            <FileText size={16} style={{ color: 'var(--color-primary)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '0.4rem' }}>{totalAnalyzed}</div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Quality Records Monitored</span>
        </div>

        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>Critical Issues</span>
            <AlertOctagon size={16} style={{ color: 'var(--color-critical)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '0.4rem', color: 'var(--color-critical)' }}>{criticalCount}</div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Requires Immediate Review</span>
        </div>

        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>Warnings</span>
            <AlertTriangle size={16} style={{ color: 'var(--color-warning)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '0.4rem', color: 'var(--color-warning)' }}>{warningCount}</div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Minor or Unit Inconsistencies</span>
        </div>

        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>Consistent</span>
            <CheckCircle size={16} style={{ color: 'var(--color-success)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '0.4rem', color: 'var(--color-success)' }}>{consistentCount}</div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Records in Full Compliance</span>
        </div>

        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.7rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>OCR Confidence</span>
            <Activity size={16} style={{ color: 'var(--color-accent)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: '800', marginTop: '0.4rem', color: 'var(--color-accent)' }}>{avgConfidence}%</div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Average Scanner Accuracy</span>
        </div>
      </div>

      {/* Projects Search & Table */}
      <div className="glass-card" style={{ padding: '1.25rem' }}>
        <div style={{
          display: 'flex',
          justifyContent: 'between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
          marginBottom: '1.25rem',
          borderBottom: '1px solid var(--border-color)',
          paddingBottom: '1rem'
        }}>
          <h3 style={{ fontSize: '1.15rem', fontWeight: '700' }}>Monitored Roads</h3>
          <div style={{
            position: 'relative',
            width: '100%',
            maxWidth: '350px'
          }}>
            <Search size={16} style={{
              position: 'absolute',
              left: '0.75rem',
              top: '50%',
              transform: 'translateY(-50%)',
              color: 'var(--text-muted)'
            }} />
            <input 
              type="text" 
              placeholder="Search by road, package, or district..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                padding: '0.55rem 0.55rem 0.55rem 2.25rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(0, 0, 0, 0.2)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                outline: 'none',
                fontSize: '0.85rem'
              }}
            />
          </div>
        </div>

        {/* Table layout */}
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)' }}>
                <th style={{ padding: '0.75rem 1rem', fontWeight: '600' }}>Road/Project details</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: '600' }}>Package ID</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: '600' }}>District / State</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: '600' }}>Discrepancies</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: '600' }}>Audit Status</th>
                <th style={{ padding: '0.75rem 1rem', fontWeight: '600', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredProjects.length > 0 ? (
                filteredProjects.map((project) => (
                  <tr key={project.id} style={{ borderBottom: '1px solid var(--border-color)', transition: 'background-color 0.2s' }} className="project-row">
                    <td style={{ padding: '1rem' }}>
                      <div style={{ fontWeight: '700', color: 'var(--text-primary)' }}>{project.road_name}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.1rem' }}>OCR Accuracy: {project.ocr_confidence}%</div>
                    </td>
                    <td style={{ padding: '1rem', fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>{project.package_id}</td>
                    <td style={{ padding: '1rem' }}>
                      <div>{project.district}</div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{project.state}</div>
                    </td>
                    <td style={{ padding: '1rem' }}>
                      {project.total_discrepancies > 0 ? (
                        <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                          {project.critical > 0 && <span className="badge badge-critical">{project.critical} Crit</span>}
                          {project.warning > 0 && <span className="badge badge-warning">{project.warning} Warn</span>}
                        </div>
                      ) : (
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>No discrepancies</span>
                      )}
                    </td>
                    <td style={{ padding: '1rem' }}>
                      <span className={`badge ${project.status === 'CONSISTENT' ? 'badge-success' : 'badge-critical'}`}>
                        {project.status}
                      </span>
                    </td>
                    <td style={{ padding: '1rem', textAlign: 'right' }}>
                      <button 
                        className="btn-secondary" 
                        style={{ padding: '0.45rem 0.95rem', fontSize: '0.8rem', display: 'inline-flex', alignItems: 'center' }}
                        onClick={() => handleViewDetails(project)}
                      >
                        Details <ChevronRight size={14} />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" style={{ padding: '2rem 1rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                    No roads match your search query.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Styles */}
      <style>{`
        .project-row:hover {
          background-color: rgba(255, 255, 255, 0.02);
        }
      `}</style>
    </div>
  );
}
