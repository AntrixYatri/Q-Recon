import os
import json
from PIL import Image, ImageDraw
from ai_engine.synthetic_documents.qcr_image_generator import get_system_font

def generate_test_datasheet_image(record: dict, output_path: str, variant: str = "A", seed: int = 42) -> Image.Image:
    """
    Generates a structured Test Datasheet document image from record details.
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

    if variant == "A":
        # VARIANT A: Key-value vertical layout
        draw.text((WIDTH // 2, y), "LABORATORY TEST DATASHEET", font=title_font, fill="black", anchor="ma")
        y += 80
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=3)
        y += 60

        kv_data = [
            ("Project Code", record.get("project_code", "")),
            ("Road Name", record.get("road_name", "")),
            ("District", record.get("district", "")),
            ("Block", record.get("block", "")),
            ("State", record.get("state", "")),
            ("Habitation Name", record.get("habitation_name", "")),
            ("Habitation ID", record.get("habitation_id", "")),
            ("Parameter", record.get("parameter", "")),
            ("Required Value", record.get("required_value", "")),
            ("Measured Value", record.get("measured_value", "")),
            ("Unit", record.get("unit", "")),
            ("Test Result", record.get("quality_status", "")),
            ("Test Date", record.get("inspection_date", "")),
            ("Inspector Name", record.get("inspector_name", ""))
        ]

        for label, val in kv_data:
            draw.text((margin, y), f"{label}:", font=label_font, fill="black")
            draw.text((margin + 300, y), str(val), font=text_font, fill="black")
            y += 65

    elif variant == "B":
        # VARIANT B: Two-column metadata section plus measurement table
        draw.text((WIDTH // 2, y), "TEST DATASHEET", font=title_font, fill="black", anchor="ma")
        y += 80
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=3)
        y += 60

        # Two-column metadata
        left_col_x = margin
        right_col_x = WIDTH // 2 + 50
        
        left_data = [
            ("Project Code", record.get("project_code", "")),
            ("Road Name", record.get("road_name", "")),
            ("District", record.get("district", "")),
            ("Block", record.get("block", ""))
        ]
        right_data = [
            ("State", record.get("state", "")),
            ("Habitation Name", record.get("habitation_name", "")),
            ("Habitation ID", record.get("habitation_id", "")),
            ("Test Date", record.get("inspection_date", ""))
        ]

        temp_y = y
        for label, val in left_data:
            draw.text((left_col_x, temp_y), f"{label}:", font=label_font, fill="black")
            draw.text((left_col_x + 220, temp_y), str(val), font=text_font, fill="black")
            temp_y += 60

        temp_y = y
        for label, val in right_data:
            draw.text((right_col_x, temp_y), f"{label}:", font=label_font, fill="black")
            draw.text((right_col_x + 220, temp_y), str(val), font=text_font, fill="black")
            temp_y += 60

        y = max(temp_y, y + 260) + 40
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=2)
        y += 50

        # Table-based measurement section
        draw.text((margin, y), "TEST RESULT MEASUREMENT TABLE", font=section_font, fill="black")
        y += 60

        columns = [
            ("Parameter", 500),
            ("Required", 280),
            ("Measured", 280),
            ("Unit", 200)
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
        values = [
            record.get("parameter", ""),
            str(record.get("required_value", "")),
            str(record.get("measured_value", "")),
            record.get("unit", "")
        ]
        for val, (_, width) in zip(values, columns):
            draw.rectangle((x, y, x + width, y + row_height), outline="black", width=2)
            draw.text((x + 10, y + 18), str(val), font=text_font, fill="black")
            x += width

        y += row_height + 80
        draw.text((margin, y), "Test Result:", font=label_font, fill="black")
        draw.text((margin + 200, y), record.get("quality_status", ""), font=section_font, fill="black")
        y += 60
        draw.text((margin, y), "Inspector Name:", font=label_font, fill="black")
        draw.text((margin + 200, y), record.get("inspector_name", ""), font=text_font, fill="black")

    else:
        # VARIANT C: Table-heavy layout
        draw.text((WIDTH // 2, y), "LABORATORY TEST REPORT", font=title_font, fill="black", anchor="ma")
        y += 80
        draw.line((margin, y, WIDTH - margin, y), fill="black", width=3)
        y += 60

        row_h = 75
        col_w = (WIDTH - 2 * margin) // 2

        # Row 1: Project Code | Road Name
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Project Code:", font=label_font, fill="black")
        draw.text((margin + 180, y + 20), str(record.get("project_code", "")), font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Road Name:", font=label_font, fill="black")
        draw.text((margin + col_w + 180, y + 20), str(record.get("road_name", "")), font=text_font, fill="black")
        y += row_h

        # Row 2: Location (State, District, Block) | Habitation (Name & ID)
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Location:", font=label_font, fill="black")
        loc_str = f"{record.get('state', '')}, {record.get('district', '')}, {record.get('block', '')}"
        draw.text((margin + 150, y + 20), loc_str, font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Habitation:", font=label_font, fill="black")
        hab_str = f"{record.get('habitation_name', '')} ({record.get('habitation_id', '')})"
        draw.text((margin + col_w + 150, y + 20), hab_str, font=text_font, fill="black")
        y += row_h

        # Row 3: Test Date | Inspector
        draw.rectangle((margin, y, margin + col_w, y + row_h), outline="black", width=2)
        draw.text((margin + 15, y + 20), "Test Date:", font=label_font, fill="black")
        draw.text((margin + 150, y + 20), str(record.get("inspection_date", "")), font=text_font, fill="black")

        draw.rectangle((margin + col_w, y, WIDTH - margin, y + row_h), outline="black", width=2)
        draw.text((margin + col_w + 15, y + 20), "Inspector:", font=label_font, fill="black")
        draw.text((margin + col_w + 150, y + 20), str(record.get("inspector_name", "")), font=text_font, fill="black")
        y += row_h + 80

        # Parameter Table Headers
        columns = [
            ("Parameter", 400),
            ("Required", 230),
            ("Measured", 230),
            ("Unit", 180),
            ("Result", 220)
        ]
        
        x = margin
        for header, width in columns:
            draw.rectangle((x, y, x + width, y + row_h), outline="black", width=2)
            draw.text((x + 10, y + 20), header, font=label_font, fill="black")
            x += width
        y += row_h

        # Parameter Table Data
        x = margin
        values = [
            record.get("parameter", ""),
            str(record.get("required_value", "")),
            str(record.get("measured_value", "")),
            record.get("unit", ""),
            record.get("quality_status", "")
        ]
        for val, (_, width) in zip(values, columns):
            draw.rectangle((x, y, x + width, y + row_h), outline="black", width=2)
            draw.text((x + 10, y + 20), str(val), font=text_font, fill="black")
            x += width

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
