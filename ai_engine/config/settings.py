import os
from pathlib import Path

# Base project directory relative to settings.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data subdirectories
DATA_DIR = BASE_DIR / "data"
DATA_RAW_DIR = DATA_DIR / "raw"
DATA_SYNTHETIC_DIR = DATA_DIR / "synthetic"
DATA_PROCESSED_DIR = DATA_DIR / "processed"

# Ensure folders exist
for folder in [DATA_DIR, DATA_RAW_DIR, DATA_SYNTHETIC_DIR, DATA_PROCESSED_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Constant value pools for synthetic QCR record generation
STATES = [
    "Uttar Pradesh",
    "Bihar",
    "Rajasthan",
    "Madhya Pradesh",
    "Odisha",
    "Jharkhand",
    "Chhattisgarh"
]

DISTRICTS = [
    "District A",
    "District B",
    "District C",
    "District D",
    "District E"
]

BLOCKS = [
    "Block A",
    "Block B",
    "Block C",
    "Block D"
]

ROAD_CATEGORIES = [
    "Rural Road",
    "Major Rural Road",
    "Link Road"
]

INSPECTION_TYPES = [
    "Routine Inspection",
    "Quality Inspection",
    "Final Inspection",
    "Material Inspection"
]

PARAMETERS = [
    {
        "name": "Pavement Thickness",
        "required_min": 50,
        "required_max": 60,
        "unit": "mm"
    },
    {
        "name": "Compaction",
        "required_min": 95,
        "required_max": 100,
        "unit": "%"
    },
    {
        "name": "Aggregate Size",
        "required_min": 20,
        "required_max": 40,
        "unit": "mm"
    }
]

# Field labels for extraction
FIELD_LABELS = {
    "report_number": ["Report Number"],
    "state": ["State"],
    "district": ["District"],
    "block": ["Block"],
    "habitation_name": ["Habitation"],
    "habitation_id": ["Habitation ID"],
    "facility_name": ["Facility"],
    "facility_category": ["Category"],
    "facility_subcategory": ["Subcategory"],
    "inspection_date": ["Inspection Date"],
    "inspection_type": ["Inspection Type"],
    "inspector_name": ["Inspector"],
    "quality_status": ["QUALITY STATUS"]
}

# Targeted OCR settings (e.g. crop coordinates for the Inspector field on the generated form layout)
TARGETED_INSPECTOR_CROP = {
    "x1": 350,
    "x2_max_offset": 700,
    "y1": 925,
    "y2_max_offset": 1005
}
