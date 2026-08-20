import uuid
from ai_engine.data_integration.canonical_schema import CanonicalRecord
from ai_engine.preprocessing.field_normalizer import normalize_field_value

def link_records(record_a: CanonicalRecord, record_b: CanonicalRecord) -> dict:
    """
    Compares two canonical records and determines if they represent the same road project.
    Uses explainable deterministic logic and returns confidence scoring.
    """
    matched_on = []
    confidence = 0.0

    # Extract cleaned comparison strings
    p_code_a = normalize_field_value("project_code", record_a.get_value("project_code"))
    p_code_b = normalize_field_value("project_code", record_b.get_value("project_code"))
    
    pkg_a = normalize_field_value("package_id", record_a.get_value("package_id"))
    pkg_b = normalize_field_value("package_id", record_b.get_value("package_id"))
    
    r_code_a = normalize_field_value("road_code", record_a.get_value("road_code"))
    r_code_b = normalize_field_value("road_code", record_b.get_value("road_code"))
    
    hab_id_a = normalize_field_value("habitation_id", record_a.get_value("habitation_id"))
    hab_id_b = normalize_field_value("habitation_id", record_b.get_value("habitation_id"))
    
    road_name_a = normalize_field_value("road_name", record_a.get_value("road_name"))
    road_name_b = normalize_field_value("road_name", record_b.get_value("road_name"))
    
    dist_a = normalize_field_value("district", record_a.get_value("district"))
    dist_b = normalize_field_value("district", record_b.get_value("district"))
    
    block_a = normalize_field_value("block", record_a.get_value("block"))
    block_b = normalize_field_value("block", record_b.get_value("block"))

    date_a = normalize_field_value("inspection_date", record_a.get_value("inspection_date"))
    date_b = normalize_field_value("inspection_date", record_b.get_value("inspection_date"))

    # Rule 1: Project Code matches exactly (Strongest Link)
    if p_code_a and p_code_b and p_code_a == p_code_b:
        matched_on.append("project_code")
        confidence = max(confidence, 0.98)

    # Rule 2: Package ID matches exactly
    if pkg_a and pkg_b and pkg_a == pkg_b:
        matched_on.append("package_id")
        confidence = max(confidence, 0.96)

    # Rule 3: Road Code matches exactly
    if r_code_a and r_code_b and r_code_a == r_code_b:
        matched_on.append("road_code")
        confidence = max(confidence, 0.95)

    # Rule 4: Habitation ID matches exactly
    if hab_id_a and hab_id_b and hab_id_a == hab_id_b:
        matched_on.append("habitation_id")
        confidence = max(confidence, 0.92)

    # Rule 5: Road name + Location match (District & Block)
    if road_name_a and road_name_b and road_name_a == road_name_b:
        matched_on.append("road_name")
        temp_conf = 0.70
        if dist_a and dist_b and dist_a == dist_b:
            matched_on.append("district")
            temp_conf += 0.15
        if block_a and block_b and block_a == block_b:
            matched_on.append("block")
            temp_conf += 0.08
        if date_a and date_b and date_a == date_b:
            matched_on.append("inspection_date")
            temp_conf += 0.05
        confidence = max(confidence, min(temp_conf, 0.95))

    linked = confidence >= 0.75
    return {
        "linked": linked,
        "confidence": confidence if linked else 0.0,
        "matched_on": matched_on
    }

def group_records(records: list) -> list:
    """
    Partitions a list of CanonicalRecords into linked groups.
    Each group gets a unique 'group_id' and lists its matching documents.
    """
    groups = []
    # To keep track of record indexing
    unassigned = list(range(len(records)))

    while unassigned:
        base_idx = unassigned.pop(0)
        base_rec = records[base_idx]
        current_group = [base_rec]

        i = 0
        while i < len(unassigned):
            cand_idx = unassigned[i]
            cand_rec = records[cand_idx]
            
            link_res = link_records(base_rec, cand_rec)
            if link_res["linked"]:
                current_group.append(cand_rec)
                unassigned.pop(i)
            else:
                i += 1

        # Generate a descriptive group_id using project codes or road name if possible
        road_name = base_rec.get_value("road_name")
        road_code = base_rec.get_value("road_code")
        project_code = base_rec.get_value("project_code")

        if project_code:
            group_id = f"PROJECT-{project_code.upper().replace(' ', '-')}"
        elif road_code:
            group_id = f"ROAD-{road_code.upper().replace(' ', '-')}"
        elif road_name:
            group_id = f"ROAD-NAME-{road_name.upper().replace(' ', '-')[:15]}"
        else:
            group_id = f"GROUP-{str(uuid.uuid4())[:8].upper()}"

        groups.append({
            "group_id": group_id,
            "records": current_group
        })

    return groups
