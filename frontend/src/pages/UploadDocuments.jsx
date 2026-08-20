import React, { useState } from 'react';
import { uploadDocument, analyzeProject } from '../services/api';
import { Upload, FileText, CheckCircle, AlertTriangle, ArrowRight, Loader2, Info } from 'lucide-react';

export default function UploadDocuments({ navigateTo, setProjectData }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [docType, setDocType] = useState('qcr');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setUploadResult(null);
      setError(null);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setError("Please select a file to upload.");
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('document_type', docType);

    try {
      const result = await uploadDocument(formData);
      setUploadResult(result);
    } catch (err) {
      setError("An error occurred during file upload. Check your backend status.");
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleRunAnalysis = async () => {
    if (!uploadResult) return;
    setIsUploading(true);
    try {
      // Analyze the project linked to the upload
      const analysisId = uploadResult.analysis_id || "proj-101";
      const resultData = await analyzeProject(analysisId);
      setProjectData(resultData);
      navigateTo('results');
    } catch (err) {
      setError("Failed to generate comparative discrepancy report.");
      console.error(err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto' }}>
      <div className="section-title">
        <Upload size={22} style={{ color: 'var(--color-primary)' }} /> Ingest & Analyze Quality Records
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2rem'
      }}>
        {/* Upload Form Card */}
        <div className="glass-card" style={{ flex: 1.2 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
            Upload Record Document
          </h3>
          
          <form onSubmit={handleUpload}>
            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                Document Category
              </label>
              <select 
                value={docType} 
                onChange={(e) => setDocType(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.65rem',
                  borderRadius: '8px',
                  backgroundColor: '#0a0f18',
                  border: '1px solid var(--border-color)',
                  color: 'var(--text-primary)',
                  outline: 'none'
                }}
              >
                <option value="qcr">Quality Control Register (QCR)</option>
                <option value="datasheet">Material Test Datasheet</option>
                <option value="qm-eform">QM Inspection E-Form</option>
                <option value="other">Other Road Quality Record</option>
              </select>
            </div>

            <div style={{
              border: '2px dashed var(--border-color)',
              borderRadius: '12px',
              padding: '2rem 1.5rem',
              textAlign: 'center',
              backgroundColor: 'rgba(0, 0, 0, 0.2)',
              cursor: 'pointer',
              marginBottom: '1.25rem',
              transition: 'border-color 0.2s',
              position: 'relative'
            }}>
              <input 
                type="file" 
                onChange={handleFileChange}
                accept="image/*,application/pdf"
                style={{
                  position: 'absolute',
                  top: 0, right: 0, bottom: 0, left: 0,
                  opacity: 0,
                  cursor: 'pointer',
                  width: '100%',
                  height: '100%'
                }}
              />
              <Upload size={32} style={{ color: 'var(--text-muted)', marginBottom: '0.75rem' }} />
              <p style={{ fontSize: '0.9rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                {selectedFile ? selectedFile.name : 'Select or drop document file'}
              </p>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                Supports PNG, JPG, WEBP, PDF (Max 10MB)
              </p>
            </div>

            {error && (
              <div style={{
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                border: '1px solid rgba(239, 68, 68, 0.3)',
                color: 'var(--color-critical)',
                borderRadius: '8px',
                padding: '0.75rem',
                fontSize: '0.8rem',
                marginBottom: '1.25rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}>
                <AlertTriangle size={14} />
                <span>{error}</span>
              </div>
            )}

            <button 
              type="submit" 
              className="btn-primary" 
              style={{ width: '100%', justifyContent: 'center' }}
              disabled={isUploading || !selectedFile}
            >
              {isUploading ? (
                <>
                  <Loader2 size={16} className="glow-active" style={{ animation: 'spin 1.5s linear infinite' }} />
                  Extracting Fields...
                </>
              ) : (
                'Run Ingestion & OCR'
              )}
            </button>
          </form>
        </div>

        {/* Dynamic Help Card */}
        <div className="glass-card" style={{ flex: 0.8, display: 'flex', flexDirection: 'column', justifyContent: 'between' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: '700', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
              OCR Pipeline Details
            </h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: '1.5', marginBottom: '1rem' }}>
              The system triggers a multi-stage layout analysis. It runs:
            </p>
            <ul style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', paddingLeft: '1.25rem', lineHeight: '1.7', marginBottom: '1.5rem' }}>
              <li>EasyOCR Engine detection</li>
              <li>Visual word box grouping</li>
              <li>Text and metric normalization</li>
              <li>Field layout label-matching</li>
              <li>Targeted crop pass for inspector signatures</li>
            </ul>
          </div>
          
          <div style={{
            backgroundColor: 'rgba(59, 130, 246, 0.05)',
            border: '1px solid rgba(59, 130, 246, 0.15)',
            borderRadius: '8px',
            padding: '0.75rem',
            display: 'flex',
            gap: '0.5rem',
            alignItems: 'start'
          }}>
            <Info size={16} style={{ color: 'var(--color-primary)', marginTop: '0.1rem', flexShrink: 0 }} />
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: '1.4' }}>
              <strong>Demo Tip:</strong> Upload a QCR image to see real-time OCR results. Handwritten registers require validation checks.
            </p>
          </div>
        </div>
      </div>

      {/* OCR Results & Step 2 */}
      {uploadResult && (
        <div className="glass-card" style={{ borderLeft: '4px solid var(--color-success)', marginBottom: '2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'between', alignItems: 'center', marginBottom: '1.25rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle size={20} style={{ color: 'var(--color-success)' }} />
              <h3 style={{ fontSize: '1.1rem', fontWeight: '700' }}>OCR Pipeline Complete</h3>
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              Confidence Score: <strong style={{ color: 'var(--text-primary)' }}>{uploadResult.ocr_confidence}%</strong>
            </div>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <h4 style={{ fontSize: '0.85rem', fontWeight: '700', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
              Extracted QCR Schema Fields
            </h4>
            <div style={{ overflowX: 'auto', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem', textAlign: 'left' }}>
                <thead>
                  <tr style={{ backgroundColor: 'rgba(0, 0, 0, 0.3)', borderBottom: '1px solid var(--border-color)' }}>
                    <th style={{ padding: '0.65rem 1rem', fontWeight: '600' }}>Parameter Field</th>
                    <th style={{ padding: '0.65rem 1rem', fontWeight: '600' }}>Extracted Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(uploadResult.extracted_fields || {}).map(([key, val]) => (
                    <tr key={key} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '0.65rem 1rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)' }}>{key}</td>
                      <td style={{ padding: '0.65rem 1rem', fontWeight: '600' }}>{val}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'end' }}>
            <button 
              className="btn-primary" 
              onClick={handleRunAnalysis}
              disabled={isUploading}
            >
              Analyze Project Discrepancies <ArrowRight size={16} />
            </button>
          </div>
        </div>
      )}

      {/* CSS Animation injection */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
