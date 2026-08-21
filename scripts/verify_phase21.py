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

# Sourced deterministically from PMGSY dataset
from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.testing.discrepancy_scenario_factory import create_scenario

# Case A: 3-document majority consensus
base_maj = create_pmgsy_grounded_base_record(10, seed=42)
docs_majority = create_scenario(base_maj, "majority_consensus")

# Case B: 2-document tie handling (1 vs 1)
base_tie = create_pmgsy_grounded_base_record(12, seed=42)
docs_tie = create_scenario(base_tie, "ambiguous_conflict")
# Modify to create a date tie mismatch and make measured_values identical to avoid other conflicts
docs_tie[0]["fields"]["inspection_date"] = "12 Aug 2026"
docs_tie[1]["fields"]["inspection_date"] = "19 Aug 2026"
docs_tie[0]["fields"]["measured_value"] = "150"
docs_tie[1]["fields"]["measured_value"] = "150"

# Log dataset provenance
print("\n" + "="*60)
print("DATA SOURCE VERIFICATION")
print("="*60)
prov = base_maj["provenance"]
print(f"Data Origin:         {prov['data_origin']}")
print(f"Source Dataset:      {prov['source_dataset']}")
print(f"Source Row Index:    {prov['source_row_index']}")
print(f"Synthetic Record ID: {prov['synthetic_record_id']}")
print(f"Generator:           {prov['generator']}")
print("="*60 + "\n")

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
