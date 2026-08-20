import os
import sys

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

print("="*60)
print("RUNNING AI ENGINE PHASE 2 DISCREPANCY VERIFICATION")
print("="*60)

try:
    from ai_engine.pipeline import analyze_documents
    print("LOG: [OK] Pipeline imports successful.")
except Exception as e:
    print(f"LOG: [FAIL] Pipeline imports failed: {str(e)}")
    sys.exit(1)

# Set up comprehensive demo files representing multi-doc discrepancies
document_inputs = [
    # Document 1: QCR
    {
        "document_id": "TEST-QCR-01",
        "document_type": "QCR",
        "fields": {
            "project_code": "PRJ-KA-2026",
            "road_name": "Shedbal govt Hospital Bypass Route 4",
            "district": "Belagavi",
            "block": "Athni",
            "inspection_dt": "12 Aug 2026", # alias of inspection_date
            "parameter": "Pavement Thickness",
            "required_val": "150",          # alias of required_value
            "measured_val": "150 mm",       # alias of measured_value with unit
            "unit": "mm",
            "quality_status": "COMPLIANT"
        }
    },
    # Document 2: Test Datasheet (Equivalent Unit but Numerical Mismatch)
    {
        "document_id": "TEST-DS-01",
        "document_type": "TEST_DATASHEET",
        "fields": {
            "project_code": "PRJ-KA-2026",
            "road_name": "Shedbal Govt Hospital Bypass Route 4", # fuzzy text casing match
            "district": "belagavi",
            "block": "athni",
            "inspection_date": "2026-08-12",
            "parameter": "Pavement Thickness",
            "required_val": "15 cm",         # equivalent required thickness (150 mm)
            "measured_val": "12 cm",         # 12 cm = 120 mm (Numerical mismatch outlier!)
            "unit": "cm"
        }
    },
    # Document 3: QM E-Form (Missing field inspection_date)
    {
        "document_id": "TEST-QM-01",
        "document_type": "QM_EFORM",
        "fields": {
            "project_code": "PRJ-KA-2026",
            "road_name": "Shedbal govt Hospital Bypass Route 4",
            "district": "Belagavi",
            "block": "Athni",
            # inspection_date is missing (Missing value check!)
            "parameter": "Pavement Thickness",
            "required_val": "150",
            "measured_val": "150",
            "unit": "mm",
            "quality_status": "COMPLIANT"
        }
    }
]

# Run analysis
try:
    results = analyze_documents(document_inputs)
    print("LOG: [OK] Pipeline execution completed successfully.")
except Exception as e:
    print(f"LOG: [FAIL] Pipeline execution crashed: {str(e)}")
    sys.exit(1)

# Check results
summary = results.get("summary", {})
discrepancies = results.get("discrepancies", [])

print(f"LOG: Documents Analyzed: {results.get('documents_analyzed')}")
print(f"LOG: Total Discrepancies Found: {summary.get('total_discrepancies')}")
print(f"LOG: Critical: {summary.get('critical')}, High: {summary.get('high')}, Medium: {summary.get('medium')}, Low: {summary.get('low')}")

# Verify specific discrepancies
has_numerical = False
has_missing = False

for disc in discrepancies:
    f = disc.get("field")
    d_type = disc.get("discrepancy_type")
    sev = disc.get("severity")
    conf = disc.get("confidence")
    exp = disc.get("explanation")
    
    print(f"\nDiscrepancy ID: {disc.get('discrepancy_id')}")
    print(f" - Field: {f}")
    print(f" - Type: {d_type}")
    print(f" - Severity: {sev}")
    print(f" - Confidence: {conf}")
    print(f" - Explanation: {exp}")
    
    if d_type == "numerical_mismatch" and f == "measured_value":
        has_numerical = True
    if d_type == "missing_value" and f == "inspection_date":
        has_missing = True

# Verification assertion
if has_numerical and has_missing:
    print("\n" + "="*60)
    print("ALL MIGRATED PHASE 2 LOGIC VERIFIED: SUCCESS")
    print("="*60)
else:
    print("\n" + "="*60)
    print("LOG: [FAIL] Did not detect all expected discrepancy types.")
    print("="*60)
    sys.exit(1)
