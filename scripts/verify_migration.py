import os
import sys

# Add root folder to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

print("="*60)
print("RUNNING AI ENGINE MIGRATION VERIFICATION")
print("="*60)

# 1. Verification of Imports
try:
    from ai_engine.data_generation.qcr_generator import generate_qcr_record
    from ai_engine.validation.qcr_validator import validate_qcr_record
    from ai_engine.synthetic_documents.qcr_image_generator import generate_qcr_image
    from ai_engine.extraction.line_reconstruction import group_into_lines
    from ai_engine.document_processing.layout_field_extractor import extract_from_reconstructed_lines
    from ai_engine.pipeline import analyze_document
    print("LOG: [OK] Stage 1: Imports validation passed.")
except Exception as e:
    print(f"LOG: [FAIL] Stage 1: Imports validation failed: {str(e)}")
    sys.exit(1)

# 2. Test Synthetic QCR Generation Workflow
try:
    record = generate_qcr_record(1)
    print("LOG: [OK] Stage 2: Synthetic QCR Record generated successfully.")
    print(f"   Record ID: {record['image_id']}")
    print(f"   Road: {record['road_name']}")
    print(f"   Parameter: {record['parameter']} (Required={record['required_value']}, Measured={record['measured_value']})")
except Exception as e:
    print(f"LOG: [FAIL] Stage 2: QCR Generation failed: {str(e)}")
    sys.exit(1)

# 3. Test QCR Record Validation
try:
    errors = validate_qcr_record(record)
    if not errors:
        print("LOG: [OK] Stage 3: QCR record validation returned zero errors.")
    else:
        print(f"LOG: [WARN] Stage 3: QCR record validation returned errors: {errors}")
except Exception as e:
    print(f"LOG: [FAIL] Stage 3: Validation function crashed: {str(e)}")
    sys.exit(1)

# 4. Test Synthetic Image Generation Workflow
try:
    output_image_path = os.path.join(ROOT_DIR, "data", "synthetic", "verify_qcr_000001.png")
    generate_qcr_image(record, output_image_path)
    if os.path.exists(output_image_path):
        print(f"LOG: [OK] Stage 4: QCR document image generated successfully at: {output_image_path}")
    else:
        print("LOG: [FAIL] Stage 4: QCR image path not found after generation.")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Stage 4: Image generation failed: {str(e)}")
    sys.exit(1)

# 5. Test Line Reconstruction Using Mock OCR Detections
try:
    mock_detections = [
        {"text": "State:", "confidence": 0.99, "x1": 100, "y1": 500, "x2": 200, "y2": 530, "xc": 150, "yc": 515, "width": 100, "height": 30},
        {"text": "Karnataka", "confidence": 0.98, "x1": 220, "y1": 500, "x2": 400, "y2": 530, "xc": 310, "yc": 515, "width": 180, "height": 30},
        {"text": "District:", "confidence": 0.95, "x1": 100, "y1": 550, "x2": 240, "y2": 580, "xc": 170, "yc": 565, "width": 140, "height": 30}
    ]
    
    lines = group_into_lines(mock_detections)
    if len(lines) == 2 and lines[0]["text"] == "State: Karnataka" and lines[1]["text"] == "District:":
        print("LOG: [OK] Stage 5: Line reconstruction grouped horizontal word boxes successfully.")
    else:
        print(f"LOG: [FAIL] Stage 5: Line reconstruction grouped incorrectly: {lines}")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Stage 5: Line reconstruction crashed: {str(e)}")
    sys.exit(1)

# 6. Test Layout Field Extraction
try:
    extracted = extract_from_reconstructed_lines(lines)
    if extracted.get("state") == "karnataka":
        print("LOG: [OK] Stage 6: Layout field extractor extracted parameters successfully.")
    else:
        print(f"LOG: [FAIL] Stage 6: Field extraction mapped incorrectly: {extracted}")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Stage 6: Field extraction crashed: {str(e)}")
    sys.exit(1)

# 7. Test AI Pipeline Interface
try:
    result = analyze_document("invalid_nonexistent_image_path.png")
    if result.get("processing_status") == "failed":
        print("LOG: [OK] Stage 7: Pipeline handler caught file errors cleanly without application crash.")
    else:
        print(f"LOG: [FAIL] Stage 7: Pipeline returned unexpected status on invalid path: {result}")
        sys.exit(1)
except Exception as e:
    print(f"LOG: [FAIL] Stage 7: Pipeline execution crashed: {str(e)}")
    sys.exit(1)

print("="*60)
print("ALL MIGRATED STAGES VERIFIED: SUCCESS")
print("="*60)
