import os
import sys

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

print("="*60)
print("RUNNING DATA INTEGRITY & PROVENANCE VERIFICATION")
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
    print("LOG: [OK] Synthetic QCR record generated from PMGSY base row.")
    print(f"   Report Number:  {base_rec['report_number']}")
    print(f"   Road Name:      {base_rec['road_name']}")
    print(f"   State/District: {base_rec['state']} / {base_rec['district']}")
    print(f"   Provenance Attached: {base_rec['provenance']}")
except Exception as e:
    print(f"LOG: [FAIL] Synthetic record generation failed: {e}")
    sys.exit(1)

# Step 4: DOCUMENT GENERATION
print("\nDOCUMENT GENERATION\n" + "-"*40)
try:
    from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
    output_image_path = os.path.join(ROOT_DIR, "data", "synthetic", "verify_data_integrity_qcr.png")
    generate_qcr_image(base_rec, output_image_path)
    if os.path.exists(output_image_path):
        print(f"LOG: [OK] Synthetic QCR document image generated successfully at: {output_image_path}")
    else:
        print("LOG: [FAIL] Generated QCR image path not found.")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Document image generation failed: {e}")
    sys.exit(1)

# Step 5: TEST SCENARIO MUTATION
print("\nTEST SCENARIO MUTATION\n" + "-"*40)
try:
    from ai_engine.testing.discrepancy_scenario_factory import create_scenario
    docs = create_scenario(base_rec, "numerical_mismatch")
    print(f"LOG: [OK] Controlled discrepancy scenario generated: numerical_mismatch")
    print(f"   QCR Value:            {docs[0]['fields']['measured_value']} {docs[0]['fields']['unit']}")
    print(f"   Test Datasheet Value: {docs[1]['fields']['measured_value']} {docs[1]['fields']['unit']} (OUTLIER mutation)")
    print(f"   QM E-Form Value:      {docs[2]['fields']['measured_value']} {docs[2]['fields']['unit']}")
    
    # Verify exact same project identity is preserved across all documents
    for doc in docs:
        print(f"   - Doc '{doc['document_id']}' Type '{doc['document_type']}' Project Code: {doc['fields']['project_code']}")
        assert doc['fields']['project_code'] == base_rec['project_code']
        assert doc['fields']['road_name'] == base_rec['road_name']
    print("LOG: [OK] Base road/project identity remains consistent across all document variants.")
except Exception as e:
    print(f"LOG: [FAIL] Scenario mutation validation failed: {e}")
    sys.exit(1)

# Step 6: PIPELINE ANALYSIS & DISCREPANCY DETECTION
print("\nPIPELINE ANALYSIS\n" + "-"*40)
try:
    from ai_engine.pipeline import analyze_documents
    results = analyze_documents(docs)
    print(f"LOG: [OK] Multi-document pipeline execution completed successfully.")
    print(f"   Documents Analyzed: {results['documents_analyzed']}")
    print(f"   Total Discrepancies: {results['summary']['total_discrepancies']}")
    
    discrepancies = results.get("discrepancies", [])
    has_numerical_mismatch = False
    for disc in discrepancies:
        print(f"   Discrepancy: Field '{disc['field']}', Type '{disc['discrepancy_type']}', Severity '{disc['severity']}'")
        print(f"     Explanation: {disc['explanation']}")
        if disc['discrepancy_type'] == 'numerical_mismatch' and disc['field'] == 'measured_value':
            has_numerical_mismatch = True
            
    if has_numerical_mismatch:
        print("LOG: [OK] Intended numerical discrepancy was successfully detected.")
    else:
        print("LOG: [FAIL] Numerical discrepancy was NOT detected.")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Pipeline analysis failed: {e}")
    sys.exit(1)

# Step 7: REPRODUCIBILITY VERIFICATION
print("\nREPRODUCIBILITY CHECK\n" + "-"*40)
try:
    # Re-run same selection
    selection_2 = select_deterministic_record(5)
    base_rec_2 = create_pmgsy_grounded_base_record(index=5, seed=42)
    docs_2 = create_scenario(base_rec_2, "numerical_mismatch")
    
    # Assert exact match
    assert selection_2["index"] == row_idx
    assert base_rec_2["report_number"] == base_rec["report_number"]
    assert docs_2[1]["fields"]["measured_value"] == docs[1]["fields"]["measured_value"]
    print("LOG: [OK] Re-running with same configuration produced identical source record and expected outcome.")
except Exception as e:
    print(f"LOG: [FAIL] Reproducibility verification failed: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("DATA INTEGRITY VERIFICATION COMPLETED: SUCCESS")
print("="*60)
