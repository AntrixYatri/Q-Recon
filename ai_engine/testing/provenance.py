def create_provenance_metadata(source_row_index: int, synthetic_record_id: str, generation_seed: int = 42) -> dict:
    """
    Constructs data provenance metadata for PMGSY-grounded synthetic records.
    """
    return {
        "data_origin": "pmgsy_grounded_synthetic",
        "source_dataset": "pmgsy_karnataka_100.csv",
        "source_row_index": source_row_index,
        "synthetic_record_id": synthetic_record_id,
        "generation_seed": generation_seed,
        "generator": "pmgsy_qcr_generator"
    }
