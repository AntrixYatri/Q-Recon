# Centralized configuration mapping canonical fields to comparison behaviors
COMPARISON_CONFIG = {
    # Quality / Parameters (Highest Importance)
    "measured_value": {
        "comparison_type": "numeric",
        "tolerance": 0.01,
        "importance": "high",
        "check_missing": True,
        "authoritative_source": "QCR"
    },
    "required_value": {
        "comparison_type": "numeric",
        "tolerance": 0.01,
        "importance": "high",
        "check_missing": True,
        "authoritative_source": "QCR"
    },
    "parameter": {
        "comparison_type": "text",
        "importance": "high",
        "check_missing": True
    },
    "unit": {
        "comparison_type": "text",
        "importance": "medium",
        "check_missing": True
    },
    "quality_status": {
        "comparison_type": "text",
        "importance": "high",
        "check_missing": True
    },
    
    # Identification
    "report_number": {
        "comparison_type": "text",
        "importance": "high",
        "check_missing": False
    },
    "project_code": {
        "comparison_type": "text",
        "importance": "high",
        "check_missing": False
    },
    
    # Location
    "state": {
        "comparison_type": "text",
        "importance": "medium",
        "check_missing": False
    },
    "district": {
        "comparison_type": "text",
        "importance": "medium",
        "check_missing": False
    },
    "block": {
        "comparison_type": "text",
        "importance": "medium",
        "check_missing": False
    },
    "village": {
        "comparison_type": "text",
        "importance": "low",
        "check_missing": False
    },
    
    # Asset
    "road_name": {
        "comparison_type": "text",
        "importance": "high",
        "check_missing": True
    },
    "road_code": {
        "comparison_type": "text",
        "importance": "high",
        "check_missing": False
    },
    
    # Inspection
    "inspection_date": {
        "comparison_type": "date",
        "importance": "high",
        "check_missing": True
    },
    "inspector_name": {
        "comparison_type": "text",
        "importance": "medium",
        "check_missing": False
    }
}
