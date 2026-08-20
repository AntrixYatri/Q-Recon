import random
from datetime import datetime, timedelta
from ai_engine.config.settings import PARAMETERS, INSPECTION_TYPES

def generate_pmgsy_qcr_record(index: int, pmgsy_row: dict) -> dict:
    """
    Combines real PMGSY location/facility details with synthetic quality inspection readings.
    """
    # Extract real data from row
    state = pmgsy_row.get("State", "Karnataka")
    district = pmgsy_row.get("District", "")
    block = pmgsy_row.get("Block", "")
    habitation = pmgsy_row.get("Habitation Name", "")
    habitation_id = pmgsy_row.get("Habitation ID", "")
    facility = pmgsy_row.get("Facility Name", "")
    address = pmgsy_row.get("Address", "")
    category = pmgsy_row.get("Facility Category", "")
    subcategory = pmgsy_row.get("Facility Subcategory", "")

    # Generate synthetic metrics
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

    inspection_date = (
        datetime(2026, 1, 1)
        + timedelta(days=random.randint(0, 220))
    )

    return {
        "image_id": f"pmgsy_qcr_{index:05d}",
        "report_number": f"QCR-PMGSY-2026-{index:05d}",
        
        # Ground-truth PMGSY info
        "state": state,
        "district": district,
        "block": block,
        "habitation_name": habitation,
        "habitation_id": habitation_id,
        "facility_name": facility,
        "address": address,
        "facility_category": category,
        "facility_subcategory": subcategory,
        
        # Synthetic inspection details
        "inspection_date": inspection_date.strftime("%d/%m/%Y"),
        "inspection_type": random.choice(INSPECTION_TYPES),
        "inspector_name": f"Inspector {random.choice(['A', 'B', 'C', 'D'])}",
        
        # Quality parameters
        "parameter": parameter["name"],
        "required_value": required_value,
        "measured_value": measured_value,
        "unit": parameter["unit"],
        "quality_status": quality_status,
        
        "remarks": (
            "Measurement within acceptable limits."
            if quality_status == "COMPLIANT"
            else "Measurement below required specification."
        )
    }

# Post-processing logic inside data generation functions.
