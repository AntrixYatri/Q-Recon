import os
import pandas as pd
from ai_engine.config.settings import DATA_RAW_DIR

KARNATAKA_URL = "https://raw.githubusercontent.com/pratapvardhan/rural-facilities-pmgsy/master/pmgsy_facilities_karnataka.csv"
LOCAL_CSV_FILENAME = "pmgsy_facilities_karnataka.csv"
LOCAL_SAMPLE_FILENAME = "pmgsy_karnataka_100.csv"

USEFUL_COLUMNS = [
    "State",
    "District",
    "Block",
    "Habitation Name",
    "Habitation ID",
    "Facility Name",
    "Address",
    "Facility Category",
    "Facility Subcategory",
    "Lattitude",
    "Longitude"
]

def load_pmgsy_data(sample_n: int = 100, force_reload: bool = False) -> pd.DataFrame:
    """
    Loads PMGSY facilities dataset from a local cache if available,
    otherwise downloads it and caches it to the disk.
    """
    local_sample_path = os.path.join(DATA_RAW_DIR, LOCAL_SAMPLE_FILENAME)
    local_full_path = os.path.join(DATA_RAW_DIR, LOCAL_CSV_FILENAME)

    # 1. Check if the pre-filtered sample exists
    if os.path.exists(local_sample_path) and not force_reload:
        try:
            return pd.read_csv(local_sample_path)
        except Exception as e:
            print(f"[PMGSY Loader] Failed reading local sample {local_sample_path}: {e}")

    # 2. Check if the full dataset is cached locally
    if os.path.exists(local_full_path) and not force_reload:
        try:
            df = pd.read_csv(local_full_path)
            return _clean_and_save_sample(df, local_sample_path, sample_n)
        except Exception as e:
            print(f"[PMGSY Loader] Failed reading local dataset {local_full_path}: {e}")

    # 3. Download from GitHub URL fallback
    print(f"[PMGSY Loader] Downloading dataset from GitHub URL: {KARNATAKA_URL}")
    try:
        df = pd.read_csv(KARNATAKA_URL)
        # Cache full dataset locally
        df.to_csv(local_full_path, index=False)
        return _clean_and_save_sample(df, local_sample_path, sample_n)
    except Exception as e:
        print(f"[PMGSY Loader Error] Failed downloading data: {e}")
        # In case of absolute offline failure, return a tiny hardcoded fallback DataFrame
        # to ensure the application runs.
        print("[PMGSY Loader] Offline failure. Generating a minimal local fallback dataset.")
        fallback_data = [{
            "State": "Karnataka",
            "District": "Belagavi",
            "Block": "Athni",
            "Habitation Name": "Shedbal Rural Section",
            "Habitation ID": "2901002003",
            "Facility Name": "Shedbal Govt Hospital Link Road",
            "Address": "Athni Road, Shedbal, Karnataka 591315",
            "Facility Category": "Health",
            "Facility Subcategory": "Primary Health Centre",
            "Lattitude": 16.732,
            "Longitude": 74.834
        }]
        fallback_df = pd.DataFrame(fallback_data)
        fallback_df.to_csv(local_sample_path, index=False)
        return fallback_df

def _clean_and_save_sample(df: pd.DataFrame, dest_path: str, n: int) -> pd.DataFrame:
    """
    Cleans the PMGSY columns, selects a sample of size n, and caches it locally.
    """
    # Filter columns that exist
    available_cols = [col for col in USEFUL_COLUMNS if col in df.columns]
    df_clean = df[available_cols].copy()
    
    # Rename Latitude if misspelled in original (e.g. Lattitude)
    if "Lattitude" in df_clean.columns:
        df_clean = df_clean.rename(columns={"Lattitude": "Latitude"})
    
    # Sample and cache
    sample_df = df_clean.sample(n=min(n, len(df_clean)), random_state=42).reset_index(drop=True)
    sample_df.to_csv(dest_path, index=False)
    return sample_df
