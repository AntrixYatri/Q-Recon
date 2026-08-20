import re

def normalize_ocr_text(text: str) -> str:
    """
    Cleans up raw OCR texts by normalising whitespace,
    removing space before colons, and spacing correctly after colons.
    """
    text = str(text).strip()

    # Collapse multiple whitespace
    text = re.sub(r"\s+", " ", text)

    # Clean punctuation spaces around colons
    text = text.replace(" :", ":")
    text = re.sub(r":\s*", ": ", text)

    return text.strip()

# Post-processing normalization helper functions.
