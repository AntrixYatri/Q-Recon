import os
import pandas as pd
from ai_engine.config.settings import DATA_DIR
from ai_engine.data_sources.pmgsy_loader import load_pmgsy_data

def get_pmgsy_filepath() -> str:
    path = os.path.join(DATA_DIR, "pmgsy", "pmgsy_karnataka_100.csv")
    if os.path.exists(path):
        return path
    fallback_path = os.path.join(DATA_DIR, "raw", "pmgsy_karnataka_100.csv")
    if os.path.exists(fallback_path):
        return fallback_path
    return None

def load_pmgsy_grounded_records() -> list:
    """
    Loads all records from the PMGSY-grounded dataset as a list of dicts.
    """
    path = get_pmgsy_filepath()
    if path:
        try:
            df = pd.read_csv(path)
            return df.to_dict(orient="records")
        except Exception as e:
            print(f"[Dataset Loader] Error reading CSV {path}: {e}")
            
    # Fallback to the settings-based loader
    df = load_pmgsy_data(100)
    return df.to_dict(orient="records")

def select_deterministic_record(index: int) -> dict:
    """
    Deterministically selects and validates a row from the PMGSY-grounded dataset.
    If the selected row is unsuitable (e.g. missing critical fields), falls back
    to a deterministic fallback strategy and logs/records why.
    """
    records = load_pmgsy_grounded_records()
    if not records:
        raise ValueError("PMGSY dataset could not be loaded and is empty.")
    
    total_records = len(records)
    selected_index = index % total_records
    
    def validate_row(row_candidate: dict) -> list:
        # Check required fields exist and are non-empty
        required_fields = ["State", "District", "Block", "Habitation Name", "Habitation ID", "Facility Name"]
        missing_fields = []
        for field in required_fields:
            val = row_candidate.get(field)
            if val is None or str(val).strip() == "" or pd.isna(val):
                missing_fields.append(field)
        return missing_fields

    row = records[selected_index]
    missing = validate_row(row)
    
    if missing:
        # Deterministic fallback strategy: find the first suitable row starting from index 0
        fallback_index = -1
        for idx, rec in enumerate(records):
            if not validate_row(rec):
                fallback_index = idx
                break
                
        if fallback_index != -1:
            print(f"[Dataset Loader Warning] Row {selected_index} is unsuitable (missing fields: {missing}). "
                  f"Using deterministic fallback row {fallback_index} instead.")
            row = records[fallback_index]
            selected_index = fallback_index
        else:
            raise ValueError(f"No suitable rows found in PMGSY dataset. Row {selected_index} has missing fields: {missing}.")
            
    return {
        "row": row,
        "index": selected_index
    }
