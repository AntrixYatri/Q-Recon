import os
import json
from PIL import Image, ImageDraw
from ai_engine.synthetic_documents.qcr_image_generator import get_system_font

def generate_qm_eform_image(record: dict, output_path: str, variant: str = "A", seed: int = 42) -> Image.Image:
    """
    Generates a structured QM E-Form document image from record details.
    Supports three distinct layout variants (A, B, C).
    Writes a sidecar JSON file recording the generation details.
    """
    # Load fonts
    title_font = get_system_font(44)
    section_font = get_system_font(28)
    label_font = get_system_font(22)
    text_font = get_system_font(22)

    # Document Canvas Sizes
    WIDTH = 1600
    HEIGHT = 2200

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    margin = 100
    y = 70

    # Clean quality status
    status_val = str(record.get("quality_status", "")).lower()
    is_compliant = "non" not in status_val and ("compliant" in status_val or "pass" in status_val or "yes" in status_val or "approved" in status_val or status_val == "1")

    if variant == "A":
        # VARIANT A: Vertical form with checklist checkboxes
        draw.text((WIDTH // 2, y), "QUALITY MONITORING INSPECTION FORM", font=title_font, fill="black", anchor="ma")
        y += 80
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=3)
        y += 60

        kv_data = [
            ("Project Code", record.get("project_code", "")),
            ("Road Name", record.get("road_name", "")),
            ("State", record.get("state", "")),
            ("District", record.get("district", "")),
            ("Block", record.get("block", "")),
            ("Habitation Name", record.get("habitation_name", "")),
            ("Habitation ID", record.get("habitation_id", "")),
            ("Monitoring Date", record.get("inspection_date", "")),
            ("Monitoring Inspector", record.get("inspector_name", "")),
            ("Parameter", record.get("parameter", "")),
            ("Required Value", record.get("required_value", "")),
            ("Measured Value", record.get("measured_value", "")),
            ("Unit", record.get("unit", ""))
        ]

        for label, val in kv_data:
            draw.text((margin, y), f"{label}:", font=label_font, fill="black")
            draw.text((margin + 320, y), str(val), font=text_font, fill="black")
            y += 65

        # Checkbox field
        draw.text((margin, y), "Status:", font=label_font, fill="black")
        comp_check = "[X] Compliant" if is_compliant else "[ ] Compliant"
        non_comp_check = "[X] Non-Compliant" if not is_compliant else "[ ] Non-Compliant"
        draw.text((margin + 320, y), f"{comp_check}      {non_comp_check}", font=text_font, fill="black")
        y += 75

        # Remarks field
        remarks = record.get("remarks", "Measurement within acceptable limits" if is_compliant else "Deficiencies observed during inspection")
        draw.text((margin, y), "Remarks:", font=label_font, fill="black")
        draw.text((margin + 320, y), remarks, font=text_font, fill="black")

    elif variant == "B":
        # VARIANT B: Sectioned form with observations table
        draw.text((WIDTH // 2, y), "QUALITY MONITORING REPORT", font=title_font, fill="black", anchor="ma")
        y += 80
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=3)
        y += 60

        # Section 1: Project Details
        draw.text((margin, y), "1. PROJECT DETAILS", font=section_font, fill="black")
        y += 45
        left_col_x = margin + 30
        right_col_x = WIDTH // 2 + 50
        
        draw.text((left_col_x, y), "Project Code:", font=label_font, fill="black")
        draw.text((left_col_x + 220, y), str(record.get("project_code", "")), font=text_font, fill="black")
        
        draw.text((right_col_x, y), "Road Name:", font=label_font, fill="black")
        draw.text((right_col_x + 220, y), str(record.get("road_name", "")), font=text_font, fill="black")
        y += 55

        draw.text((left_col_x, y), "Habitation ID:", font=label_font, fill="black")
        draw.text((left_col_x + 220, y), str(record.get("habitation_id", "")), font=text_font, fill="black")
        y += 80

        # Section 2: Inspection Details
        draw.text((margin, y), "2. INSPECTION DETAILS", font=section_font, fill="black")
        y += 45
        draw.text((left_col_x, y), "Monitoring Date:", font=label_font, fill="black")
        draw.text((left_col_x + 220, y), str(record.get("inspection_date", "")), font=text_font, fill="black")
        
        draw.text((right_col_x, y), "Monitoring Inspector:", font=label_font, fill="black")
        draw.text((right_col_x + 220, y), str(record.get("inspector_name", "")), font=text_font, fill="black")
        y += 55

        draw.text((left_col_x, y), "State/District/Block:", font=label_font, fill="black")
        loc_str = f"{record.get('state', '')}, {record.get('district', '')}, {record.get('block', '')}"
        draw.text((left_col_x + 220, y), loc_str, font=text_font, fill="black")
        y += 90

        # Section 3: Quality Observations Table
        draw.text((margin, y), "3. QUALITY OBSERVATIONS", font=section_font, fill="black")
        y += 55

        columns = [
            ("Parameter", 450),
            ("Required", 220),
            ("Measured", 220),
            ("Unit", 150),
            ("Status", 300)
        ]
        row_height = 65

        # Draw Table Headers
        x = margin
        for header, width in columns:
            draw.rectangle((x, y, x + width, y + row_height), outline="black", width=2)
            draw.text((x + 10, y + 18), header, font=label_font, fill="black")
            x += width

        # Draw Data Row
        y += row_height
        x = margin
        
        status_text = "[X] Pass  [ ] Fail" if is_compliant else "[ ] Pass  [X] Fail"
        values = [
            record.get("parameter", ""),
            str(record.get("required_value", "")),
            str(record.get("measured_value", "")),
            record.get("unit", ""),
            status_text
        ]
        for val, (_, width) in zip(values, columns):
            draw.rectangle((x, y, x + width, y + row_height), outline="black", width=2)
            draw.text((x + 10, y + 18), str(val), font=text_font, fill="black")
            x += width
        y += row_height + 70

        # Section 4: Remarks
        draw.text((margin, y), "4. REMARKS", font=section_font, fill="black")
        y += 45
        remarks = record.get("remarks", "Measurement within acceptable limits" if is_compliant else "Deficiencies observed during inspection")
        draw.text((margin + 30, y), remarks, font=text_font, fill="black")

    else:
        # VARIANT C: Independent Quality Checklist
        draw.text((WIDTH // 2, y), "INDEPENDENT QUALITY MONITORING CHECKLIST", font=title_font, fill="black", anchor="ma")
        y += 80
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=3)
        y += 60

        row_h = 75
        col_w = (WIDTH - 2 * margin) // 2

        # Row 1: Project Code | Monitoring Inspector
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Project Code:", font=label_font, fill="black")
        draw.text((margin + 200, y + 20), str(record.get("project_code", "")), font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Monitoring Inspector:", font=label_font, fill="black")
        draw.text((margin + col_w + 250, y + 20), str(record.get("inspector_name", "")), font=text_font, fill="black")
        y += row_h

        # Row 2: Road Name | Monitoring Date
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Road Name:", font=label_font, fill="black")
        draw.text((margin + 200, y + 20), str(record.get("road_name", "")), font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Monitoring Date:", font=label_font, fill="black")
        draw.text((margin + col_w + 250, y + 20), str(record.get("inspection_date", "")), font=text_font, fill="black")
        y += row_h

        # Row 3: District / Block / State | Habitation
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "District / Block / State:", font=label_font, fill="black")
        loc_str = f"{record.get('district', '')} / {record.get('block', '')} / {record.get('state', '')}"
        draw.text((margin + 250, y + 20), loc_str, font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Habitation ID:", font=label_font, fill="black")
        draw.text((margin + col_w + 250, y + 20), str(record.get("habitation_id", "")), font=text_font, fill="black")
        y += row_h

        # Row 4: Parameter & Required | Measured & Unit
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Parameter / Required:", font=label_font, fill="black")
        param_req = f"{record.get('parameter', '')} ({record.get('required_value', '')})"
        draw.text((margin + 250, y + 20), param_req, font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Measured / Unit:", font=label_font, fill="black")
        meas_unit = f"{record.get('measured_value', '')} {record.get('unit', '')}"
        draw.text((margin + col_w + 250, y + 20), meas_unit, font=text_font, fill="black")
        y += row_h

        # Row 5: Checklist Status | Remarks
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Compliant:", font=label_font, fill="black")
        comp_box = "[X]" if is_compliant else "[ ]"
        draw.text((margin + 160, y + 20), comp_box, font=text_font, fill="black")
        
        draw.text((margin + 230, y + 20), "Non-Compliant:", font=label_font, fill="black")
        non_comp_box = "[X]" if not is_compliant else "[ ]"
        draw.text((margin + 420, y + 20), non_comp_box, font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Remarks:", font=label_font, fill="black")
        remarks = record.get("remarks", "Measurement within acceptable limits" if is_compliant else "Deficiencies observed during inspection")
        draw.text((margin + col_w + 120, y + 20), remarks, font=text_font, fill="black")

    # Ensure parent output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    image.save(output_path)

    # Save sidecar metadata JSON
    sidecar_path = os.path.splitext(output_path)[0] + ".json"
    sidecar_data = {
        "variant": variant,
        "seed": seed,
        "provenance": record.get("provenance", {})
    }
    with open(sidecar_path, "w", encoding="utf-8") as f:
        json.dump(sidecar_data, f, indent=4)

    return image
