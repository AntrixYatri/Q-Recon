import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm

def get_system_font(size: int):
    """
    Locates an available system TrueType font or falls back to PIL default font.
    Prioritises clean, standard Sans-Serif fonts for OCR readability.
    """
    try:
        fonts = fm.findSystemFonts()
        # Search for clean, readable standard fonts first
        for name in ["arial.ttf", "calibri.ttf", "dejavusans.ttf", "liberationsans.ttf", "segoeui.ttf", "verdana.ttf"]:
            for f in fonts:
                if name in f.lower():
                    return ImageFont.truetype(f, size)
        
        if fonts:
            return ImageFont.truetype(fonts[0], size)
        
        # Check standard Windows font path as fallback
        win_arial = "C:\\Windows\\Fonts\\arial.ttf"
        if os.path.exists(win_arial):
            return ImageFont.truetype(win_arial, size)
            
        # Linux fallback
        linux_font = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        if os.path.exists(linux_font):
            return ImageFont.truetype(linux_font, size)
    except Exception:
        pass
    
    # Absolute fallback
    return ImageFont.load_default()

def generate_qcr_image(record: dict, output_path: str) -> Image.Image:
    """
    Generates a structured Quality Control Report document image from record details.
    """
    # Load fonts
    title_font = get_system_font(48)
    section_font = get_system_font(30)
    label_font = get_system_font(24)
    text_font = get_system_font(24)

    # Canvas Size
    WIDTH = 1600
    HEIGHT = 2200

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    margin = 100
    y = 70

    # 1. HEADER
    draw.text(
        (WIDTH // 2, y),
        "QUALITY CONTROL REPORT",
        font=title_font,
        fill="black",
        anchor="ma"
    )
    y += 90

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
    y += 45

    draw.text(
        (margin, y),
        f"Project Name: {record.get('project_name', '')}",
        font=text_font,
        fill="black"
    )
    y += 45

    draw.text(
        (margin, y),
        f"Project Code: {record.get('project_code', '')}",
        font=text_font,
        fill="black"
    )
    y += 80

    # 2. LOCATION
    draw.text(
        (margin, y),
        "1. LOCATION DETAILS",
        font=section_font,
        fill="black"
    )
    y += 55

    location_data = [
        ("State", record.get("state", "")),
        ("District", record.get("district", "")),
        ("Block", record.get("block", "")),
        ("Village", record.get("village", ""))
    ]

    for label, value in location_data:
        draw.text(
            (margin, y),
            f"{label}:",
            font=label_font,
            fill="black"
        )
        draw.text(
            (margin + 250, y),
            str(value),
            font=text_font,
            fill="black"
        )
        y += 45
    y += 35

    # 3. ROAD INFORMATION
    draw.text(
        (margin, y),
        "2. ROAD INFORMATION",
        font=section_font,
        fill="black"
    )
    y += 55

    road_data = [
        ("Road Name", record.get("road_name", "")),
        ("Road Code", record.get("road_code", "")),
        ("Road Length", f"{record.get('road_length', '')} km"),
        ("Road Category", record.get("road_category", ""))
    ]

    for label, value in road_data:
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
        ("Inspector", record.get("inspector_name", "")),
        ("Location", record.get("inspection_location", ""))
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
    y += 40

    # 5. QUALITY TABLE
    draw.text(
        (margin, y),
        "4. QUALITY MEASUREMENTS",
        font=section_font,
        fill="black"
    )
    y += 60

    table_x = margin
    row_height = 70

    columns = [
        ("Parameter", 450),
        ("Required Value", 300),
        ("Measured Value", 300),
        ("Unit", 200)
    ]

    # Draw Table Headers
    x = table_x
    for header, width in columns:
        draw.rectangle(
            (x, y, x + width, y + row_height),
            outline="black",
            width=2
        )
        draw.text(
            (x + 15, y + 20),
            header,
            font=label_font,
            fill="black"
        )
        x += width

    # Draw Table Data Rows
    y += row_height
    x = table_x
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
            (x + 15, y + 20),
            str(value),
            font=text_font,
            fill="black"
        )
        x += width
    y += row_height + 60

    # 6. QUALITY STATUS
    draw.text(
        (margin, y),
        "Quality Status:",
        font=label_font,
        fill="black"
    )
    draw.text(
        (margin + 300, y),
        record.get("quality_status", ""),
        font=section_font,
        fill="black"
    )
    y += 90

    # 7. REMARKS & CONTRACTOR
    draw.text(
        (margin, y),
        "5. REMARKS",
        font=section_font,
        fill="black"
    )
    y += 55

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
        y += 40
    y += 40

    draw.text(
        (margin, y),
        f"Contractor: {record.get('contractor_name', '')}",
        font=text_font,
        fill="black"
    )
    y += 45

    draw.text(
        (margin, y),
        f"Agency: {record.get('agency_name', '')}",
        font=text_font,
        fill="black"
    )

    # Ensure parent output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    image.save(output_path)
    return image
