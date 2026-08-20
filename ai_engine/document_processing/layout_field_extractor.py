from ai_engine.config.settings import FIELD_LABELS
from ai_engine.preprocessing.ocr_normalizer import normalize_ocr_text

def clean_label(label: str) -> str:
    """
    Standardises labels (lowercase, trims whitespace, removes colons)
    to enable unified schema matching.
    """
    label = normalize_ocr_text(label)
    label = label.lower()
    label = label.replace(":", "")
    return label.strip()

def extract_from_reconstructed_lines(lines: list) -> dict:
    """
    Extracts QCR parameters from horizontal reconstructed lines.
    
    Case 1: Label and value reside on the same line (e.g. 'State: Karnataka').
    Case 2: The label resides on one line, and the value is on the next vertical line.
    """
    extracted = {}

    # Prepare normalized comparison strings
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

                # Match label at start of text line
                if line_text.startswith(label_clean):
                    value = line_text[len(label_clean):].strip()
                    value = value.lstrip(":")

                    # Case 1: Value is on the same line
                    if value:
                        extracted[field] = value.strip()
                        break

                    # Case 2: Label matches, but value is on the next line
                    if i + 1 < len(normalized_lines):
                        next_value = normalized_lines[i + 1]["original"]
                        extracted[field] = next_value.strip()
                        break
            
            if field in extracted:
                break

    return extracted
