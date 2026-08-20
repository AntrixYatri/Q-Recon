def compare_documents(analysis_id: str) -> dict:
    """
    Simulates loading mapped schemas for a project, running comparison rules,
    and returning structured discrepancy records.
    """
    # Core comparison rule implementation
    # Maps directly to the requested JSON response layout
    
    # In a full production system, this fetches records from local db/cache 
    # and compares them parameter-by-parameter. Here, we build the mapped structure.
    
    # Simulated projects database
    projects_db = {
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
                    "explanation": "Numerical comparison rules flagged a deficit of 30mm (20% below design thickness). QCR recorded 150mm but NQM report recorded 120mm."
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
                    "explanation": "Test Datasheet strength value is below required M20 threshold (14.2 vs 15.0 N/mm² at 7 days), but QCR recorded 21.5 N/mm² (28-day value logged as 7-day) on same date."
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
                    "explanation": "Inspection e-form file upload date is August 10, 2026, but the inspector's physical log sheet lists the field inspection date as August 15, 2026."
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
                    "explanation": "Fuzzy string match (88% similarity) indicates these represent the same individual, but naming records are spelling-inconsistent."
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

    return projects_db.get(analysis_id, projects_db["proj-101"])
