import numpy as np

def extract_table_from_detections(detections: list, header_keywords: list = None) -> list:
    """
    Parses horizontal table structures from raw EasyOCR detections.
    
    1. Identifies header row based on keywords.
    2. Clusters horizontal coordinates to define column boundaries.
    3. Groups detections below header vertically into rows and maps them to columns.
    """
    if header_keywords is None:
        header_keywords = ["parameter", "required", "measured", "unit", "result", "value", "status"]

    # 1. Find the header detections
    # Group detections into visual lines first using line reconstruction
    from ai_engine.extraction.line_reconstruction import group_into_lines
    lines = group_into_lines(detections)
    
    header_line_idx = -1
    columns = [] # list of dicts: {"name": col_name, "x1": x1, "x2": x2, "xc": xc}

    for idx, line in enumerate(lines):
        line_text = line["text"].lower()
        matched_count = sum(1 for kw in header_keywords if kw in line_text)
        if matched_count >= 2: # At least 2 header keywords match
            header_line_idx = idx
            
            # Map detections on this line as header columns
            header_dets = sorted(line["detections"], key=lambda d: d["x1"])
            for h_det in header_dets:
                h_text = h_det["text"].lower()
                columns.append({
                    "name": h_text,
                    "x1": h_det["x1"],
                    "x2": h_det["x2"],
                    "xc": h_det["xc"]
                })
            break

    if header_line_idx == -1 or not columns:
        return []

    # 2. Extract rows below the header
    table_rows = []
    header_y = lines[header_line_idx]["y"]
    
    # Collect lines below header
    data_lines = [l for l in lines if l["y"] > header_y]

    for d_line in data_lines:
        row_cells = {col["name"]: [] for col in columns}
        # Associate each detection with the horizontally closest column
        for det in d_line["detections"]:
            best_col = None
            min_dist = float("inf")
            for col in columns:
                dist = abs(det["xc"] - col["xc"])
                if dist < min_dist:
                    min_dist = dist
                    best_col = col
            # Ensure it is reasonably close horizontally
            if best_col and min_dist < (best_col["x2"] - best_col["x1"]) * 3.5:
                row_cells[best_col["name"]].append(det)

        # Build clean row mapping
        clean_row = {}
        has_any = False
        for col_name, col_dets in row_cells.items():
            if col_dets:
                col_dets_sorted = sorted(col_dets, key=lambda d: d["x1"])
                cell_text = " ".join(d["text"] for d in col_dets_sorted)
                clean_row[col_name] = cell_text
                has_any = True
            else:
                clean_row[col_name] = ""
        
        # Only add row if it has content
        if has_any:
            table_rows.append(clean_row)

    return table_rows
