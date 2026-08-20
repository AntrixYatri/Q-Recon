# Fields grouped by logical category
IDENTIFICATION_FIELDS = ["document_id", "document_type", "report_number", "source_file"]
PROJECT_FIELDS = ["project_name", "project_code", "package_id"]
LOCATION_FIELDS = ["state", "district", "block", "village", "habitation_name", "habitation_id"]
ROAD_FIELDS = ["road_name", "road_code", "road_length", "road_category"]
INSPECTION_FIELDS = ["inspection_date", "inspection_type", "inspector_name", "inspection_location"]
QUALITY_FIELDS = ["parameter", "material_type", "layer_type", "required_value", "measured_value", "unit", "quality_status"]
ADMINISTRATIVE_FIELDS = ["contractor_name", "agency_name", "remarks"]

ALL_CANONICAL_FIELDS = (
    IDENTIFICATION_FIELDS +
    PROJECT_FIELDS +
    LOCATION_FIELDS +
    ROAD_FIELDS +
    INSPECTION_FIELDS +
    QUALITY_FIELDS +
    ADMINISTRATIVE_FIELDS
)

class CanonicalValue:
    """
    Wraps an individual extracted variable with metadata to track its source provenance.
    """
    def __init__(self, value, source_document=None, source_field=None, ocr_confidence=None):
        self.value = value
        self.source_document = source_document
        self.source_field = source_field
        self.ocr_confidence = ocr_confidence

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "source_document": self.source_document,
            "source_field": self.source_field,
            "ocr_confidence": self.ocr_confidence
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            return cls(value=data)
        return cls(
            value=data.get("value"),
            source_document=data.get("source_document"),
            source_field=data.get("source_field"),
            ocr_confidence=data.get("ocr_confidence")
        )

class CanonicalRecord:
    """
    A unified model representing a document's extracted fields, preserving field-level provenance.
    """
    def __init__(self, fields: dict = None):
        self.fields = {}
        for f in ALL_CANONICAL_FIELDS:
            self.fields[f] = CanonicalValue(value=None)
            
        if fields:
            for k, val in fields.items():
                if k in self.fields:
                    if isinstance(val, CanonicalValue):
                        self.fields[k] = val
                    elif isinstance(val, dict):
                        self.fields[k] = CanonicalValue.from_dict(val)
                    else:
                        self.fields[k] = CanonicalValue(value=val)

    def set_field(self, field_name: str, value, source_document=None, source_field=None, ocr_confidence=None):
        if field_name not in ALL_CANONICAL_FIELDS:
            raise KeyError(f"Field '{field_name}' is not defined in the canonical schema.")
        self.fields[field_name] = CanonicalValue(
            value=value,
            source_document=source_document,
            source_field=source_field,
            ocr_confidence=ocr_confidence
        )

    def get_value(self, field_name: str):
        return self.fields.get(field_name).value if field_name in self.fields else None

    def to_dict(self) -> dict:
        return {k: v.to_dict() for k, v in self.fields.items()}

    @classmethod
    def from_dict(cls, data: dict):
        record = cls()
        for k, v in data.items():
            if k in record.fields:
                record.fields[k] = CanonicalValue.from_dict(v)
        return record
