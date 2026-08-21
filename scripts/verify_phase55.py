import os
import sys
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.document_processing.document_classifier import classify_document
from ai_engine.data_integration.unified_data_builder import build_canonical_record
from ai_engine.discrepancy_engine.discrepancy_detector import detect_discrepancies
from ai_engine.data_integration.record_linker import group_records, link_records
from ai_engine.pipeline import analyze_documents, process_mixed_document
from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
from ai_engine.synthetic_documents.test_datasheet_generator import generate_test_datasheet_image
from ai_engine.synthetic_documents.qm_eform_generator import generate_qm_eform_image

def main():
    print("================================================")
    print("PHASE 5.5 — AI ENGINE HARDENING VERIFICATION")
    print("================================================\n")

    # ----------------------------------------------------
    # SECTION 1 — MIXED DOCUMENT CLASSIFICATION
    # ----------------------------------------------------
    print("SECTION 1 — MIXED DOCUMENT CLASSIFICATION")
    docs_to_classify = [
        ("qcr_register.png", "quality control register PMGSY inspection details"),
        ("test_sheet.png", "material test datasheet grading sieve analysis"),
        ("nqm_form.png", "independent quality monitoring report observations checklist"),
        ("unknown_doc.png", "hello random text here")
    ]
    print(f"Total documents to classify: {len(docs_to_classify)}")
    for filename, text in docs_to_classify:
        res = classify_document(filename, ocr_text=text)
        print(f"  - File: {filename} -> Classified as: {res['document_type']} (Confidence: {res['confidence']})")
    print()

    # ----------------------------------------------------
    # SECTION 2 — RECORD LINKING
    # ----------------------------------------------------
    print("SECTION 2 — RECORD LINKING")
    # Project A
    rec_a1 = build_canonical_record("doc-a1", "QCR", {"project_code": "PRJ-AAA", "road_name": "T.Narasipur Link"})
    rec_a2 = build_canonical_record("doc-a2", "TEST_DATASHEET", {"project_code": "prj-aaa", "road_name": "T Narasipur Link"}) # Case & punct variant
    # Project B
    rec_b1 = build_canonical_record("doc-b1", "QCR", {"project_code": "PRJ-BBB", "road_name": "Road Beta"})
    rec_b2 = build_canonical_record("doc-b2", "TEST_DATASHEET", {"project_code": "PRJ-CCC", "road_name": "Road Beta"}) # Conflicting project code
    
    records = [rec_a1, rec_a2, rec_b1, rec_b2]
    groups = group_records(records)
    
    for i, g in enumerate(groups):
        linked_docs = [rec.get_value("document_id") for rec in g["records"]]
        print(f"  Project Group {i+1} (ID: {g['group_id']}):")
        print(f"    Linked documents: {linked_docs}")
    
    # Show link results
    link_a = link_records(rec_a1, rec_a2)
    print(f"  Linking Doc A1 & A2 (Case/Punct variation): Linked={link_a['linked']} (Confidence={link_a['confidence']})")
    link_b = link_records(rec_b1, rec_b2)
    print(f"  Linking Doc B1 & B2 (Conflicting Project Code): Linked={link_b['linked']}")
    print()

    # ----------------------------------------------------
    # SECTION 3 — NORMALIZATION
    # ----------------------------------------------------
    print("SECTION 3 — NORMALIZATION")
    rec_cm = build_canonical_record("qcr-cm", "QCR", {"measured_value": "15 cm", "inspection_date": "04/03/2026"})
    rec_mm = build_canonical_record("td-mm", "TEST_DATASHEET", {"measured_value": "150 mm", "inspection_date": "2026-03-04"})
    print(f"  Document QCR (15 cm, 04/03/2026) -> Normalized: Value={rec_cm.get_value('measured_value')} {rec_cm.get_value('unit')}, Date={rec_cm.get_value('inspection_date')}")
    print(f"  Document TD (150 mm, 2026-03-04) -> Normalized: Value={rec_mm.get_value('measured_value')} {rec_mm.get_value('unit')}, Date={rec_mm.get_value('inspection_date')}")
    
    # Verify discrepancy
    rec_cm.fields["project_code"].value = "PRJ-NORM"
    rec_mm.fields["project_code"].value = "PRJ-NORM"
    discs = detect_discrepancies([rec_cm, rec_mm])
    print(f"  Discrepancies found after normalization: {len(discs)}")
    print()

    # ----------------------------------------------------
    # SECTION 4 — LOW CONFIDENCE
    # ----------------------------------------------------
    print("SECTION 4 — LOW CONFIDENCE")
    # Low confidence scenario
    rec_high = build_canonical_record("doc-h", "QCR", {"project_code": "PRJ-LC", "measured_value": "150"}, {"ocr_confidence": 0.98})
    rec_low = build_canonical_record("doc-l", "TEST_DATASHEET", {"project_code": "PRJ-LC", "measured_value": "120"}, {"ocr_confidence": 0.50})
    
    discs_lc = detect_discrepancies([rec_high, rec_low])
    for disc in discs_lc:
        print(f"  Field: {disc['field']} Mismatch")
        print(f"    Consensus Value: {disc['metadata'].get('consensus_value')}")
        print(f"    Document list & OCR confidence values:")
        for doc in disc["documents"]:
            print(f"      - {doc['document_type']} ({doc['document_id']}): Value={doc['value']}, OCR Confidence={doc.get('ocr_confidence')}")
        print(f"    Resulting Discrepancy Confidence Score: {disc['confidence']} ({disc['confidence_level']})")
    print()

    # ----------------------------------------------------
    # SECTION 5 — MULTIPLE DISCREPANCIES
    # ----------------------------------------------------
    print("SECTION 5 — MULTIPLE DISCREPANCIES")
    rec_q = build_canonical_record("doc-q", "QCR", {
        "project_code": "PRJ-MULT", "measured_value": "150 mm", "required_value": "150 mm",
        "quality_status": "compliant", "inspection_date": "2026-03-04"
    })
    rec_t = build_canonical_record("doc-t", "TEST_DATASHEET", {
        "project_code": "PRJ-MULT", "measured_value": "120 mm", "required_value": "150 mm",
        "quality_status": "compliant", "inspection_date": "2026-03-04"
    })
    rec_m = build_canonical_record("doc-m", "QM_EFORM", {
        "project_code": "PRJ-MULT", "measured_value": "150 mm", "required_value": "150 mm",
        "quality_status": "non-compliant", "inspection_date": "2026-03-10"
    })
    mult_discs = detect_discrepancies([rec_q, rec_t, rec_m])
    print(f"  Total independent discrepancies detected: {len(mult_discs)}")
    for d in mult_discs:
        print(f"    - Field: {d['field']} | Type: {d['discrepancy_type']} | Severity: {d['severity']} | Confidence: {d['confidence']}")
        print(f"      Explanation: {d['explanation']}")
    print()

    # ----------------------------------------------------
    # SECTION 6 — DUPLICATE HANDLING
    # ----------------------------------------------------
    print("SECTION 6 — DUPLICATE HANDLING")
    dup_q1 = {
        "document_id": "dup-q1", "document_type": "QCR",
        "fields": {"project_code": "PRJ-DUP", "measured_value": "150", "required_value": "150"}
    }
    # Identical fields duplicate
    dup_q2 = {
        "document_id": "dup-q2", "document_type": "QCR",
        "fields": {"project_code": "PRJ-DUP", "measured_value": "150", "required_value": "150"}
    }
    res_dup = analyze_documents([dup_q1, dup_q2])
    print(f"  Received 2 documents (1 duplicate QCR).")
    print(f"  Processed Canonical Dataset size after deduplication: {res_dup['documents_analyzed']}")
    print()

    # ----------------------------------------------------
    # SECTION 7 — MIXED BATCH END-TO-END
    # ----------------------------------------------------
    print("SECTION 7 — MIXED BATCH END-TO-END")
    batch = [
        {"document_id": "A-QCR", "document_type": "QCR", "fields": {"project_code": "PRJ-A", "measured_value": "150"}},
        {"document_id": "B-TD", "document_type": "TEST_DATASHEET", "fields": {"project_code": "PRJ-B", "measured_value": "120"}},
        {"document_id": "A-TD", "document_type": "TEST_DATASHEET", "fields": {"project_code": "PRJ-A", "measured_value": "150"}},
        {"document_id": "B-QCR", "document_type": "QCR", "fields": {"project_code": "PRJ-B", "measured_value": "150"}}
    ]
    print(f"  Mixed batch inputs: {[d['document_id'] for d in batch]}")
    res_batch = analyze_documents(batch)
    print(f"  Analysis Status: {res_batch['processing_status']}")
    print(f"  Total Discrepancies detected across separated groups: {res_batch['summary']['total_discrepancies']}")
    for d in res_batch["discrepancies"]:
        print(f"    - Field: {d['field']} | Group ID: {d['group_id']} | Type: {d['discrepancy_type']}")
        print(f"      Involved Docs: {[doc['document_id'] for doc in d['documents']]}")
    print()

    # ----------------------------------------------------
    # SECTION 8 — PERFORMANCE
    # ----------------------------------------------------
    print("SECTION 8 — PERFORMANCE")
    
    # Setup paths for timing checks
    temp_qcr_path = os.path.join(ROOT_DIR, "data", "synthetic", "perf_qcr.png")
    temp_td_path = os.path.join(ROOT_DIR, "data", "synthetic", "perf_td.png")
    temp_qm_path = os.path.join(ROOT_DIR, "data", "synthetic", "perf_qm.png")

    try:
        base_record = create_pmgsy_grounded_base_record(index=22, seed=42)
        generate_qcr_image(base_record, temp_qcr_path)
        generate_test_datasheet_image(base_record, temp_td_path, variant="B")
        generate_qm_eform_image(base_record, temp_qm_path, variant="B")

        # Profile OCR Init / first run
        t_start = time.time()
        process_mixed_document(temp_qcr_path)
        t_qcr = time.time() - t_start
        print(f"  QCR processing time (first run/init): {t_qcr:.2f}s")

        # Profile second run (cached reader)
        t_start = time.time()
        process_mixed_document(temp_td_path)
        t_td = time.time() - t_start
        print(f"  Test Datasheet processing time: {t_td:.2f}s")

        t_start = time.time()
        process_mixed_document(temp_qm_path)
        t_qm = time.time() - t_start
        print(f"  QM E-Form processing time: {t_qm:.2f}s")

        # Profile mixed batch processing
        t_start = time.time()
        analyze_documents(batch)
        t_batch = time.time() - t_start
        print(f"  Structured mixed batch comparison time: {t_batch:.4f}s")

        times = {"QCR": t_qcr, "TEST_DATASHEET": t_td, "QM_EFORM": t_qm, "Structured Batch": t_batch}
        slowest = max(times, key=times.get)
        print(f"  Slowest operation: {slowest} ({times[slowest]:.2f}s)")
        
    finally:
        for path in [temp_qcr_path, temp_td_path, temp_qm_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
            json_path = os.path.splitext(path)[0] + ".json"
            if os.path.exists(json_path):
                try:
                    os.remove(json_path)
                except Exception:
                    pass

if __name__ == "__main__":
    main()
