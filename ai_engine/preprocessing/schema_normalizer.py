# Centralized schema aliases mapping configuration
FIELD_ALIASES = {
    # Road / Asset
    "road": "road_name",
    "road_name": "road_name",
    "name_of_road": "road_name",
    "road_code": "road_code",
    "code_of_road": "road_code",
    
    # Project
    "project_code": "project_code",
    "code_of_project": "project_code",
    "project": "project_code",
    
    # Habitation
    "habitation_id": "habitation_id",
    "habitation_code": "habitation_id",
    "habitation_name": "habitation_name",
    "habitation": "habitation_name",
    
    # Parameter / Table
    "parameter": "parameter",
    "test_parameter": "parameter",
    "unit": "unit",
    "quality_status": "quality_status",
    "status": "quality_status",
    "test_result": "quality_status",
    
    # Inspection
    "inspection_dt": "inspection_date",
    "inspection_date": "inspection_date",
    "date_of_inspection": "inspection_date",
    "test_date": "inspection_date",
    "test_dt": "inspection_date",
    "date_of_test": "inspection_date",
    "inspector": "inspector_name",
    "inspector_name": "inspector_name",
    "name_of_inspector": "inspector_name",
    
    # Location
    "district": "district",
    "district_name": "district",
    "state": "state",
    "state_name": "state",
    "block": "block",
    "block_name": "block",
    
    # Quality / Parameters
    "measured": "measured_value",
    "measured_value": "measured_value",
    "measured_val": "measured_value",
    "value_measured": "measured_value",
    "required": "required_value",
    "required_value": "required_value",
    "required_val": "required_value",
    "value_required": "required_value",
    
    # Administrative
    "contractor": "contractor_name",
    "contractor_name": "contractor_name",
    "agency": "agency_name",
    "agency_name": "agency_name"
}

def normalize_field_name(raw_name: str) -> str:
    """
    Translates raw input field name variants into their canonical field schema equivalent.
    If no alias is matched, returns the lowercase cleaned original input.
    """
    if not raw_name:
        return ""
        
    cleaned_name = str(raw_name).strip().lower().replace(" ", "_")
    return FIELD_ALIASES.get(cleaned_name, cleaned_name)
