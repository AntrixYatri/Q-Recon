def validate_qcr_record(record: dict) -> list:
    """
    Validates a structured QCR record.
    Returns a list of error strings if any anomalies are found, otherwise an empty list.
    """
    errors = []

    # Check required fields
    required_fields = [
        "image_id",
        "report_number",
        "state",
        "district",
        "block",
        "inspection_date",
        "inspector_name",
        "parameter",
        "required_value",
        "measured_value",
        "unit",
        "quality_status"
    ]

    for field in required_fields:
        if field not in record or record.get(field) is None:
            errors.append(f"Missing field: {field}")

    # Check road length if provided
    if "road_length" in record and record["road_length"] is not None:
        try:
            if float(record["road_length"]) <= 0:
                errors.append("Road length must be greater than 0")
        except ValueError:
            errors.append("Road length must be a numeric value")

    # Check measurement values
    try:
        req_val = float(record.get("required_value", 0))
        if req_val <= 0:
            errors.append("Required value must be greater than 0")
    except (ValueError, TypeError):
        errors.append("Required value must be a numeric value")

    try:
        meas_val = float(record.get("measured_value", 0))
        if meas_val <= 0:
            errors.append("Measured value must be greater than 0")
    except (ValueError, TypeError):
        errors.append("Measured value must be a numeric value")

    # Check compliance flag correctness
    status = record.get("quality_status")
    if status is not None:
        try:
            req_val = float(record.get("required_value", 0))
            meas_val = float(record.get("measured_value", 0))
            
            # Simple threshold rules matching the notebook logic
            expected_status = "COMPLIANT" if meas_val >= req_val else "NON-COMPLIANT"
            
            # Standardize status format (hyphens/underscores)
            normalized_status = str(status).upper().replace("_", "-")
            normalized_expected = expected_status.upper().replace("_", "-")
            
            if normalized_status != normalized_expected:
                errors.append(
                    f"Incorrect quality status: expected {normalized_expected}, got {status}"
                )
            
            if normalized_status not in ["COMPLIANT", "NON-COMPLIANT"]:
                errors.append("Invalid quality status")
        except (ValueError, TypeError):
            pass  # Error already handled by value type checks

    return errors
