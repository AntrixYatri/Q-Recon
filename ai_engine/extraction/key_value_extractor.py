from ai_engine.preprocessing.schema_normalizer import normalize_field_name

def extract_key_values_from_lines(lines: list) -> dict:
    """
    Parses key-value metadata from reconstructed text lines.
    
    1. Splits lines on colons ':'.
    2. Searches for canonical key labels in lines and retrieves values.
    3. Handles multi-line values where a label stands alone and the value is on the next line.
    """
    extracted = {}
    normalized_lines = []
    
    for idx, line in enumerate(lines):
        line_text = line["text"]
        normalized_lines.append({
            "index": idx,
            "text": line_text.strip(),
            "lower": line_text.lower().strip()
        })

    for i, line in enumerate(normalized_lines):
        line_text = line["text"]
        line_lower = line["lower"]
        
        # Scenario 1: Colon separation
        if ":" in line_text:
            parts = line_text.split(":", 1)
            raw_key = parts[0].strip()
            raw_val = parts[1].strip()
            
            canonical_key = normalize_field_name(raw_key)
            if canonical_key and raw_val:
                extracted[canonical_key] = raw_val
                continue
            elif canonical_key and not raw_val:
                # Key present but value is empty (might be on the next line)
                if i + 1 < len(normalized_lines):
                    extracted[canonical_key] = normalized_lines[i + 1]["text"]
                    continue

        # Scenario 2: Keyword match without colon
        # Sort aliases by length descending to match the longest label first
        from ai_engine.preprocessing.schema_normalizer import FIELD_ALIASES
        sorted_aliases = sorted(FIELD_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)
        
        for alias, canonical_key in sorted_aliases:
            alias_clean = alias.replace("_", " ")
            if line_lower.startswith(alias_clean):
                val_candidate = line_text[len(alias_clean):].strip()
                val_candidate = val_candidate.lstrip(":").strip()
                if val_candidate:
                    extracted[canonical_key] = val_candidate
                    break
                elif i + 1 < len(normalized_lines):
                    extracted[canonical_key] = normalized_lines[i + 1]["text"]
                    break
                    
    return extracted
