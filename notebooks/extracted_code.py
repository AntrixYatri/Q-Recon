# ============================================================
# CELL
# ============================================================
import os

folders = [
    "QCR_SIH",
    "QCR_SIH/data",
    "QCR_SIH/data/raw",
    "QCR_SIH/data/synthetic",
    "QCR_SIH/data/processed",
    "QCR_SIH/data/annotations",
    "QCR_SIH/models",
    "QCR_SIH/outputs",
    "QCR_SIH/notebooks"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Project folders created successfully!")

for folder in folders:
    print(folder)



# ============================================================
# CELL
# ============================================================
import torch

print("PyTorch version:", torch.__version__)
print("GPU available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
else:
    print("No GPU detected")



# ============================================================
# CELL
# ============================================================
dataset_fields = {
    "project_details": [
        "project_name",
        "project_code",
        "state",
        "district",
        "block",
        "village"
    ],

    "road_details": [
        "road_name",
        "road_code",
        "road_length",
        "road_category"
    ],

    "inspection_details": [
        "inspection_date",
        "inspection_type",
        "inspector_name",
        "inspection_location"
    ],

    "quality_parameters": [
        "material_type",
        "layer_type",
        "measured_value",
        "required_value",
        "unit",
        "quality_status"
    ],

    "report_details": [
        "report_number",
        "contractor_name",
        "agency_name",
        "remarks"
    ]
}

for category, fields in dataset_fields.items():
    print(f"\n{category.upper()}")
    for field in fields:
        print(" -", field)



# ============================================================
# CELL
# ============================================================
dataset_plan = {
    "clean_documents": 1000,
    "difficult_documents": 1000,
    "non_compliant_documents": 1000
}

total = sum(dataset_plan.values())

print("Dataset Plan")
print("=" * 30)

for category, count in dataset_plan.items():
    print(f"{category}: {count}")

print("=" * 30)
print("Total planned documents:", total)




# ============================================================
# CELL
# ============================================================
ground_truth_example = {
    "image_id": "qcr_000001",
    "project_name": "Rural Road Improvement Project",
    "project_code": "RR-2026-014",
    "state": "Example State",
    "district": "Example District",
    "road_name": "ABC Village Road",
    "road_length": 5.2,
    "inspection_date": "12/08/2026",
    "measured_value": 42,
    "required_value": 50,
    "unit": "mm",
    "quality_status": "NON_COMPLIANT"
}

ground_truth_example



# ============================================================
# CELL
# ============================================================
qcr_template = {
    "header": [
        "report_number",
        "project_name",
        "project_code"
    ],

    "location": [
        "state",
        "district",
        "block",
        "village"
    ],

    "road_information": [
        "road_name",
        "road_code",
        "road_length",
        "road_category"
    ],

    "inspection": [
        "inspection_date",
        "inspection_type",
        "inspector_name",
        "inspection_location"
    ],

    "quality_measurements": [
        "parameter",
        "required_value",
        "measured_value",
        "unit",
        "quality_status"
    ],

    "remarks": [
        "contractor_name",
        "agency_name",
        "remarks"
    ]
}

print("QCR TEMPLATE")
print("=" * 40)

for section, fields in qcr_template.items():
    print(f"\n{section.upper()}")
    for field in fields:
        print("  -", field)



# ============================================================
# CELL
# ============================================================
import random
import json
from datetime import datetime, timedelta

print("Libraries loaded successfully!")



# ============================================================
# CELL
# ============================================================
states = [
    "Uttar Pradesh",
    "Bihar",
    "Rajasthan",
    "Madhya Pradesh",
    "Odisha",
    "Jharkhand",
    "Chhattisgarh"
]

districts = [
    "District A",
    "District B",
    "District C",
    "District D",
    "District E"
]

blocks = [
    "Block A",
    "Block B",
    "Block C",
    "Block D"
]

road_categories = [
    "Rural Road",
    "Major Rural Road",
    "Link Road"
]

inspection_types = [
    "Routine Inspection",
    "Quality Inspection",
    "Final Inspection",
    "Material Inspection"
]

parameters = [
    {
        "name": "Pavement Thickness",
        "required_min": 50,
        "required_max": 60,
        "unit": "mm"
    },
    {
        "name": "Compaction",
        "required_min": 95,
        "required_max": 100,
        "unit": "%"
    },
    {
        "name": "Aggregate Size",
        "required_min": 20,
        "required_max": 40,
        "unit": "mm"
    }
]

print("Value pools created successfully!")



# ============================================================
# CELL
# ============================================================
def generate_qcr_record(index):
    state = random.choice(states)
    district = random.choice(districts)
    block = random.choice(blocks)

    parameter = random.choice(parameters)

    required_value = random.randint(
        parameter["required_min"],
        parameter["required_max"]
    )

    # 80% compliant, 20% non-compliant
    if random.random() < 0.8:
        measured_value = required_value + random.randint(0, 3)
        quality_status = "COMPLIANT"
    else:
        measured_value = required_value - random.randint(1, 10)
        quality_status = "NON-COMPLIANT"

    start_date = datetime(2025, 1, 1)
    inspection_date = start_date + timedelta(
        days=random.randint(0, 500)
    )

    record = {
        "image_id": f"qcr_{index:06d}",

        "report_number": f"QCR-2026-{index:05d}",

        "project_name": "Rural Road Improvement Project",
        "project_code": f"RR-{random.randint(2025, 2026)}-{random.randint(100, 999)}",

        "state": state,
        "district": district,
        "block": block,
        "village": f"Village {random.choice(['A', 'B', 'C', 'D', 'E'])}",

        "road_name": f"{random.choice(['ABC', 'XYZ', 'PQR', 'LMN'])} Village Road",
        "road_code": f"RD-{random.randint(10000, 99999)}",
        "road_length": round(random.uniform(1.0, 10.0), 1),
        "road_category": random.choice(road_categories),

        "inspection_date": inspection_date.strftime("%d/%m/%Y"),
        "inspection_type": random.choice(inspection_types),
        "inspector_name": f"Inspector {random.choice(['A', 'B', 'C', 'D'])}",
        "inspection_location": f"{block}, {district}",

        "parameter": parameter["name"],
        "required_value": required_value,
        "measured_value": measured_value,
        "unit": parameter["unit"],
        "quality_status": quality_status,

        "contractor_name": f"Contractor {random.choice(['A', 'B', 'C', 'D'])}",
        "agency_name": "Quality Control Agency",
        "remarks": (
            "Measurements within acceptable limits."
            if quality_status == "COMPLIANT"
            else "Measurement below required specification."
        )
    }

    return record



# ============================================================
# CELL
# ============================================================
records = [
    generate_qcr_record(i)
    for i in range(1, 11)
]

print("Generated records:", len(records))

for record in records[:3]:
    print(json.dumps(record, indent=2))



# ============================================================
# CELL
# ============================================================
for record in records:
    print(
        record["image_id"],
        "|",
        record["parameter"],
        "| Required:", record["required_value"],
        "| Measured:", record["measured_value"],
        "| Status:", record["quality_status"]
    )



# ============================================================
# CELL
# ============================================================
def validate_qcr_record(record):
    errors = []

    # Check required fields
    required_fields = [
        "image_id",
        "report_number",
        "project_name",
        "project_code",
        "state",
        "district",
        "block",
        "village",
        "road_name",
        "road_code",
        "road_length",
        "road_category",
        "inspection_date",
        "inspection_type",
        "inspector_name",
        "inspection_location",
        "parameter",
        "required_value",
        "measured_value",
        "unit",
        "quality_status",
        "contractor_name",
        "agency_name",
        "remarks"
    ]

    for field in required_fields:
        if field not in record:
            errors.append(f"Missing field: {field}")

    # Check road length
    if record.get("road_length", 0) <= 0:
        errors.append("Road length must be greater than 0")

    # Check measurement values
    if record.get("required_value", 0) <= 0:
        errors.append("Required value must be greater than 0")

    if record.get("measured_value", 0) <= 0:
        errors.append("Measured value must be greater than 0")

    # Check quality status
    required_value = record.get("required_value")
    measured_value = record.get("measured_value")
    status = record.get("quality_status")

    if measured_value >= required_value:
        expected_status = "COMPLIANT"
    else:
        expected_status = "NON-COMPLIANT"

    if status != expected_status:
        errors.append(
            f"Incorrect quality status: expected {expected_status}, got {status}"
        )

    # Check valid status values
    if status not in ["COMPLIANT", "NON-COMPLIANT"]:
        errors.append("Invalid quality status")

    return errors



# ============================================================
# CELL
# ============================================================
print("VALIDATING DATA")
print("=" * 50)

all_valid = True

for record in records:
    errors = validate_qcr_record(record)

    if errors:
        all_valid = False
        print(f"\n❌ {record['image_id']}")
        for error in errors:
            print("   -", error)
    else:
        print(f"✅ {record['image_id']}")

print("\n" + "=" * 50)

if all_valid:
    print("ALL RECORDS ARE VALID ✅")
else:
    print("SOME RECORDS HAVE ERRORS ❌")



# ============================================================
# CELL
# ============================================================
compliant = sum(
    1 for record in records
    if record["quality_status"] == "COMPLIANT"
)

non_compliant = sum(
    1 for record in records
    if record["quality_status"] == "NON-COMPLIANT"
)

print("COMPLIANCE DISTRIBUTION")
print("=" * 40)
print("Compliant:", compliant)
print("Non-compliant:", non_compliant)
print("Total:", compliant + non_compliant)



# ============================================================
# CELL
# ============================================================
test_record = records[0].copy()

test_record["measured_value"] = 20
test_record["required_value"] = 50
test_record["quality_status"] = "COMPLIANT"

errors = validate_qcr_record(test_record)

print("INTENTIONALLY BROKEN RECORD")
print("=" * 40)

if errors:
    print("Validator correctly detected the problem! ✅")
    for error in errors:
        print("-", error)
else:
    print("Validator failed to detect the problem ❌")



# ============================================================
# CELL
# ============================================================
test_records = [
    generate_qcr_record(i)
    for i in range(1, 101)
]

valid_count = 0
invalid_count = 0

for record in test_records:
    errors = validate_qcr_record(record)

    if errors:
        invalid_count += 1
    else:
        valid_count += 1

print("TEST DATASET")
print("=" * 40)
print("Total records:", len(test_records))
print("Valid records:", valid_count)
print("Invalid records:", invalid_count)



# ============================================================
# CELL
# ============================================================
from google.colab import drive

drive.mount('/content/drive')



# ============================================================
# CELL
# ============================================================
import os

DRIVE_ROOT = "/content/drive/MyDrive/QCR_SIH"

folders = [
    DRIVE_ROOT,
    f"{DRIVE_ROOT}/data",
    f"{DRIVE_ROOT}/data/raw",
    f"{DRIVE_ROOT}/data/synthetic",
    f"{DRIVE_ROOT}/data/processed",
    f"{DRIVE_ROOT}/data/annotations",
    f"{DRIVE_ROOT}/models",
    f"{DRIVE_ROOT}/outputs"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Google Drive project structure created!")
print(DRIVE_ROOT)



# ============================================================
# CELL
# ============================================================
import json

json_path = f"{DRIVE_ROOT}/data/synthetic/qcr_ground_truth_100.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(test_records, f, indent=2, ensure_ascii=False)

print("JSON saved successfully!")
print(json_path)



# ============================================================
# CELL
# ============================================================
import pandas as pd

csv_path = f"{DRIVE_ROOT}/data/synthetic/qcr_ground_truth_100.csv"

df = pd.DataFrame(test_records)
df.to_csv(csv_path, index=False)

print("CSV saved successfully!")
print(csv_path)



# ============================================================
# CELL
# ============================================================
print("Dataset shape:", df.shape)

display(df.head())



# ============================================================
# CELL
# ============================================================
print("JSON exists:", os.path.exists(json_path))
print("CSV exists:", os.path.exists(csv_path))

print("\nFiles:")
for file in os.listdir(f"{DRIVE_ROOT}/data/synthetic"):
    print("-", file)



# ============================================================
# CELL
# ============================================================
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

print("Image generation libraries loaded!")



# ============================================================
# CELL
# ============================================================
import matplotlib.font_manager as fm

fonts = fm.findSystemFonts()

print("Number of fonts found:", len(fonts))

for font in fonts[:20]:
    print(font)



# ============================================================
# CELL
# ============================================================
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm

# Find available fonts automatically
fonts = fm.findSystemFonts()

# Pick a font from the available system fonts
font_path = fonts[0]

print("Using font:")
print(font_path)

# Load fonts
title_font = ImageFont.truetype(font_path, 48)
section_font = ImageFont.truetype(font_path, 30)
label_font = ImageFont.truetype(font_path, 24)
text_font = ImageFont.truetype(font_path, 24)

print("Fonts loaded successfully! ✅")



# ============================================================
# CELL
# ============================================================
from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm
import textwrap
import os

# --------------------------------------------------
# 1. SELECT A WORKING FONT
# --------------------------------------------------

fonts = fm.findSystemFonts()

if len(fonts) == 0:
    raise RuntimeError("No system fonts found.")

font_path = fonts[0]

print("Using font:")
print(font_path)

# Load fonts
title_font = ImageFont.truetype(font_path, 48)
section_font = ImageFont.truetype(font_path, 30)
label_font = ImageFont.truetype(font_path, 24)
text_font = ImageFont.truetype(font_path, 24)

# --------------------------------------------------
# 2. SELECT OUR GROUND-TRUTH RECORD
# --------------------------------------------------

record = test_records[0]

print("\nGenerating document for:")
print(record["image_id"])

# --------------------------------------------------
# 3. CREATE DOCUMENT
# --------------------------------------------------

WIDTH = 1600
HEIGHT = 2200

image = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(image)

margin = 100
y = 70

# --------------------------------------------------
# 4. HEADER
# --------------------------------------------------

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
    f"Report Number: {record['report_number']}",
    font=text_font,
    fill="black"
)

y += 45

draw.text(
    (margin, y),
    f"Project Name: {record['project_name']}",
    font=text_font,
    fill="black"
)

y += 45

draw.text(
    (margin, y),
    f"Project Code: {record['project_code']}",
    font=text_font,
    fill="black"
)

y += 80

# --------------------------------------------------
# 5. LOCATION DETAILS
# --------------------------------------------------

draw.text(
    (margin, y),
    "1. LOCATION DETAILS",
    font=section_font,
    fill="black"
)

y += 55

location_data = [
    ("State", record["state"]),
    ("District", record["district"]),
    ("Block", record["block"]),
    ("Village", record["village"])
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

# --------------------------------------------------
# 6. ROAD INFORMATION
# --------------------------------------------------

draw.text(
    (margin, y),
    "2. ROAD INFORMATION",
    font=section_font,
    fill="black"
)

y += 55

road_data = [
    ("Road Name", record["road_name"]),
    ("Road Code", record["road_code"]),
    ("Road Length", f"{record['road_length']} km"),
    ("Road Category", record["road_category"])
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

# --------------------------------------------------
# 7. INSPECTION DETAILS
# --------------------------------------------------

draw.text(
    (margin, y),
    "3. INSPECTION DETAILS",
    font=section_font,
    fill="black"
)

y += 55

inspection_data = [
    ("Inspection Date", record["inspection_date"]),
    ("Inspection Type", record["inspection_type"]),
    ("Inspector", record["inspector_name"]),
    ("Location", record["inspection_location"])
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

# --------------------------------------------------
# 8. QUALITY MEASUREMENTS TABLE
# --------------------------------------------------

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

# Table header
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

# Table data
y += row_height
x = table_x

values = [
    record["parameter"],
    str(record["required_value"]),
    str(record["measured_value"]),
    record["unit"]
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

# --------------------------------------------------
# 9. QUALITY STATUS
# --------------------------------------------------

draw.text(
    (margin, y),
    "Quality Status:",
    font=label_font,
    fill="black"
)

draw.text(
    (margin + 300, y),
    record["quality_status"],
    font=section_font,
    fill="black"
)

y += 90

# --------------------------------------------------
# 10. REMARKS
# --------------------------------------------------

draw.text(
    (margin, y),
    "5. REMARKS",
    font=section_font,
    fill="black"
)

y += 55

remarks = textwrap.wrap(
    record["remarks"],
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
    f"Contractor: {record['contractor_name']}",
    font=text_font,
    fill="black"
)

y += 45

draw.text(
    (margin, y),
    f"Agency: {record['agency_name']}",
    font=text_font,
    fill="black"
)

# --------------------------------------------------
# 11. SAVE IMAGE
# --------------------------------------------------

image_path = f"{DRIVE_ROOT}/data/synthetic/qcr_000001.png"

image.save(image_path)

print("\nQCR image created successfully! ✅")
print("Saved to:")
print(image_path)



# ============================================================
# CELL
# ============================================================
from IPython.display import display

display(image)



# ============================================================
# CELL
# ============================================================
# Generate 10 different QCR records

variation_records = [
    generate_qcr_record(i)
    for i in range(1, 11)
]

print("Generated:", len(variation_records), "records")

for record in variation_records:
    print(
        record["image_id"],
        "|",
        record["parameter"],
        "| Required:",
        record["required_value"],
        "| Measured:",
        record["measured_value"],
        "|",
        record["quality_status"]
    )



# ============================================================
# CELL
# ============================================================
def generate_qcr_image(record, output_path):

    from PIL import Image, ImageDraw, ImageFont
    import matplotlib.font_manager as fm
    import textwrap

    # Find available font
    fonts = fm.findSystemFonts()

    if len(fonts) == 0:
        raise RuntimeError("No fonts found.")

    font_path = fonts[0]

    # Fonts
    title_font = ImageFont.truetype(font_path, 48)
    section_font = ImageFont.truetype(font_path, 30)
    label_font = ImageFont.truetype(font_path, 24)
    text_font = ImageFont.truetype(font_path, 24)

    # Document
    WIDTH = 1600
    HEIGHT = 2200

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    margin = 100
    y = 70

    # -----------------------------
    # HEADER
    # -----------------------------

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
        f"Report Number: {record['report_number']}",
        font=text_font,
        fill="black"
    )

    y += 45

    draw.text(
        (margin, y),
        f"Project Name: {record['project_name']}",
        font=text_font,
        fill="black"
    )

    y += 45

    draw.text(
        (margin, y),
        f"Project Code: {record['project_code']}",
        font=text_font,
        fill="black"
    )

    y += 80

    # -----------------------------
    # LOCATION
    # -----------------------------

    draw.text(
        (margin, y),
        "1. LOCATION DETAILS",
        font=section_font,
        fill="black"
    )

    y += 55

    location_data = [
        ("State", record["state"]),
        ("District", record["district"]),
        ("Block", record["block"]),
        ("Village", record["village"])
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

    # -----------------------------
    # ROAD INFORMATION
    # -----------------------------

    draw.text(
        (margin, y),
        "2. ROAD INFORMATION",
        font=section_font,
        fill="black"
    )

    y += 55

    road_data = [
        ("Road Name", record["road_name"]),
        ("Road Code", record["road_code"]),
        ("Road Length", f"{record['road_length']} km"),
        ("Road Category", record["road_category"])
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

    # -----------------------------
    # INSPECTION
    # -----------------------------

    draw.text(
        (margin, y),
        "3. INSPECTION DETAILS",
        font=section_font,
        fill="black"
    )

    y += 55

    inspection_data = [
        ("Inspection Date", record["inspection_date"]),
        ("Inspection Type", record["inspection_type"]),
        ("Inspector", record["inspector_name"]),
        ("Location", record["inspection_location"])
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

    # -----------------------------
    # QUALITY TABLE
    # -----------------------------

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

    y += row_height
    x = table_x

    values = [
        record["parameter"],
        str(record["required_value"]),
        str(record["measured_value"]),
        record["unit"]
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

    # -----------------------------
    # STATUS
    # -----------------------------

    draw.text(
        (margin, y),
        "Quality Status:",
        font=label_font,
        fill="black"
    )

    draw.text(
        (margin + 300, y),
        record["quality_status"],
        font=section_font,
        fill="black"
    )

    y += 90

    # -----------------------------
    # REMARKS
    # -----------------------------

    draw.text(
        (margin, y),
        "5. REMARKS",
        font=section_font,
        fill="black"
    )

    y += 55

    remarks = textwrap.wrap(
        record["remarks"],
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
        f"Contractor: {record['contractor_name']}",
        font=text_font,
        fill="black"
    )

    y += 45

    draw.text(
        (margin, y),
        f"Agency: {record['agency_name']}",
        font=text_font,
        fill="black"
    )

    # Save
    image.save(output_path)

    return image



# ============================================================
# CELL
# ============================================================
test_image_path = f"{DRIVE_ROOT}/data/synthetic/test_function.png"

test_image = generate_qcr_image(
    variation_records[0],
    test_image_path
)

print("Image generated successfully!")
print(test_image_path)



# ============================================================
# CELL
# ============================================================
from IPython.display import display

display(test_image)



# ============================================================
# CELL
# ============================================================
import os

batch_dir = f"{DRIVE_ROOT}/data/synthetic/images"

os.makedirs(batch_dir, exist_ok=True)

generated_images = []

for record in variation_records:

    output_path = (
        f"{batch_dir}/{record['image_id']}.png"
    )

    generate_qcr_image(
        record,
        output_path
    )

    generated_images.append(output_path)

print("Generated images:", len(generated_images))



# ============================================================
# CELL
# ============================================================
for path in generated_images:
    print(
        os.path.basename(path),
        "->",
        os.path.getsize(path),
        "bytes"
    )



# ============================================================
# CELL
# ============================================================
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import random
import os

print("Augmentation libraries loaded successfully! ✅")



# ============================================================
# CELL
# ============================================================
def augment_qcr_image(image_path, output_path, variant_type):

    image = Image.open(image_path).convert("RGB")

    # -----------------------------
    # 1. ROTATION
    # -----------------------------
    if variant_type == "rotation":

        angle = random.uniform(-4, 4)

        image = image.rotate(
            angle,
            expand=True,
            fillcolor="white"
        )

    # -----------------------------
    # 2. BRIGHTNESS
    # -----------------------------
    elif variant_type == "brightness":

        factor = random.uniform(0.65, 1.35)

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(factor)

    # -----------------------------
    # 3. CONTRAST
    # -----------------------------
    elif variant_type == "contrast":

        factor = random.uniform(0.65, 1.35)

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(factor)

    # -----------------------------
    # 4. BLUR
    # -----------------------------
    elif variant_type == "blur":

        radius = random.uniform(0.5, 1.5)

        image = image.filter(
            ImageFilter.GaussianBlur(radius)
        )

    # -----------------------------
    # 5. NOISE
    # -----------------------------
    elif variant_type == "noise":

        image_array = np.array(image).astype(np.int16)

        noise = np.random.normal(
            0,
            8,
            image_array.shape
        )

        image_array = image_array + noise

        image_array = np.clip(
            image_array,
            0,
            255
        ).astype(np.uint8)

        image = Image.fromarray(image_array)

    # -----------------------------
    # SAVE
    # -----------------------------

    image.save(
        output_path,
        quality=90
    )

    return image



# ============================================================
# CELL
# ============================================================
augmentation_dir = (
    f"{DRIVE_ROOT}/data/synthetic/augmented"
)

os.makedirs(
    augmentation_dir,
    exist_ok=True
)

print("Augmentation folder ready! ✅")
print(augmentation_dir)



# ============================================================
# CELL
# ============================================================
variant_types = [
    "rotation",
    "brightness",
    "contrast",
    "blur",
    "noise"
]

augmented_images = []

for image_path in generated_images:

    base_name = os.path.splitext(
        os.path.basename(image_path)
    )[0]

    for variant in variant_types:

        output_path = (
            f"{augmentation_dir}/"
            f"{base_name}_{variant}.jpg"
        )

        augment_qcr_image(
            image_path,
            output_path,
            variant
        )

        augmented_images.append(output_path)

print("Augmented images created:", len(augmented_images))



# ============================================================
# CELL
# ============================================================
print("Total augmented images:", len(augmented_images))

for path in augmented_images[:10]:
    print(os.path.basename(path))



# ============================================================
# CELL
# ============================================================
from IPython.display import display

original = Image.open(generated_images[0])

rotation = Image.open(
    f"{augmentation_dir}/qcr_000001_rotation.jpg"
)

blur = Image.open(
    f"{augmentation_dir}/qcr_000001_blur.jpg"
)

noise = Image.open(
    f"{augmentation_dir}/qcr_000001_noise.jpg"
)

print("ORIGINAL")
display(original)

print("ROTATION")
display(rotation)

print("BLUR")
display(blur)

print("NOISE")
display(noise)



# ============================================================
# CELL
# ============================================================
!pip install -q easyocr




# ============================================================
# CELL
# ============================================================
import easyocr

print("EasyOCR imported successfully! ✅")



# ============================================================
# CELL
# ============================================================
reader = easyocr.Reader(
    ['en'],
    gpu=True
)

print("OCR engine initialized successfully! ✅")




# ============================================================
# CELL
# ============================================================
test_ocr_image = generated_images[0]

print("Testing OCR on:")
print(test_ocr_image)



# ============================================================
# CELL
# ============================================================
result = reader.readtext(
    test_ocr_image
)

print("OCR completed!")
print("Detected text regions:", len(result))



# ============================================================
# CELL
# ============================================================
for detection in result:

    bounding_box = detection[0]
    text = detection[1]
    confidence = detection[2]

    print(
        f"Text: {text}"
    )

    print(
        f"Confidence: {confidence:.2f}"
    )

    print("-" * 50)



# ============================================================
# CELL
# ============================================================
ocr_text = "\n".join(
    detection[1]
    for detection in result
)

print(ocr_text)



# ============================================================
# CELL
# ============================================================
import re

def extract_qcr_fields(ocr_text):

    extracted = {}

    # --------------------------------
    # Basic helper
    # --------------------------------

    def find_value(pattern):
        match = re.search(
            pattern,
            ocr_text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return None

    # --------------------------------
    # Header fields
    # --------------------------------

    extracted["report_number"] = find_value(
        r"Report Number:\s*(.+)"
    )

    extracted["project_name"] = find_value(
        r"Project Name:\s*(.+)"
    )

    extracted["project_code"] = find_value(
        r"Project Code:\s*(.+)"
    )

    # --------------------------------
    # Location
    # --------------------------------

    extracted["state"] = find_value(
        r"State:\s*(.+)"
    )

    extracted["district"] = find_value(
        r"District:\s*(.+)"
    )

    extracted["block"] = find_value(
        r"Block:\s*(.+)"
    )

    extracted["village"] = find_value(
        r"Village:\s*(.+)"
    )

    # --------------------------------
    # Road
    # --------------------------------

    extracted["road_name"] = find_value(
        r"Road Name:\s*(.+)"
    )

    extracted["road_code"] = find_value(
        r"Road Code:\s*(.+)"
    )

    extracted["road_length"] = find_value(
        r"Road Length:\s*(.+)"
    )

    extracted["road_category"] = find_value(
        r"Road Category:\s*(.+)"
    )

    # --------------------------------
    # Inspection
    # --------------------------------

    extracted["inspection_date"] = find_value(
        r"Inspection Date:\s*(.+)"
    )

    extracted["inspection_type"] = find_value(
        r"Inspection Type:\s*(.+)"
    )

    extracted["inspector_name"] = find_value(
        r"Inspector:\s*(.+)"
    )

    extracted["inspection_location"] = find_value(
        r"Location:\s*(.+)"
    )

    # --------------------------------
    # Quality information
    # --------------------------------

    extracted["parameter"] = find_value(
        r"Parameter\s*\n?([A-Za-z ]+)"
    )

    extracted["required_value"] = find_value(
        r"Required Value\s*\n?([0-9.]+)"
    )

    extracted["measured_value"] = find_value(
        r"Measured Value\s*\n?([0-9.]+)"
    )

    extracted["unit"] = find_value(
        r"Unit\s*\n?([A-Za-z%]+)"
    )

    extracted["quality_status"] = find_value(
        r"Quality Status:\s*(.+)"
    )

    # --------------------------------
    # Other fields
    # --------------------------------

    extracted["contractor_name"] = find_value(
        r"Contractor:\s*(.+)"
    )

    extracted["agency_name"] = find_value(
        r"Agency:\s*(.+)"
    )

    return extracted



# ============================================================
# CELL
# ============================================================
extracted_data = extract_qcr_fields(ocr_text)

print("EXTRACTED QCR DATA")
print("=" * 50)

for field, value in extracted_data.items():
    print(f"{field}: {value}")



# ============================================================
# CELL
# ============================================================
print("RAW OCR TEXT")
print("=" * 50)
print(ocr_text)



# ============================================================
# CELL
# ============================================================
ground_truth = test_records[0]

print("GROUND TRUTH")
print("=" * 50)

for field in extracted_data.keys():
    print(
        f"{field}: "
        f"GROUND TRUTH = {ground_truth.get(field)} "
        f"| OCR = {extracted_data.get(field)}"
    )



# ============================================================
# CELL
# ============================================================
total_fields = 0
correct_fields = 0

for field in extracted_data.keys():

    ground_value = ground_truth.get(field)
    extracted_value = extracted_data.get(field)

    if ground_value is not None:
        total_fields += 1

        if extracted_value is not None:
            if str(ground_value).strip().lower() == str(extracted_value).strip().lower():
                correct_fields += 1

accuracy = (
    correct_fields / total_fields * 100
    if total_fields > 0
    else 0
)

print("FIELD EXTRACTION ACCURACY")
print("=" * 40)
print(f"Correct fields: {correct_fields}")
print(f"Total fields: {total_fields}")
print(f"Accuracy: {accuracy:.2f}%")



# ============================================================
# CELL
# ============================================================
import pandas as pd
import os

karnataka_url = (
    "https://raw.githubusercontent.com/"
    "pratapvardhan/rural-facilities-pmgsy/"
    "master/pmgsy_facilities_karnataka.csv"
)

pmgsy_ka = pd.read_csv(karnataka_url)

print("Dataset downloaded successfully! ✅")
print("Rows:", len(pmgsy_ka))
print("Columns:", len(pmgsy_ka.columns))



# ============================================================
# CELL
# ============================================================
print("COLUMNS")
print("=" * 50)

for column in pmgsy_ka.columns:
    print("-", column)



# ============================================================
# CELL
# ============================================================
display(pmgsy_ka.head(10))



# ============================================================
# CELL
# ============================================================
pmgsy_ka.info()



# ============================================================
# CELL
# ============================================================
print("Missing values")
print("=" * 50)

print(
    pmgsy_ka.isnull().sum()
)



# ============================================================
# CELL
# ============================================================
useful_columns = [
    "State",
    "District",
    "Block",
    "Habitation Name",
    "Habitation ID",
    "Facility Name",
    "Address",
    "Facility Category",
    "Facility Subcategory",
    "Lattitude",
    "Longitude"
]

pmgsy_clean = pmgsy_ka[useful_columns].copy()

print("Clean dataset shape:", pmgsy_clean.shape)



# ============================================================
# CELL
# ============================================================
pmgsy_sample = pmgsy_clean.sample(
    n=100,
    random_state=42
).reset_index(drop=True)

print("Selected records:", len(pmgsy_sample))

display(pmgsy_sample.head())



# ============================================================
# CELL
# ============================================================
pmgsy_path = (
    f"{DRIVE_ROOT}/data/raw/"
    "pmgsy_karnataka_100.csv"
)

pmgsy_sample.to_csv(
    pmgsy_path,
    index=False
)

print("Saved:")
print(pmgsy_path)



# ============================================================
# CELL
# ============================================================
import random
from datetime import datetime, timedelta

def generate_pmgsy_qcr_record(index, pmgsy_row):

    # Real PMGSY information
    state = pmgsy_row["State"]
    district = pmgsy_row["District"]
    block = pmgsy_row["Block"]
    habitation = pmgsy_row["Habitation Name"]
    habitation_id = pmgsy_row["Habitation ID"]
    facility = pmgsy_row["Facility Name"]
    address = pmgsy_row["Address"]
    category = pmgsy_row["Facility Category"]
    subcategory = pmgsy_row["Facility Subcategory"]

    # Synthetic quality measurement
    parameter = random.choice(parameters)

    required_value = random.randint(
        parameter["required_min"],
        parameter["required_max"]
    )

    if random.random() < 0.8:
        measured_value = required_value + random.randint(0, 3)
        quality_status = "COMPLIANT"
    else:
        measured_value = required_value - random.randint(1, 10)
        quality_status = "NON-COMPLIANT"

    inspection_date = (
        datetime(2026, 1, 1)
        + timedelta(days=random.randint(0, 220))
    )

    return {
        "image_id": f"pmgsy_qcr_{index:05d}",
        "report_number": f"QCR-PMGSY-2026-{index:05d}",

        # Real PMGSY information
        "state": state,
        "district": district,
        "block": block,
        "habitation_name": habitation,
        "habitation_id": habitation_id,
        "facility_name": facility,
        "address": address,
        "facility_category": category,
        "facility_subcategory": subcategory,

        # Inspection information
        "inspection_date": inspection_date.strftime("%d/%m/%Y"),
        "inspection_type": random.choice(inspection_types),
        "inspector_name": f"Inspector {random.choice(['A', 'B', 'C', 'D'])}",

        # Quality information
        "parameter": parameter["name"],
        "required_value": required_value,
        "measured_value": measured_value,
        "unit": parameter["unit"],
        "quality_status": quality_status,

        "remarks": (
            "Measurement within acceptable limits."
            if quality_status == "COMPLIANT"
            else "Measurement below required specification."
        )
    }

print("PMGSY QCR generator created successfully! ✅")



# ============================================================
# CELL
# ============================================================
pmgsy_qcr_records = []

for i, (_, row) in enumerate(
    pmgsy_sample.iterrows(),
    start=1
):
    record = generate_pmgsy_qcr_record(
        i,
        row
    )

    pmgsy_qcr_records.append(record)

print(
    "PMGSY-grounded QCR records:",
    len(pmgsy_qcr_records)
)



# ============================================================
# CELL
# ============================================================
import json

print(
    json.dumps(
        pmgsy_qcr_records[0],
        indent=2,
        default=str
    )
)



# ============================================================
# CELL
# ============================================================
pmgsy_qcr_json = (
    f"{DRIVE_ROOT}/data/processed/"
    "pmgsy_qcr_ground_truth_100.json"
)

with open(
    pmgsy_qcr_json,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        pmgsy_qcr_records,
        f,
        indent=2,
        ensure_ascii=False,
        default=str
    )

pmgsy_qcr_csv = (
    f"{DRIVE_ROOT}/data/processed/"
    "pmgsy_qcr_ground_truth_100.csv"
)

pd.DataFrame(
    pmgsy_qcr_records
).to_csv(
    pmgsy_qcr_csv,
    index=False
)

print("PMGSY QCR ground truth saved! ✅")



# ============================================================
# CELL
# ============================================================
def generate_pmgsy_qcr_image(record, output_path):

    from PIL import Image, ImageDraw, ImageFont
    import matplotlib.font_manager as fm
    import textwrap

    fonts = fm.findSystemFonts()

    if not fonts:
        raise RuntimeError("No fonts found.")

    font_path = fonts[0]

    title_font = ImageFont.truetype(font_path, 44)
    section_font = ImageFont.truetype(font_path, 28)
    label_font = ImageFont.truetype(font_path, 22)
    text_font = ImageFont.truetype(font_path, 22)

    WIDTH = 1600
    HEIGHT = 2200

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        "white"
    )

    draw = ImageDraw.Draw(image)

    margin = 100
    y = 60

    # -----------------------------
    # TITLE
    # -----------------------------

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
        f"Report Number: {record['report_number']}",
        font=text_font,
        fill="black"
    )

    y += 50

    # -----------------------------
    # LOCATION
    # -----------------------------

    draw.text(
        (margin, y),
        "1. PMGSY LOCATION DETAILS",
        font=section_font,
        fill="black"
    )

    y += 55

    location_data = [
        ("State", record["state"]),
        ("District", record["district"]),
        ("Block", record["block"]),
        ("Habitation", record["habitation_name"]),
        ("Habitation ID", record["habitation_id"])
    ]

    for label, value in location_data:

        value = str(value)

        draw.text(
            (margin, y),
            f"{label}:",
            font=label_font,
            fill="black"
        )

        # Wrap long values
        wrapped = textwrap.wrap(
            value,
            width=55
        )

        draw.text(
            (margin + 280, y),
            wrapped[0] if wrapped else "",
            font=text_font,
            fill="black"
        )

        y += 45

    y += 30

    # -----------------------------
    # FACILITY
    # -----------------------------

    draw.text(
        (margin, y),
        "2. FACILITY DETAILS",
        font=section_font,
        fill="black"
    )

    y += 55

    facility_data = [
        ("Facility", record["facility_name"]),
        ("Category", record["facility_category"]),
        ("Subcategory", record["facility_subcategory"]),
        ("Address", record["address"])
    ]

    for label, value in facility_data:

        value = str(value)

        draw.text(
            (margin, y),
            f"{label}:",
            font=label_font,
            fill="black"
        )

        wrapped = textwrap.wrap(
            value,
            width=55
        )

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

    # -----------------------------
    # INSPECTION
    # -----------------------------

    draw.text(
        (margin, y),
        "3. INSPECTION DETAILS",
        font=section_font,
        fill="black"
    )

    y += 55

    inspection_data = [
        ("Inspection Date", record["inspection_date"]),
        ("Inspection Type", record["inspection_type"]),
        ("Inspector", record["inspector_name"])
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

    # -----------------------------
    # QUALITY TABLE
    # -----------------------------

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

    y += row_height
    x = margin

    values = [
        record["parameter"],
        record["required_value"],
        record["measured_value"],
        record["unit"]
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

    # -----------------------------
    # STATUS
    # -----------------------------

    draw.text(
        (margin, y),
        "QUALITY STATUS:",
        font=label_font,
        fill="black"
    )

    draw.text(
        (margin + 300, y),
        record["quality_status"],
        font=section_font,
        fill="black"
    )

    y += 80

    # -----------------------------
    # REMARKS
    # -----------------------------

    draw.text(
        (margin, y),
        "5. REMARKS",
        font=section_font,
        fill="black"
    )

    y += 50

    remarks = textwrap.wrap(
        record["remarks"],
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
    image.save(
        output_path
    )

    return image

print("PMGSY QCR image generator ready! ✅")



# ============================================================
# CELL
# ============================================================
pmgsy_image_dir = (
    f"{DRIVE_ROOT}/data/processed/"
    "pmgsy_qcr_images"
)

os.makedirs(
    pmgsy_image_dir,
    exist_ok=True
)

pmgsy_image_paths = []

for record in pmgsy_qcr_records[:20]:

    output_path = (
        f"{pmgsy_image_dir}/"
        f"{record['image_id']}.png"
    )

    generate_pmgsy_qcr_image(
        record,
        output_path
    )

    pmgsy_image_paths.append(
        output_path
    )

print(
    "Generated PMGSY-grounded images:",
    len(pmgsy_image_paths)
)




# ============================================================
# CELL
# ============================================================
from PIL import Image
from IPython.display import display

sample_image = Image.open(
    pmgsy_image_paths[0]
)

display(sample_image)



# ============================================================
# CELL
# ============================================================
pmgsy_ocr_results = {}

for image_path in pmgsy_image_paths:

    result = reader.readtext(image_path)

    pmgsy_ocr_results[image_path] = result

print("OCR completed for:", len(pmgsy_ocr_results), "documents")



# ============================================================
# CELL
# ============================================================
# Keep the COMPLETE OCR detections:
# text + bounding box + confidence

pmgsy_ocr_detections = pmgsy_ocr_results

print("Stored OCR detections for:",
      len(pmgsy_ocr_detections),
      "documents")

# Inspect one detection
first_image = pmgsy_image_paths[0]

print("\nExample OCR detections:")
for detection in pmgsy_ocr_detections[first_image][:10]:
    box, text, confidence = detection

    print({
        "text": text,
        "confidence": round(confidence, 3),
        "box": box
    })



# ============================================================
# CELL
# ============================================================
import numpy as np
import re
import math

def normalize_ocr_text(text):
    """
    Basic OCR cleanup.
    Does NOT alter the actual semantic value.
    """
    text = str(text).strip()

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Common OCR punctuation cleanup
    text = text.replace(" :", ":")
    text = re.sub(r":\s*", ": ", text)

    return text.strip()


def get_box_geometry(box):
    """
    Convert EasyOCR polygon into useful coordinates.
    """
    xs = [point[0] for point in box]
    ys = [point[1] for point in box]

    return {
        "x1": min(xs),
        "y1": min(ys),
        "x2": max(xs),
        "y2": max(ys),
        "xc": sum(xs) / len(xs),
        "yc": sum(ys) / len(ys),
        "width": max(xs) - min(xs),
        "height": max(ys) - min(ys)
    }


def prepare_detections(ocr_result):
    """
    Convert EasyOCR results into structured objects.
    """

    detections = []

    for detection in ocr_result:

        box, text, confidence = detection

        geom = get_box_geometry(box)

        detections.append({
            "text": normalize_ocr_text(text),
            "confidence": float(confidence),
            "box": box,
            **geom
        })

    return detections



# ============================================================
# CELL
# ============================================================
def group_into_lines(detections):
    """
    Reconstruct visual text lines from EasyOCR bounding boxes.

    OCR may detect:

        State:
        Karnataka

    as two separate objects.

    This function reconnects them based on their Y position.
    """

    if not detections:
        return []

    # Sort top-to-bottom
    detections = sorted(
        detections,
        key=lambda d: d["yc"]
    )

    lines = []

    for det in detections:

        placed = False

        for line in lines:

            # Average Y of current line
            avg_y = np.mean(
                [item["yc"] for item in line]
            )

            # Average height
            avg_h = np.mean(
                [item["height"] for item in line]
            )

            # Same horizontal text line?
            if abs(det["yc"] - avg_y) <= max(
                avg_h * 0.65,
                12
            ):

                line.append(det)
                placed = True
                break

        if not placed:
            lines.append([det])

    # Sort each line left-to-right
    for line in lines:
        line.sort(key=lambda d: d["x1"])

    # Convert to readable structure
    reconstructed_lines = []

    for line in lines:

        text = " ".join(
            item["text"]
            for item in line
        )

        reconstructed_lines.append({
            "text": normalize_ocr_text(text),
            "detections": line,
            "y": np.mean(
                [item["yc"] for item in line]
            )
        })

    # Sort final lines top-to-bottom
    reconstructed_lines.sort(
        key=lambda x: x["y"]
    )

    return reconstructed_lines



# ============================================================
# CELL
# ============================================================
first_image = pmgsy_image_paths[0]

detections = prepare_detections(
    pmgsy_ocr_detections[first_image]
)

lines = group_into_lines(detections)

print("=" * 80)
print("RECONSTRUCTED OCR")
print("=" * 80)

for i, line in enumerate(lines):
    print(
        f"{i:02d}: {line['text']}"
    )



# ============================================================
# CELL
# ============================================================
FIELD_LABELS = {
    "report_number": [
        "Report Number"
    ],

    "state": [
        "State"
    ],

    "district": [
        "District"
    ],

    "block": [
        "Block"
    ],

    "habitation_name": [
        "Habitation"
    ],

    "habitation_id": [
        "Habitation ID"
    ],

    "facility_name": [
        "Facility"
    ],

    "facility_category": [
        "Category"
    ],

    "facility_subcategory": [
        "Subcategory"
    ],

    "inspection_date": [
        "Inspection Date"
    ],

    "inspection_type": [
        "Inspection Type"
    ],

    "inspector_name": [
        "Inspector"
    ],

    "quality_status": [
        "QUALITY STATUS"
    ]
}



# ============================================================
# CELL
# ============================================================
def clean_label(label):
    label = normalize_ocr_text(label)

    label = label.lower()
    label = label.replace(":", "")

    return label.strip()


def extract_from_reconstructed_lines(lines):

    extracted = {}

    normalized_lines = [
        {
            "text": clean_label(line["text"]),
            "original": line["text"]
        }
        for line in lines
    ]

    for field, labels in FIELD_LABELS.items():

        for i, line in enumerate(normalized_lines):

            line_text = line["text"]

            for label in labels:

                label_clean = clean_label(label)

                # Case 1:
                # "State: Karnataka"
                if line_text.startswith(
                    label_clean
                ):

                    value = line_text[
                        len(label_clean):
                    ].strip()

                    value = value.lstrip(":")

                    if value:
                        extracted[field] = value.strip()
                        break

                    # Case 2:
                    # label exists but value is on next line
                    if i + 1 < len(
                        normalized_lines
                    ):

                        next_value = (
                            normalized_lines[i + 1]
                            ["original"]
                        )

                        extracted[field] = (
                            next_value.strip()
                        )

                        break

            if field in extracted:
                break

    return extracted



# ============================================================
# CELL
# ============================================================
import cv2
import numpy as np
import matplotlib.pyplot as plt


def targeted_inspector_ocr(image_path, reader):
    """
    Second-pass OCR specifically for the Inspector value.
    Uses the known approximate location of the Inspector field.
    """

    image = cv2.imread(image_path)

    if image is None:
        return None

    # ------------------------------------------------
    # Inspector value region
    # Based on EasyOCR's detected Inspector label/value
    # ------------------------------------------------

    h, w = image.shape[:2]

    # Original value is around:
    # x = 398–522
    # y = 950–976

    # Add generous padding so we don't clip the character
    x1 = 350
    x2 = min(w, 700)

    y1 = 925
    y2 = min(h, 1005)

    crop = image[y1:y2, x1:x2]

    # ------------------------------------------------
    # Upscale
    # ------------------------------------------------

    scale = 4

    enlarged = cv2.resize(
        crop,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # ------------------------------------------------
    # Grayscale
    # ------------------------------------------------

    gray = cv2.cvtColor(
        enlarged,
        cv2.COLOR_BGR2GRAY
    )

    # ------------------------------------------------
    # Contrast enhancement
    # ------------------------------------------------

    gray = cv2.equalizeHist(gray)

    # ------------------------------------------------
    # Run OCR
    # ------------------------------------------------

    results = reader.readtext(
        gray,
        detail=1,
        paragraph=False
    )

    return results, crop, enlarged



# ============================================================
# CELL
# ============================================================
def get_targeted_inspector_value(image_path, reader):

    try:
        results, _, _ = targeted_inspector_ocr(
            image_path,
            reader
        )

        # Collect OCR text from the crop
        texts = [
            str(text).strip()
            for _, text, confidence in results
            if confidence >= 0.5
        ]

        if not texts:
            return None

        # Join pieces detected in the crop
        value = " ".join(texts)

        return value.strip()

    except Exception as e:

        print(
            f"Inspector fallback failed: {e}"
        )

        return None



# ============================================================
# CELL
# ============================================================
def normalize_field_value(field, value):

    if value is None:
        return ""

    value = str(value).strip().lower()

    # General whitespace normalization
    value = re.sub(r"\s+", " ", value)

    # -----------------------------------------
    # Report number normalization
    # -----------------------------------------
    if field == "report_number":

        # Remove spaces around hyphens
        value = re.sub(r"\s*-\s*", "-", value)

        # Remove all remaining spaces
        value = value.replace(" ", "")

    # -----------------------------------------
    # Text fields
    # -----------------------------------------
    elif field in [
        "state",
        "district",
        "block",
        "habitation_name",
        "facility_name",
        "facility_category",
        "facility_subcategory",
        "inspection_type",
        "inspector_name",
        "quality_status"
    ]:

        value = re.sub(r"\s+", " ", value)

    return value.strip()



# ============================================================
# CELL
# ============================================================
first_image = pmgsy_image_paths[0]

detections = prepare_detections(
    pmgsy_ocr_detections[first_image]
)

lines = group_into_lines(
    detections
)

extracted = extract_from_reconstructed_lines(
    lines
)

print("=" * 60)
print("STRUCTURED EXTRACTION")
print("=" * 60)

for field, value in extracted.items():

    print(
        f"{field:25s}: {value}"
    )



# ============================================================
# CELL
# ============================================================
print("\nGROUND TRUTH")
print("=" * 60)

for field in extracted:

    print(
        f"{field:25s}: "
        f"{pmgsy_qcr_records[0].get(field)}"
    )



# ============================================================
# CELL
# ============================================================
fields_to_evaluate = [
    "report_number",
    "state",
    "district",
    "block",
    "habitation_name",
    "habitation_id",
    "facility_name",
    "facility_category",
    "facility_subcategory",
    "inspection_date",
    "inspection_type",
    "inspector_name",
    "quality_status"
]



# ============================================================
# CELL
# ============================================================
all_extraction_results = []
all_field_details = []

for index, image_path in enumerate(
    pmgsy_image_paths
):

    # -----------------------------
    # OCR detections
    # -----------------------------

    ocr_result = pmgsy_ocr_detections[
        image_path
    ]

    detections = prepare_detections(
        ocr_result
    )

    # -----------------------------
    # Reconstruct lines
    # -----------------------------

    lines = group_into_lines(
        detections
    )

    # -----------------------------
    # Extract fields
    # -----------------------------

    extracted = extract_from_reconstructed_lines(
        lines
    )

    # -----------------------------
    # Targeted Inspector OCR fallback
    # -----------------------------

    inspector_fallback = get_targeted_inspector_value(
        image_path,
        reader
    )

    if inspector_fallback:
        extracted["inspector_name"] = inspector_fallback
    # -----------------------------
    # Ground truth
    # -----------------------------

    ground_truth = pmgsy_qcr_records[
        index
    ]

    # -----------------------------
    # Evaluate
    # -----------------------------

    correct = 0
    total = 0

    for field in fields_to_evaluate:

        actual = normalize_field_value(
        field,
        ground_truth.get(field)
        )

        predicted = normalize_field_value(
        field,
        extracted.get(field)
        )

        if actual == "":
            continue

        total += 1

        if actual == predicted:
            correct += 1
            status = "CORRECT"
        else:
            status = "WRONG"

        all_field_details.append({
            "image": os.path.basename(
                image_path
            ),
            "field": field,
            "ground_truth":
                ground_truth.get(field),
            "extracted":
                extracted.get(field),
            "status": status
        })

    accuracy = (
        correct / total * 100
        if total else 0
    )

    all_extraction_results.append({
        "image":
            os.path.basename(image_path),
        "correct": correct,
        "total": total,
        "accuracy": accuracy
    })


accuracy_df = pd.DataFrame(
    all_extraction_results
)

field_details_df = pd.DataFrame(
    all_field_details
)

print(
    "Average field extraction accuracy:",
    round(
        accuracy_df["accuracy"].mean(),
        2
    ),
    "%"
)

display(accuracy_df)


field_accuracy = (
    field_details_df
    .groupby("field")["status"]
    .apply(
        lambda x:
        (x == "CORRECT").mean() * 100
    )
    .sort_values(
        ascending=False
    )
)

display(
    field_accuracy.to_frame(
        "accuracy_percent"
    )
)



# ============================================================
# CELL
# ============================================================
test_image = pmgsy_image_paths[0]

fallback = get_targeted_inspector_value(
    test_image,
    reader
)

print("Targeted Inspector:", fallback)
print(
    "Ground Truth:",
    pmgsy_qcr_records[0]["inspector_name"]
)



# ============================================================
# CELL
# ============================================================
# Pick the first document
test_image = pmgsy_image_paths[0]

# Prepare OCR detections
detections = prepare_detections(
    pmgsy_ocr_detections[test_image]
)

# Reconstruct lines
lines = group_into_lines(detections)

print("=" * 80)
print("RECONSTRUCTED OCR FOR:", test_image)
print("=" * 80)

for i, line in enumerate(lines):
    print(f"{i:02d}: {line['text']}")

print("\n" + "=" * 80)
print("CURRENT EXTRACTION")
print("=" * 80)

extracted = extract_from_reconstructed_lines(lines)

for field, value in extracted.items():
    print(f"{field:25s}: {value}")

print("\n" + "=" * 80)
print("GROUND TRUTH")
print("=" * 80)

ground_truth = pmgsy_qcr_records[0]

for field in fields_to_evaluate:
    print(
        f"{field:25s}: "
        f"{ground_truth.get(field)}"
    )

  # Targeted Inspector OCR fallback
inspector_fallback = get_targeted_inspector_value(
    image_path,
    reader
)

if inspector_fallback:
    extracted["inspector_name"] = inspector_fallback



# ============================================================
# CELL
# ============================================================
accuracy_df = pd.DataFrame(
    all_extraction_results
)

display(accuracy_df)

print(
    "Average field extraction accuracy:",
    round(
        accuracy_df["accuracy"].mean(),
        2
    ),
    "%"
)



# ============================================================
# CELL
# ============================================================
import matplotlib.pyplot as plt
import os

# Data provided by the user
before_accuracy = 81.54
current_accuracy = 89.23

# Calculate improvement
accuracy_improvement = current_accuracy - before_accuracy

# Setup the figure and axes
fig, ax = plt.subplots(figsize=(10, 7), facecolor='white')
ax.set_facecolor('white')

# Data for plotting
labels = ['Baseline', 'Current Prototype']
accuracies = [before_accuracy, current_accuracy]
colors = ['#FF9800', '#4CAF50'] # Orange for baseline, green for improved

# Create the bars
bars = ax.bar(labels, accuracies, color=colors, width=0.4)

# Add exact percentage above each bar
for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width()/2,
        yval + 1, # Position slightly above the bar
        f'{yval:.2f}%',
        ha='center', va='bottom', fontsize=20, fontweight='bold', color='black'
    )

# Add improvement annotation between the bars
# Positioning relative to the bars' x-coordinates
x_center = (bars[0].get_x() + bars[0].get_width()/2 + bars[1].get_x() + bars[1].get_width()/2) / 2
y_position = (max(accuracies) + min(accuracies)) / 2 # Mid-point of accuracies
ax.annotate(
    f'+{accuracy_improvement:.2f} percentage-point improvement',
    xy=(bars[0].get_x() + bars[0].get_width() * 0.9, y_position), # Start annotation slightly to the right of the first bar
    xytext=(bars[1].get_x() + bars[1].get_width() * 0.1, y_position), # End annotation slightly to the left of the second bar
    arrowprops=dict(facecolor='gray', shrink=0.05, width=2, headwidth=8, headlength=8),
    fontsize=16, ha='center', va='center', color='black', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.7)
)

# Titles
ax.set_title(
    'QCR Field Extraction Accuracy',
    fontsize=24, fontweight='bold', color='#0D47A1', pad=20
)
fig.suptitle(
    'Baseline vs Current Prototype',
    fontsize=18, color='#424242', y=0.92
)

# Y-axis settings
ax.set_ylabel('Accuracy (%)', fontsize=18, color='black', labelpad=15)
ax.set_ylim(0, 100) # Ensure Y-axis goes from 0-100

# Remove all spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Minimal gridlines on Y-axis
ax.grid(axis='y', linestyle='--', alpha=0.7)

# X-axis tick parameters (remove ticks but keep labels)
ax.tick_params(axis='x', length=0, labelsize=16, colors='black')
ax.tick_params(axis='y', labelsize=14, colors='black', width=1)

plt.tight_layout(rect=[0, 0.05, 1, 0.9]) # Adjust layout to prevent overlap with suptitle

# Save the figure to Google Drive
output_path = f'{DRIVE_ROOT}/outputs/sih_ocr_comparison_graph.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()

print(f"Comparison graph saved to: {output_path}")



# ============================================================
# CELL
# ============================================================
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Data for Graph 1: OCR Field Extraction Accuracy
oCR_accuracy_mean = accuracy_df['accuracy'].mean()

fig1, ax1 = plt.subplots(figsize=(10, 7), facecolor='white')

# Plotting the average accuracy
ax1.bar(
    ['Average Field Extraction Accuracy'],
    [oCR_accuracy_mean],
    color='#4CAF50',
    width=0.4
)

# Adding the value on top of the bar
ax1.text(
    0,
    oCR_accuracy_mean + 1, # Slightly above the bar
    f'{oCR_accuracy_mean:.2f}%',
    ha='center',
    va='bottom',
    fontsize=18,
    color='black'
)

ax1.set_title(
    'Document AI / OCR Field Extraction Accuracy',
    fontsize=22,
    fontweight='bold',
    color='black',
    pad=20
)
ax1.set_ylabel('Accuracy (%)', fontsize=18, color='black', labelpad=15)
ax1.tick_params(axis='x', labelsize=16, colors='black')
ax1.tick_params(axis='y', labelsize=16, colors='black')
ax1.set_ylim(0, 100)

# Remove spines
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')

ax1.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f'{DRIVE_ROOT}/outputs/ocr_accuracy_graph.png', dpi=300)
plt.show()

print(f"OCR Accuracy: {oCR_accuracy_mean:.2f}%")



# ============================================================
# CELL
# ============================================================
# Data for Graph 2: Quality Status Distribution
# Convert list of dicts to DataFrame for easier processing
pmgsy_qcr_df = pd.DataFrame(pmgsy_qcr_records)
quality_status_counts = pmgsy_qcr_df['quality_status'].value_counts()

fig2, ax2 = plt.subplots(figsize=(10, 7), facecolor='white')

colors = {'COMPLIANT': '#4CAF50', 'NON-COMPLIANT': '#FF5733'}

quality_status_counts.plot(
    kind='bar',
    ax=ax2,
    color=[colors.get(x, '#607D8B') for x in quality_status_counts.index]
)

ax2.set_title(
    'Quality Status Distribution in Synthetic QCR Dataset',
    fontsize=22,
    fontweight='bold',
    color='black',
    pad=20
)
ax2.set_xlabel('Quality Status', fontsize=18, color='black', labelpad=15)
ax2.set_ylabel('Number of Records', fontsize=18, color='black', labelpad=15)
ax2.tick_params(axis='x', rotation=0, labelsize=16, colors='black')
ax2.tick_params(axis='y', labelsize=16, colors='black')

# Add values on bars
for container in ax2.containers:
    for patch in container.patches:
        width = patch.get_width()
        height = patch.get_height()
        x, y = patch.get_xy()
        ax2.annotate(
            f'{int(height)}',
            (x + width/2, y + height),
            ha='center',
            va='bottom',
            fontsize=16,
            color='black'
        )

# Remove spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('black')
ax2.spines['bottom'].set_color('black')

ax2.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f'{DRIVE_ROOT}/outputs/quality_status_distribution.png', dpi=300)
plt.show()

print("Quality Status Counts:")
print(quality_status_counts)



# ============================================================
# CELL
# ============================================================
# Data for Graph 3: Facility Categories in PMGSY Karnataka
# Using pmgsy_clean (the cleaned real PMGSY data from Pratap Vardhan's repo)
facility_category_counts = pmgsy_clean['Facility Category'].value_counts().head(10) # Top 10 categories for readability

fig3, ax3 = plt.subplots(figsize=(12, 8), facecolor='white')

facility_category_counts.plot(kind='barh', ax=ax3, color='#3F51B5')

ax3.set_title(
    'Top 10 Facility Categories in PMGSY Karnataka (External Context)',
    fontsize=22,
    fontweight='bold',
    color='black',
    pad=20
)
ax3.set_xlabel('Number of Facilities', fontsize=18, color='black', labelpad=15)
ax3.set_ylabel('Facility Category', fontsize=18, color='black', labelpad=15)
ax3.tick_params(axis='x', labelsize=16, colors='black')
ax3.tick_params(axis='y', labelsize=16, colors='black')

# Add values on bars
for container in ax3.containers:
    for patch in container.patches:
        width = patch.get_width()
        y_pos = patch.get_y() + patch.get_height() / 2
        ax3.annotate(
            f'{int(width)}',
            (width, y_pos),
            ha='left',
            va='center',
            fontsize=16,
            color='black',
            xytext=(5, 0),
            textcoords='offset points'
        )

# Remove spines
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['bottom'].set_color('black')
ax3.spines['left'].set_color('black')

ax3.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(f'{DRIVE_ROOT}/outputs/pmgsy_facility_categories.png', dpi=300)
plt.show()

print("Top 10 PMGSY Facility Category Counts:")
print(facility_category_counts)



# ============================================================
# CELL
# ============================================================
print("### Data Used for Graphs")
data_summary = [
    {
        'graph_name': 'Document AI / OCR Field Extraction Accuracy',
        'metric': 'Average Field Extraction Accuracy',
        'value': f'{oCR_accuracy_mean:.2f}%',
        'source': 'Project OCR evaluation on synthetic PMGSY QCR images (accuracy_df)',
        'category': 'MEASURED PROJECT RESULTS'
    },
    {
        'graph_name': 'Quality Status Distribution in Synthetic QCR Dataset',
        'metric': 'Compliant Records',
        'value': int(quality_status_counts.get('COMPLIANT', 0)),
        'source': 'Synthetic PMGSY QCR dataset (pmgsy_qcr_records)',
        'category': 'MEASURED PROJECT RESULTS'
    },
    {
        'graph_name': 'Quality Status Distribution in Synthetic QCR Dataset',
        'metric': 'Non-Compliant Records',
        'value': int(quality_status_counts.get('NON-COMPLIANT', 0)),
        'source': 'Synthetic PMGSY QCR dataset (pmgsy_qcr_records)',
        'category': 'MEASURED PROJECT RESULTS'
    },
    {
        'graph_name': 'Distribution of Facility Categories in PMGSY Karnataka',
        'metric': 'Top Facility Categories & Counts',
        'value': 'See graph for details',
        'source': 'Pratap Vardhan PMGSY Facilities Dataset (pmgsy_clean)',
        'category': 'EXTERNAL GOVERNMENT CONTEXT'
    }
]

display(pd.DataFrame(data_summary))

print("\n### A. Strongest Graphs for SIH PPT")
print("1. Document AI / OCR Field Extraction Accuracy")
print("2. Quality Status Distribution in Synthetic QCR Dataset")
print("3. Distribution of Facility Categories in PMGSY Karnataka")

print("\n### B. Exact Figures and C. Official Source for Each Graph")
print(f"1. **Document AI / OCR Field Extraction Accuracy**: {oCR_accuracy_mean:.2f}% (from `accuracy_df` - project OCR evaluation on synthetic data).")
print(f"2. **Quality Status Distribution in Synthetic QCR Dataset**: Compliant: {int(quality_status_counts.get('COMPLIANT', 0))} records, Non-Compliant: {int(quality_status_counts.get('NON-COMPLIANT', 0))} records (from `pmgsy_qcr_records` - synthetic data generated in the project).")
print(f"3. **Distribution of Facility Categories in PMGSY Karnataka**: (See graph for detailed counts of top 10 categories) (from `pmgsy_clean` which originates from `https://github.com/pratapvardhan/rural-facilities-pmgsy`).")

print("\n### D. One-line PPT Caption for Each Graph")
print(f"1. **Document AI / OCR Field Extraction Accuracy**: Our AI system demonstrates a field extraction accuracy of approximately {oCR_accuracy_mean:.2f}% on simulated inspection reports.")
print("2. **Quality Status Distribution in Synthetic QCR Dataset**: Our synthetic dataset reflects a balanced distribution of compliant and non-compliant road quality scenarios for model training.")
print("3. **Distribution of Facility Categories in PMGSY Karnataka**: Rural road connectivity in Karnataka supports a diverse range of essential facilities, highlighting the broad impact of infrastructure development.")

print("\n### E. Limitations/Caveats about the Data")
print("""**Category 1 (Measured Project Results):**
- The OCR accuracy is based on *synthetic* PMGSY-grounded QCR documents, not real-world scanned documents, and is specific to the fields evaluated. Real-world performance may vary.
- The 'Quality Status Distribution' is based on *synthetic* data generation rules (80% compliant, 20% non-compliant) and represents the composition of our generated training data, not actual PMGSY road defect statistics.
- We currently lack measured data for end-to-end model performance (e.g., mAP for defect detection, full training/validation curves), before-vs-after preprocessing quantitative metrics (e.g., image quality scores), or direct comparisons of manual vs AI-assisted workflow efficiency (time/cost reduction).""")

print("""**Category 3 (External Government Context):**
- The 'Distribution of Facility Categories in PMGSY Karnataka' uses real external data, but it is from a specific state and may not represent the entire country or specific road quality assessment contexts. It serves as general ecosystem scale context.""")

print("""\n**Data Gaps:**
- **Model Performance Metrics**: We need actual precision, recall, F1-score, and mAP values from a trained Computer Vision model on road defect detection.
- **Training History**: Quantitative plots of training and validation loss/metrics over epochs are missing.
- **Real-world OCR/CV Data**: Evaluation of OCR and CV on actual, diverse, scanned inspection documents and road images would strengthen claims.
- **Workflow Efficiency**: Quantifiable measurements (e.g., time saved, manual effort reduced) for the AI-assisted workflow versus traditional manual methods are not yet available in the project data.""")



# ============================================================
# CELL
# ============================================================
!pip install -q streamlit pillow numpy opencv-python-headless easyocr



# ============================================================
# CELL
# ============================================================
!streamlit run app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false \
  --server.enableXsrfProtection false \
  > /content/qcr_streamlit.log 2>&1 &



# ============================================================
# CELL
# ============================================================
!pkill -f "streamlit run app.py" || true



# ============================================================
# CELL
# ============================================================
from google.colab import output

output.serve_kernel_port_as_iframe(
    8501,
    width="100%",
    height="900px"
)



# ============================================================
# CELL
# ============================================================
from google.colab.output import eval_js

url = eval_js("google.colab.kernel.proxyPort(8501)")
print(url)



# ============================================================
# CELL
# ============================================================
!cat /content/qcr_streamlit.log


