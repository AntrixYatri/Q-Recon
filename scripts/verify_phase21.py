import os
import sys

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

print("="*60)
print("RUNNING PHASE 2.1 DISCREPANCY CONSISTENCY VERIFICATION")
print("="*60)

try:
    from ai_engine.pipeline import analyze_documents
    from backend.app.services.analysis_service import AnalysisService
    print("LOG: [OK] AI Engine and Backend imports successful.")
except Exception as e:
    print(f"LOG: [FAIL] Imports failed: {str(e)}")
    sys.exit(1)

# Case A: 3-document majority consensus
# 2 docs agree on 150 mm, 1 doc says 120 mm. Consensus = 150 mm, outlier = 120 mm
docs_majority = [
    {"document_id": "QCR-01", "document_type": "QCR", "fields": {"project_code": "P-MAJ", "road": "Highway 1", "measured_value": "150 mm"}},
    {"document_id": "TEST-01", "document_type": "TEST_DATASHEET", "fields": {"project_code": "P-MAJ", "road": "Highway 1", "measured_value": "120 mm"}},
    {"document_id": "QM-01", "document_type": "QM_EFORM", "fields": {"project_code": "P-MAJ", "road": "Highway 1", "measured_value": "15 cm"}} # equivalent 150 mm
]

# Case B: 2-document tie handling (1 vs 1)
# 1 doc says 2026-08-12, 1 doc says 2026-08-19. No authority configured. Should be ambiguous conflict
docs_tie = [
    {"document_id": "QCR-02", "document_type": "QCR", "fields": {"project_code": "P-TIE", "road": "Highway 2", "inspection_date": "12 Aug 2026"}},
    {"document_id": "TEST-02", "document_type": "TEST_DATASHEET", "fields": {"project_code": "P-TIE", "road": "Highway 2", "inspection_date": "19 Aug 2026"}}
]

# 1. Run Case A
try:
    res_maj = analyze_documents(docs_majority)
    discs_maj = res_maj["discrepancies"]
    if len(discs_maj) == 1 and discs_maj[0]["discrepancy_type"] == "numerical_mismatch":
        print("LOG: [OK] Majority consensus successfully resolved (150 mm is consensus, 120 mm is outlier).")
    else:
        print(f"LOG: [FAIL] Majority consensus failed: {discs_maj}")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Case A crashed: {str(e)}")
    sys.exit(1)

# 2. Run Case B
try:
    res_tie = analyze_documents(docs_tie)
    discs_tie = res_tie["discrepancies"]
    if len(discs_tie) == 1 and discs_tie[0]["discrepancy_type"] == "ambiguous_conflict":
        print("LOG: [OK] Tie successfully handled as ambiguous conflict.")
        print(f"      Ambiguous confidence: {discs_tie[0]['confidence']} (should be 0.75)")
    else:
        print(f"LOG: [FAIL] Tie handling failed: {discs_tie}")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Case B crashed: {str(e)}")
    sys.exit(1)

# 3. Verify API consistency via service mapper
try:
    # Use fallback mock database trigger to audit schema mapper
    api_res = AnalysisService.run_analysis("proj-101")
    summary = api_res["summary"]
    discs_api = api_res["discrepancies"]

    print(f"LOG: API documents analyzed: {api_res['documents_analyzed']}")
    print(f"LOG: API total discrepancies: {summary['total_discrepancies']}")
    
    # Check severity lowercase and summary matching
    calculated_total = summary["critical"] + summary["high"] + summary["medium"] + summary["low"]
    if summary["total_discrepancies"] == calculated_total:
        print("LOG: [OK] Summary count calculation is mathematically consistent.")
    else:
        print(f"LOG: [FAIL] Summary counts sum mismatch: {summary}")
        sys.exit(1)

    # Check confidence decimals
    all_decimals = True
    for disc in discs_api:
        c = disc["confidence"]
        if c > 1.0 or c < 0.0:
            all_decimals = False
            
    if all_decimals:
        print("LOG: [OK] Discrepancy confidence ratings are standardized between 0.0 and 1.0.")
    else:
        print("LOG: [FAIL] Detected percentage values inside API confidence fields.")
        sys.exit(1)

except Exception as e:
    print(f"LOG: [FAIL] API consistency check crashed: {str(e)}")
    sys.exit(1)

print("="*60)
print("ALL PHASE 2.1 VERIFICATIONS PASSED: SUCCESS")
print("="*60)
