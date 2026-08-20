import os
import textwrap
from PIL import Image, ImageDraw
from ai_engine.synthetic_documents.qcr_image_generator import get_system_font

def generate_pmgsy_qcr_image(record: dict, output_path: str) -> Image.Image:
    """
    Generates a structured PMGSY Quality Control Report document image from record details.
    """
    # Load fonts
    title_font = get_system_font(44)
    section_font = get_system_font(28)
    label_font = get_system_font(22)
    text_font = get_system_font(22)

    # Document Geometry
    WIDTH = 1600
    HEIGHT = 2200

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    margin = 100
    y = 60

    # 1. TITLE HEADER
    draw.text(
        (WIDTH // 2, y),
        "PMGSY QUALITY CONTROL REPORT",
        font=title_font,
        fill="black",
        anchor="ma"
    )
    y += 80

    draw.line(
        (margin, y, WIDTH - margin, y),
        fill="black",
        width=3
    )
    y += 40

    draw.text(
        (margin, y),
        f"Report Number: {record.get('report_number', '')}",
        font=text_font,
        fill="black"
    )
    y += 50

    # 2. LOCATION DETAILS
    draw.text(
        (margin, y),
        "1. PMGSY LOCATION DETAILS",
        font=section_font,
        fill="black"
    )
    y += 55

    location_data = [
        ("State", record.get("state", "")),
        ("District", record.get("district", "")),
        ("Block", record.get("block", "")),
        ("Habitation", record.get("habitation_name", "")),
        ("Habitation ID", record.get("habitation_id", ""))
    ]

    for label, value in location_data:
        draw.text(
            (margin, y),
            f"{label}:",
            font=label_font,
            fill="black"
        )
        wrapped = textwrap.wrap(str(value), width=55)
        draw.text(
            (margin + 280, y),
            wrapped[0] if wrapped else "",
            font=text_font,
            fill="black"
        )
        y += 45
    y += 30

    # 3. FACILITY DETAILS
    draw.text(
        (margin, y),
        "2. FACILITY DETAILS",
        font=section_font,
        fill="black"
    )
    y += 55

    facility_data = [
        ("Facility", record.get("facility_name", "")),
        ("Category", record.get("facility_category", "")),
        ("Subcategory", record.get("facility_subcategory", "")),
        ("Address", record.get("address", ""))
    ]

    for label, value in facility_data:
        draw.text(
            (margin, y),
            f"{label}:",
            font=label_font,
            fill="black"
        )
        wrapped = textwrap.wrap(str(value), width=55)
        for line in wrapped[:2]:
            draw.text(
                (margin + 280, y),
                line,
                font=text_font,
                fill="black"
            )
            y += 35
        y += 10
    y += 30

    # 4. INSPECTION DETAILS
    draw.text(
        (margin, y),
        "3. INSPECTION DETAILS",
        font=section_font,
        fill="black"
    )
    y += 55

    inspection_data = [
        ("Inspection Date", record.get("inspection_date", "")),
        ("Inspection Type", record.get("inspection_type", "")),
        ("Inspector", record.get("inspector_name", ""))
    ]

    for label, value in inspection_data:
        draw.text(
            (margin, y),
            f"{label}:",
            font=label_font,
            fill="black"
        )
        draw.text(
            (margin + 300, y),
            str(value),
            font=text_font,
            fill="black"
        )
        y += 45
    y += 35

    # 5. QUALITY TABLE
    draw.text(
        (margin, y),
        "4. QUALITY MEASUREMENT",
        font=section_font,
        fill="black"
    )
    y += 55

    columns = [
        ("Parameter", 500),
        ("Required", 280),
        ("Measured", 280),
        ("Unit", 200)
    ]
    row_height = 65

    # Draw headers
    x = margin
    for header, width in columns:
        draw.rectangle(
            (x, y, x + width, y + row_height),
            outline="black",
            width=2
        )
        draw.text(
            (x + 10, y + 18),
            header,
            font=label_font,
            fill="black"
        )
        x += width

    # Draw data
    y += row_height
    x = margin
    values = [
        record.get("parameter", ""),
        str(record.get("required_value", "")),
        str(record.get("measured_value", "")),
        record.get("unit", "")
    ]

    for value, (_, width) in zip(values, columns):
        draw.rectangle(
            (x, y, x + width, y + row_height),
            outline="black",
            width=2
        )
        draw.text(
            (x + 10, y + 18),
            str(value),
            font=text_font,
            fill="black"
        )
        x += width
    y += row_height + 50

    # 6. QUALITY STATUS
    draw.text(
        (margin, y),
        "QUALITY STATUS:",
        font=label_font,
        fill="black"
    )
    draw.text(
        (margin + 300, y),
        record.get("quality_status", ""),
        font=section_font,
        fill="black"
    )
    y += 80

    # 7. REMARKS
    draw.text(
        (margin, y),
        "5. REMARKS",
        font=section_font,
        fill="black"
    )
    y += 50

    remarks = textwrap.wrap(
        record.get("remarks", ""),
        width=80
    )
    for line in remarks:
        draw.text(
            (margin, y),
            line,
            font=text_font,
            fill="black"
        )
        y += 35

    # Save
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    image.save(output_path)
    return image
