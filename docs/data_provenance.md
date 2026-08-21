# Data Provenance and Testing Architecture

This document describes the data sources, synthetic generation logic, three-level testing architecture, and data provenance mechanisms implemented in this project to ensure test repeatability, traceability, and high data integrity.

## 1. Source Dataset

The primary grounded dataset used is `pmgsy_karnataka_100.csv`, which is cached locally under:
- `data/pmgsy/pmgsy_karnataka_100.csv`

This file is a cleaned sample of 100 rural facilities in the state of Karnataka.

## 2. PMGSY-Grounded Concept

In this project, "PMGSY-grounded" means that the identity and structural features of generated synthetic records are anchored on real rural facilities and road coordinates from the PMGSY (Pradhan Mantri Gram Sadak Yojana) dataset. This guarantees that road names, districts, blocks, habitation names, and habitation IDs correspond to actual real-world geographical entities rather than arbitrary invented strings.

### Fields originating from the PMGSY dataset:
- `state`
- `district`
- `block`
- `habitation_name`
- `habitation_id`
- `facility_name` (mapped to canonical `road_name`)

### Synthetically generated fields:
- `report_number` (formatted as `QCR-PMGSY-2026-{index:05d}`)
- `project_name` (constructed using facility name)
- `project_code`
- `road_code`
- `road_length`
- `road_category`
- `inspection_date`
- `inspection_type`
- `inspector_name`
- `parameter`
- `required_value`
- `measured_value`
- `unit`
- `quality_status`
- `remarks`

## 3. Synthetic Record Generation

Synthetic records are generated deterministically starting from a deterministic PMGSY row selection:
1. A row is loaded from the `pmgsy_karnataka_100.csv` dataset using a stable row index.
2. The row details are validated to ensure required location fields exist.
3. The PMGSY-grounded generator `generate_pmgsy_qcr_record` combines these details with randomly chosen (but seed-controlled) test parameters (such as Pavement Thickness, Compaction, and Aggregate Size) to produce a mock QCR record.

## 4. Three-Level Testing Architecture

The project implements a strict three-level testing hierarchy:

### LEVEL 1: UNIT TESTS
- **Purpose:** Validate isolated logic (normalization, schema adaptation, date/unit cleaning).
- **Data Source:** Minimal, fast, deterministic hardcoded fixtures.
- **CSV Loading:** Unit tests do NOT load the PMGSY dataset to maintain high performance.

### LEVEL 2: INTEGRATION TESTS
- **Purpose:** Verify multi-document pipeline processing, record linking, and discrepancy calculations.
- **Data Source:** PMGSY-grounded records selected or generated deterministically via the fixture and scenario factories.

### LEVEL 3: END-TO-END TESTS
- **Purpose:** Validate the full pipeline flow:
  `PMGSY base record -> QCR Document Image generation -> OCR processing (EasyOCR) -> Layout line reconstruction -> Canonical fields extraction -> Comparative analysis against Test Datasheet and QM E-Form`.
- **Data Source:** Real generated QCR document images constructed from PMGSY-grounded records.

## 5. Controlled Discrepancies and Scenarios

The discrepancy scenario factory (`ai_engine/testing/discrepancy_scenario_factory.py`) creates controlled comparisons from a single PMGSY base record to test the discrepancy engine under various conditions:
- **`identical_documents`**: All documents are completely consistent.
- **`formatting_difference`**: Uses different text casings/spacings (e.g. "Karnataka" vs "karnataka ") to verify normalization.
- **`equivalent_units`**: Uses different equivalent units (e.g. "150 mm" vs "15 cm") to verify unit normalization.
- **`numerical_mismatch`**: Deliberately mutates a measured value outlier in the Test Datasheet (e.g., 120 mm vs 150 mm) to check numerical mismatch detection.
- **`missing_value`**: Deletes a configured field in one of the documents to test missing value alarms.
- **`date_format_difference`**: Uses different date formatting (e.g. "12 Aug 2026" vs "2026-08-12").
- **`actual_date_mismatch`**: Uses different date values to check date mismatch detection.
- **`majority_consensus`**: 3 documents with values `[150, 120, 150]` where `120` is recognized as the outlier.
- **`ambiguous_conflict`**: 2 documents disagreeing (1 vs 1) with no majority, resulting in an ambiguous tie.

## 6. Provenance Preservation

Every PMGSY-grounded synthetic record carries a `provenance` metadata block:
```json
{
    "data_origin": "pmgsy_grounded_synthetic",
    "source_dataset": "pmgsy_karnataka_100.csv",
    "source_row_index": 5,
    "synthetic_record_id": "pmgsy_qcr_00005",
    "generation_seed": 42,
    "generator": "pmgsy_qcr_generator"
}
```
This metadata travels with the record through the pipeline and is preserved in:
- The generated synthetic record.
- The pipeline canonical record's `ocr_metadata`.
- The final discrepancy audit logs and verification reports.

## 7. Dataset Terminology Disclaimer

All test records in this project are **synthetic records generated using PMGSY contextual structure**. They are NOT real official OMMAS inspection records, and they are marked clearly under the `pmgsy_grounded_synthetic` origin to prevent misrepresentation.
