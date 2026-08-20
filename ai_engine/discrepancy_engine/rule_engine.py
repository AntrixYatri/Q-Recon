from decimal import Decimal
from ai_engine.data_integration.canonical_schema import CanonicalRecord

def check_logical_rules(record: CanonicalRecord) -> list:
    """
    Evaluates deterministic business logic rules on a CanonicalRecord.
    Returns a list of logical inconsistency discrepancy dictionaries.
    """
    discrepancies = []
    
    meas_val = record.get_value("measured_value")
    req_val = record.get_value("required_value")
    status = record.get_value("quality_status")

    if meas_val is not None and req_val is not None and status is not None:
        try:
            m = Decimal(str(meas_val))
            r = Decimal(str(req_val))
            
            normalized_status = str(status).upper().strip().replace("_", "-")
            
            # Rule 1: Measured < Required but status claimed COMPLIANT
            if m < r and normalized_status == "COMPLIANT":
                discrepancies.append({
                    "discrepancy_type": "logical_inconsistency",
                    "field": "quality_status",
                    "explanation": (
                        f"Logical conflict: Record reports status as COMPLIANT, "
                        f"but measured value ({m}) is less than required value ({r})."
                    ),
                    "severity": "HIGH",
                    "confidence": 0.95
                })
            
            # Rule 2: Measured >= Required but status claimed NON-COMPLIANT
            elif m >= r and normalized_status == "NON-COMPLIANT":
                discrepancies.append({
                    "discrepancy_type": "logical_inconsistency",
                    "field": "quality_status",
                    "explanation": (
                        f"Logical conflict: Record reports status as NON-COMPLIANT, "
                        f"but measured value ({m}) meets or exceeds required value ({r})."
                    ),
                    "severity": "MEDIUM",
                    "confidence": 0.90
                })
        except Exception:
            # Swallow number parsing errors here as they are handled by numerical comparators
            pass

    return discrepancies
