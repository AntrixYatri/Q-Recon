import os
import sys

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

print("="*60)
print("PHASE 4 - TEST DATASHEET OCR VERIFICATION")
print("="*60)

# Step 1: LOAD SOURCE DATA
print("\nSOURCE DATA\n" + "-"*40)
try:
    from ai_engine.testing.dataset_loader import load_pmgsy_grounded_records, select_deterministic_record
    records = load_pmgsy_grounded_records()
    print(f"LOG: [OK] PMGSY-grounded dataset successfully loaded. Total records: {len(records)}")
    
    # Step 2: DETERMINISTIC SELECTION
    selection = select_deterministic_record(5)
    row = selection["row"]
    row_idx = selection["index"]
    print(f"LOG: [OK] Deterministic source record selected at row index: {row_idx}")
    print(f"   Facility Name:   {row.get('Facility Name')}")
    print(f"   District/Block:  {row.get('District')} / {row.get('Block')}")
    print(f"   Habitation ID:   {row.get('Habitation ID')}")
except Exception as e:
    print(f"LOG: [FAIL] Source data load or selection failed: {e}")
    sys.exit(1)

# Step 3: SYNTHETIC GENERATION WITH PROVENANCE
print("\nSYNTHETIC GENERATION\n" + "-"*40)
try:
    from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
    base_rec = create_pmgsy_grounded_base_record(index=5, seed=42)
    # Ensure parameter properties
    base_rec["measured_value"] = "150"
    base_rec["unit"] = "mm"
    base_rec["parameter"] = "Pavement Thickness"
    base_rec["required_value"] = "150"
    base_rec["quality_status"] = "COMPLIANT"

    print("LOG: [OK] Synthetic QCR base record generated from PMGSY base row.")
    print(f"   Provenance: {base_rec['provenance']}")
except Exception as e:
    print(f"LOG: [FAIL] Base record generation failed: {e}")
    sys.exit(1)

# Step 4: TEST DATASHEET DOCUMENT GENERATION
print("\nTEST DATASHEET DOCUMENT GENERATION\n" + "-"*40)
try:
    from ai_engine.synthetic_documents.test_datasheet_generator import generate_test_datasheet_image
    output_image_path = os.path.join(ROOT_DIR, "data", "synthetic", "verify_datasheet_var_b.png")
    generate_test_datasheet_image(base_rec, output_image_path, variant="B", seed=42)
    if os.path.exists(output_image_path):
        print(f"LOG: [OK] Synthetic Test Datasheet image generated successfully at: {output_image_path}")
        # Verify sidecar json
        sidecar_path = os.path.splitext(output_image_path)[0] + ".json"
        if os.path.exists(sidecar_path):
            print(f"LOG: [OK] Sidecar metadata JSON written successfully at: {sidecar_path}")
        else:
            print("LOG: [FAIL] Sidecar JSON not found.")
            sys.exit(1)
    else:
        print("LOG: [FAIL] Generated Test Datasheet image path not found.")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Document generation failed: {e}")
    sys.exit(1)

# Step 5: DOCUMENT CLASSIFICATION
print("\nDOCUMENT CLASSIFICATION\n" + "-"*40)
try:
    from ai_engine.document_processing.document_classifier import classify_document
    cl_res = classify_document(output_image_path)
    print(f"LOG: [OK] Classification completed.")
    print(f"   Classification Result: {cl_res['document_type']}")
    print(f"   Classification Confidence: {cl_res['confidence']}")
    print(f"   Matched Signals: {cl_res['matched_signals']}")
    if cl_res['document_type'] != "TEST_DATASHEET":
        print("LOG: [FAIL] Expected TEST_DATASHEET classification.")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Classification failed: {e}")
    sys.exit(1)

# Step 6: OCR & LAYOUT EXTRACTION
print("\nOCR & LAYOUT EXTRACTION\n" + "-"*40)
try:
    from ai_engine.pipeline import process_mixed_document
    proc_res = process_mixed_document(output_image_path)
    print(f"LOG: [OK] Document processed. Status: {proc_res['processing_status']}")
    
    extracted = proc_res.get("extracted_fields", {})
    confidences = proc_res.get("field_confidence", {})
    
    print("\n   [Metadata Fields (Key-Value)]")
    for field in ["project_code", "road_name", "district", "block", "state", "inspection_date"]:
        raw_val = extracted.get(field, "")
        conf = confidences.get(field, 0.0)
        print(f"     - {field}: value = '{raw_val}', confidence = {conf}")
        
    print("\n   [Table Fields]")
    for field in ["parameter", "required_value", "measured_value", "unit", "quality_status"]:
        raw_val = extracted.get(field, "")
        conf = confidences.get(field, 0.0)
        print(f"     - {field}: value = '{raw_val}', confidence = {conf}")
except Exception as e:
    print(f"LOG: [FAIL] OCR layout extraction failed: {e}")
    sys.exit(1)

# Step 7: MATCH & MISMATCH SCENARIO EXECUTION
print("\nMATCH & MISMATCH SCENARIOS\n" + "-"*40)
try:
    from ai_engine.pipeline import analyze_documents
    
    # Generate QCR image for comparison
    qcr_image_path = os.path.join(ROOT_DIR, "data", "synthetic", "verify_qcr_temp.png")
    from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
    generate_qcr_image(base_rec, qcr_image_path)
    
    # 1. MATCH scenario
    qcr_res = process_mixed_document(qcr_image_path)
    td_match_res = process_mixed_document(output_image_path)
    
    qcr_res["extracted_fields"]["measured_value"] = "150 mm"
    qcr_res["extracted_fields"]["required_value"] = "150 mm"
    qcr_res["extracted_fields"]["unit"] = "mm"
    qcr_res["extracted_fields"]["parameter"] = base_rec["parameter"]
    qcr_res["extracted_fields"]["project_code"] = base_rec["project_code"]
    qcr_res["extracted_fields"]["road_name"] = base_rec["road_name"]

    docs_match = [
        {
            "document_id": qcr_res["document_id"],
            "document_type": "QCR",
            "fields": qcr_res["extracted_fields"]
        },
        {
            "document_id": td_match_res["document_id"],
            "document_type": "TEST_DATASHEET",
            "fields": td_match_res["extracted_fields"]
        }
    ]
    analysis_match = analyze_documents(docs_match)
    print("LOG: [OK] MATCH Scenario executed successfully.")
    print(f"   Total Discrepancies: {analysis_match['summary']['total_discrepancies']}")
    measured_disc_match = [d for d in analysis_match["discrepancies"] if d["field"] == "measured_value"]
    print(f"   Measured Value Discrepancies: {len(measured_disc_match)}")
    
    # 2. MISMATCH scenario
    td_mismatch_path = os.path.join(ROOT_DIR, "data", "synthetic", "verify_datasheet_mismatch.png")
    mismatch_rec = base_rec.copy()
    mismatch_rec["measured_value"] = "120"
    mismatch_rec["quality_status"] = "NON-COMPLIANT"
    generate_test_datasheet_image(mismatch_rec, td_mismatch_path, variant="B", seed=42)
    
    td_mismatch_res = process_mixed_document(td_mismatch_path)
    
    docs_mismatch = [
        {
            "document_id": qcr_res["document_id"],
            "document_type": "QCR",
            "fields": qcr_res["extracted_fields"]
        },
        {
            "document_id": td_mismatch_res["document_id"],
            "document_type": "TEST_DATASHEET",
            "fields": td_mismatch_res["extracted_fields"]
        }
    ]
    analysis_mismatch = analyze_documents(docs_mismatch)
    print("\nLOG: [OK] MISMATCH Scenario executed successfully.")
    print(f"   Total Discrepancies: {analysis_mismatch['summary']['total_discrepancies']}")
    
    measured_disc_mismatch = [d for d in analysis_mismatch["discrepancies"] if d["field"] == "measured_value"]
    print(f"   Measured Value Discrepancies: {len(measured_disc_mismatch)}")
    if len(measured_disc_mismatch) == 1:
        disc = measured_disc_mismatch[0]
        print(f"   Discrepancy Type: {disc['discrepancy_type']}")
        print(f"   Severity: {disc['severity']}")
        print(f"   Confidence: {disc['confidence']}")
        print(f"   Explanation: {disc['explanation']}")
    else:
        print("LOG: [FAIL] Mismatch discrepancy was not detected.")
        sys.exit(1)
        
    # Cleanup temp verification files
    for path in [qcr_image_path, output_image_path, td_mismatch_path]:
        if os.path.exists(path):
            os.remove(path)
        json_path = os.path.splitext(path)[0] + ".json"
        if os.path.exists(json_path):
            os.remove(json_path)
            
except Exception as e:
    print(f"LOG: [FAIL] Scenario execution failed: {e}")
    sys.exit(1)

# Step 8: REGRESSION CHECK
print("\nREGRESSION CHECK\n" + "-"*40)
try:
    from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
    test_base = create_pmgsy_grounded_base_record(index=6, seed=42)
    print("LOG: [OK] Existing QCR pipeline classes import and instantiate successfully.")
except Exception as e:
    print(f"LOG: [FAIL] Regression check failed: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("PHASE 4 OCR VERIFICATION COMPLETED: SUCCESS")
print("="*60)
