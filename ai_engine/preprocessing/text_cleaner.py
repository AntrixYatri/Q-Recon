import re

def normalize_ocr_text(text: str) -> str:
    """
    Standardizes whitespace and punctuation characters.
    """
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" :", ":")
    text = re.sub(r":\s*", ": ", text)
    return text.strip()

def clean_label(label: str) -> str:
    """
    Normalizes labels (lowercases, removes colons) to enable keys mapping.
    """
    label = normalize_ocr_text(label)
    label = label.lower()
    label = label.replace(":", "")
    return label.strip()
