import os
import sys

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

print("="*60)
print("RUNNING PHASE 3 CLASSIFICATION & EXTRACTION VERIFICATION")
print("="*60)

try:
    from ai_engine.document_processing.document_classifier import classify_document
    from ai_engine.document_processing.extractor_router import get_extractor
    from ai_engine.pipeline import analyze_documents
    print("LOG: [OK] Pipeline and classification imports successful.")
except Exception as e:
    print(f"LOG: [FAIL] Imports failed: {str(e)}")
    sys.exit(1)

# CASE 1, 2, 3, 4: Classification Checks
print("\n--- CLASSIFICATION CHECKS ---")
cases = [
    ("qcr_report.png", "Quality Control Register for Pavement Thickness", "QCR"),
    ("test_lab_sheet.png", "Laboratory Material Test Datasheet", "TEST_DATASHEET"),
    ("qm_monitoring.png", "QM E-Form Quality Monitoring inspection report", "QM_EFORM"),
    ("other_report.txt", "Unrelated contractor invoice sheet", "UNKNOWN")
]

for filename, text, expected in cases:
    res = classify_document(filename, ocr_text=text)
    doc_type = res["document_type"]
    conf = res["confidence"]
    print(f"File '{filename}' classified as: {doc_type} (Confidence: {conf}) - Expected: {expected}")
    if doc_type != expected:
        print(f"LOG: [FAIL] Classification mismatch for {filename}.")
        sys.exit(1)
print("LOG: [OK] All document classifications match expectations.")

# CASE 5, 6, 7, 8, 9, 10: Multi-Document Mixed Integration Analysis
print("\n--- MIXED MULTI-DOCUMENT PIPELINE INTEGRATION CHECK ---")
mixed_docs = [
    # Document 1: QCR (Structured bypass representing a QCR file payload)
    {
        "document_id": "QCR-VAL-01",
        "document_type": "QCR",
        "fields": {
            "project_code": "PRJ-HACK-2026",
            "road_name": "Karimnagar Bypass Road 6",
            "measured_value": "150 mm",
            "unit": "mm",
            "quality_status": "COMPLIANT"
        }
    },
    # Document 2: Structured Test Datasheet Bypass (Unit normalisation cm -> mm, measured value mismatch)
    {
        "document_id": "DS-VAL-01",
        "document_type": "TEST_DATASHEET",
        "fields": {
            "project_code": "PRJ-HACK-2026",
            "road_name": "Karimnagar Bypass Road 6",
            "measured_value": "13 cm", # 130 mm (Numerical Mismatch OUTLIER!)
            "unit": "cm"
        }
    },
    # Document 3: Structured QM E-Form Bypass (Missing road_name field)
    {
        "document_id": "QM-VAL-01",
        "document_type": "QM_EFORM",
        "fields": {
            "project_code": "PRJ-HACK-2026",
            "measured_value": "150 mm",
            "unit": "mm",
            "quality_status": "COMPLIANT"
        }
    },
    # Document 4: Raw file path that fails classification (UNKNOWN) -> should generate a warning but not crash the run
    {
        "path": "random_contractor_invoice.jpg"
    }
]

try:
    results = analyze_documents(mixed_docs)
except Exception as e:
    print(f"LOG: [FAIL] Multi-document pipeline crashed: {str(e)}")
    sys.exit(1)

# Print Detailed report metrics
print(f"\nAnalysis ID: {results.get('analysis_id')}")
print(f"Processing Status: {results.get('processing_status')}")
print(f"Documents Analyzed: {results.get('documents_analyzed')}")
print(f"Linked Record Groups: {results.get('linked_record_groups')}")
print(f"Warnings Generated: {len(results.get('warnings', []))}")
for w in results.get("warnings", []):
    print(f"  - Warning: {w}")

print("\n--- Discrepancies Found ---")
discs = results.get("discrepancies", [])
print(f"Total Discrepancies: {len(discs)}")
for d in discs:
    print(f" - Discrepancy ID: {d['id']}")
    print(f"   Field: {d['field']}")
    print(f"   Type: {d['discrepancy_type']}")
    print(f"   Severity: {d['severity']}")
    print(f"   Confidence: {d['confidence']}")
    print(f"   Explanation: {d['explanation']}")

# Assertions
has_numerical = any(d["discrepancy_type"] == "numerical_mismatch" and d["field"] == "measured_value" for d in discs)
has_missing = any(d["discrepancy_type"] == "missing_value" and d["field"] == "road_name" for d in discs)
has_unknown_warning = any("skipped" in w or "unsupported" in w for w in results.get("warnings", []))

if has_numerical and has_missing and has_unknown_warning:
    print("\n" + "="*60)
    print("ALL PHASE 3 EXTRACTOR & CLASSIFICATION VERIFICATIONS PASSED: SUCCESS")
    print("="*60)
else:
    print("\n" + "="*60)
    print("LOG: [FAIL] Mismatches, warnings or missing alerts failed validation.")
    print("="*60)
    sys.exit(1)
