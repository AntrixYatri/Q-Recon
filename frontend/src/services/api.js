const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Mock Data representing quality-monitoring records and their discrepancies
const MOCK_PROJECTS = [
  {
    id: "proj-101",
    road_name: "PMGSY - Karimnagar to Sultanabad Rural Link Route 4",
    package_id: "AP-04-102-R4",
    district: "Karimnagar",
    state: "Telangana",
    status: "DISCREPANCIES DETECTED",
    ocr_confidence: 91.2,
    documents_analyzed: 3,
    total_discrepancies: 4,
    critical: 2,
    warning: 1,
    minor: 1,
    discrepancies: [
      {
        id: "disc-101-1",
        field: "Sub-base thickness (GSB)",
        document_a: "Quality Control Register (QCR)",
        document_b: "QM E-Form (National Quality Monitor Report)",
        value_a: "150 mm",
        value_b: "120 mm",
        discrepancy_type: "Numerical Mismatch",
        severity: "critical",
        confidence: 96.5,
        explanation: "The Quality Control Register records a GSB layer thickness of 150 mm, while the National Quality Monitor's inspection E-Form reports only 120 mm, showing a deficit of 30 mm (20% below design specification)."
      },
      {
        id: "disc-101-2",
        field: "Compressive Strength of Concrete (M20)",
        document_a: "Test Datasheet (7-day Compressive Test)",
        document_b: "Quality Control Register (QCR)",
        value_a: "14.2 N/mm²",
        value_b: "21.5 N/mm²",
        discrepancy_type: "Numerical Mismatch",
        severity: "critical",
        confidence: 94.0,
        explanation: "Test Datasheet records 7-day strength as 14.2 N/mm² (below required 15 N/mm² target), but the QCR entry matches the 28-day target of 21.5 N/mm² on the exact same testing date, suggesting potential log falsification."
      },
      {
        id: "disc-101-3",
        field: "Date of Joint Inspection",
        document_a: "QM E-Form",
        document_b: "Inspection Log Sheet",
        value_a: "2026-08-10",
        value_b: "2026-08-15",
        discrepancy_type: "Date Inconsistency",
        severity: "warning",
        confidence: 99.0,
        explanation: "The official inspection e-form is dated 2026-08-10, but the inspector's handwritten log sheet (transcribed via OCR) shows the inspection took place on 2026-08-15, which is 5 days after the submission date."
      },
      {
        id: "disc-101-4",
        field: "Contractor Engineer Name",
        document_a: "Quality Control Register (QCR)",
        document_b: "Test Datasheet",
        value_a: "K. R. Rao",
        value_b: "K. Ramachandra Rao",
        discrepancy_type: "Text Inconsistency",
        severity: "minor",
        confidence: 88.0,
        explanation: "Fuzzy match indicates these represent the same individual, but spelling inconsistencies exist across documents."
      }
    ]
  },
  {
    id: "proj-102",
    road_name: "PMGSY - NH2 To Malthone Connectivity Bypass",
    package_id: "MP-12-BYP-09",
    district: "Sagar",
    state: "Madhya Pradesh",
    status: "CONSISTENT",
    ocr_confidence: 95.8,
    documents_analyzed: 2,
    total_discrepancies: 0,
    critical: 0,
    warning: 0,
    minor: 0,
    discrepancies: []
  },
  {
    id: "proj-103",
    road_name: "PMGSY - Gorakhpur Pipraich Road Section B",
    package_id: "UP-22-SEC-B",
    district: "Gorakhpur",
    state: "Uttar Pradesh",
    status: "DISCREPANCIES DETECTED",
    ocr_confidence: 89.5,
    documents_analyzed: 2,
    total_discrepancies: 2,
    critical: 0,
    warning: 2,
    minor: 0,
    discrepancies: [
      {
        id: "disc-103-1",
        field: "Liquid Limit of Soil (%)",
        document_a: "Test Datasheet",
        document_b: "Quality Control Register (QCR)",
        value_a: "38 %",
        value_b: "0.38 (Ratio)",
        discrepancy_type: "Unit Inconsistency",
        severity: "warning",
        confidence: 95.0,
        explanation: "Test Datasheet records liquid limit as 38%, whereas QCR reports it as a decimal ratio of 0.38. Normalized comparison matches, but unit formats are inconsistent."
      },
      {
        id: "disc-103-2",
        field: "Inspection Date",
        document_a: "QM E-Form",
        document_b: "Quality Control Register (QCR)",
        value_a: "2026-07-22",
        value_b: "2026-07-20",
        discrepancy_type: "Date Inconsistency",
        severity: "warning",
        confidence: 92.4,
        explanation: "A date mismatch exists: Inspection date in E-Form is 2026-07-22, while the QCR log lists the corresponding inspection on 2026-07-20."
      }
    ]
  }
];

export const getHealth = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error('API server response unhealthy');
    return await res.json();
  } catch (error) {
    console.warn("Backend /health check failed, using client status.", error);
    return { status: "offline", service: "QCR AI Mock Client" };
  }
};

export const uploadDocument = async (formData) => {
  try {
    const res = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData, // Contains file and optional project metadata
    });
    if (!res.ok) throw new Error('Document upload failed');
    return await res.json();
  } catch (error) {
    console.warn("Backend upload failed, simulating successful OCR response.", error);
    
    // Simulate OCR delay and response
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      success: true,
      analysis_id: "proj-101",
      filename: "sample_qcr_document.png",
      ocr_confidence: 91.2,
      extracted_fields: {
        report_number: "REP-2026-091",
        state: "Telangana",
        district: "Karimnagar",
        block: "Sultanabad",
        habitation_name: "Karimnagar Rural Link",
        habitation_id: "HAB-409-R4",
        facility_name: "Karimnagar to Sultanabad Rural Link Route 4",
        inspection_date: "2026-08-10",
        inspector_name: "A. K. Sharma",
        quality_status: "DISCREPANCIES DETECTED"
      }
    };
  }
};

export const analyzeProject = async (analysisId) => {
  try {
    const res = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ analysis_id: analysisId }),
    });
    if (!res.ok) throw new Error('AI analysis failed');
    return await res.json();
  } catch (error) {
    console.warn("Backend analysis failed, simulating discrepancy calculation.", error);
    await new Promise(resolve => setTimeout(resolve, 1500));
    return MOCK_PROJECTS.find(p => p.id === analysisId) || MOCK_PROJECTS[0];
  }
};

export const getResults = async (analysisId) => {
  try {
    const res = await fetch(`${API_BASE_URL}/results/${analysisId}`);
    if (!res.ok) throw new Error('Failed to retrieve results');
    return await res.json();
  } catch (error) {
    console.warn("Backend GET results failed, returning mock project data.", error);
    return MOCK_PROJECTS.find(p => p.id === analysisId) || MOCK_PROJECTS[0];
  }
};

export const getProjects = async () => {
  // Simulating list of all projects/roads
  return MOCK_PROJECTS;
};
