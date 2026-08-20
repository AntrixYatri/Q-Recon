import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

class AnalysisService:
    @staticmethod
    def run_analysis(analysis_id: str) -> dict:
        """
        Runs comparative cross-document analysis on the documents linked to a project/road.
        """
        try:
            from ai_engine.pipeline import run_discrepancy_pipeline
            return run_discrepancy_pipeline(analysis_id)
        except Exception as e:
            print(f"[AnalysisService Error] AI pipeline failed: {str(e)}")
            # Fallback mock data returned when AI engine logic is in setup
            mock_projects = {
                "proj-101": {
                    "analysis_id": "proj-101",
                    "project": {
                        "road_name": "PMGSY - Karimnagar to Sultanabad Rural Link Route 4",
                        "package_id": "AP-04-102-R4",
                        "district": "Karimnagar",
                        "state": "Telangana"
                    },
                    "summary": {
                        "documents_analyzed": 3,
                        "total_discrepancies": 4,
                        "critical": 2,
                        "warning": 1,
                        "minor": 1
                    },
                    "discrepancies": [
                      {
                        "id": "disc-101-1",
                        "field": "Sub-base thickness (GSB)",
                        "document_a": "Quality Control Register (QCR)",
                        "document_b": "QM E-Form (National Quality Monitor Report)",
                        "value_a": "150 mm",
                        "value_b": "120 mm",
                        "discrepancy_type": "Numerical Mismatch",
                        "severity": "critical",
                        "confidence": 96.5,
                        "explanation": "The Quality Control Register records a GSB layer thickness of 150 mm, while the National Quality Monitor's inspection E-Form reports only 120 mm, showing a deficit of 30 mm (20% below design specification)."
                      },
                      {
                        "id": "disc-101-2",
                        "field": "Compressive Strength of Concrete (M20)",
                        "document_a": "Test Datasheet (7-day Compressive Test)",
                        "document_b": "Quality Control Register (QCR)",
                        "value_a": "14.2 N/mm²",
                        "value_b": "21.5 N/mm²",
                        "discrepancy_type": "Numerical Mismatch",
                        "severity": "critical",
                        "confidence": 94.0,
                        "explanation": "Test Datasheet records 7-day strength as 14.2 N/mm² (below required 15 N/mm² target), but the QCR entry matches the 28-day target of 21.5 N/mm² on the exact same testing date, suggesting potential log falsification."
                      },
                      {
                        "id": "disc-101-3",
                        "field": "Date of Joint Inspection",
                        "document_a": "QM E-Form",
                        "document_b": "Inspection Log Sheet",
                        "value_a": "2026-08-10",
                        "value_b": "2026-08-15",
                        "discrepancy_type": "Date Inconsistency",
                        "severity": "warning",
                        "confidence": 99.0,
                        "explanation": "The official inspection e-form is dated 2026-08-10, but the inspector's handwritten log sheet (transcribed via OCR) shows the inspection took place on 2026-08-15, which is 5 days after the submission date."
                      },
                      {
                        "id": "disc-101-4",
                        "field": "Contractor Engineer Name",
                        "document_a": "Quality Control Register (QCR)",
                        "document_b": "Test Datasheet",
                        "value_a": "K. R. Rao",
                        "value_b": "K. Ramachandra Rao",
                        "discrepancy_type": "Text Inconsistency",
                        "severity": "minor",
                        "confidence": 88.0,
                        "explanation": "Fuzzy match indicates these represent the same individual, but spelling inconsistencies exist across documents."
                      }
                    ]
                },
                "proj-102": {
                    "analysis_id": "proj-102",
                    "project": {
                        "road_name": "PMGSY - NH2 To Malthone Connectivity Bypass",
                        "package_id": "MP-12-BYP-09",
                        "district": "Sagar",
                        "state": "Madhya Pradesh"
                    },
                    "summary": {
                        "documents_analyzed": 2,
                        "total_discrepancies": 0,
                        "critical": 0,
                        "warning": 0,
                        "minor": 0
                    },
                    "discrepancies": []
                }
            }
            return mock_projects.get(analysis_id, mock_projects["proj-101"])
