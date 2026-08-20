import random
from datetime import datetime, timedelta
from ai_engine.config.settings import (
    STATES,
    DISTRICTS,
    BLOCKS,
    ROAD_CATEGORIES,
    INSPECTION_TYPES,
    PARAMETERS
)

def generate_qcr_record(index: int) -> dict:
    """
    Generates a single synthetic Quality Control Register (QCR) record dictionary.
    Preserves compliance distribution (80% compliant, 20% non-compliant).
    """
    state = random.choice(STATES)
    district = random.choice(DISTRICTS)
    block = random.choice(BLOCKS)
    parameter = random.choice(PARAMETERS)

    required_value = random.randint(
        parameter["required_min"],
        parameter["required_max"]
    )

    # 80% compliant, 20% non-compliant
    if random.random() < 0.8:
        measured_value = required_value + random.randint(0, 3)
        quality_status = "COMPLIANT"
    else:
        measured_value = required_value - random.randint(1, 10)
        quality_status = "NON-COMPLIANT"

    start_date = datetime(2025, 1, 1)
    inspection_date = start_date + timedelta(
        days=random.randint(0, 500)
    )

    record = {
        "image_id": f"qcr_{index:06d}",
        "report_number": f"QCR-2026-{index:05d}",
        "project_name": "Rural Road Improvement Project",
        "project_code": f"RR-{random.randint(2025, 2026)}-{random.randint(100, 999)}",
        
        "state": state,
        "district": district,
        "block": block,
        "village": f"Village {random.choice(['A', 'B', 'C', 'D', 'E'])}",
        
        "road_name": f"{random.choice(['ABC', 'XYZ', 'PQR', 'LMN'])} Village Road",
        "road_code": f"RD-{random.randint(10000, 99999)}",
        "road_length": round(random.uniform(1.0, 10.0), 1),
        "road_category": random.choice(ROAD_CATEGORIES),
        
        "inspection_date": inspection_date.strftime("%d/%m/%Y"),
        "inspection_type": random.choice(INSPECTION_TYPES),
        "inspector_name": f"Inspector {random.choice(['A', 'B', 'C', 'D'])}",
        "inspection_location": f"{block}, {district}",
        
        "parameter": parameter["name"],
        "required_value": required_value,
        "measured_value": measured_value,
        "unit": parameter["unit"],
        "quality_status": quality_status,
        
        "contractor_name": f"Contractor {random.choice(['A', 'B', 'C', 'D'])}",
        "agency_name": "Quality Control Agency",
        "remarks": (
            "Measurements within acceptable limits."
            if quality_status == "COMPLIANT"
            else "Measurement below required specification."
        )
    }

    return record
