import re

def parse_checkbox_status(text: str) -> str:
    """
    Parses compliance status from checkboxes ([X] / [ ]) or textual status values.
    Uses robust neighborhood matching when both compliant and non-compliant keywords are present.
    Returns 'compliant', 'non-compliant', or None.
    """
    if not text:
        return None

    text_lower = text.lower()

    # Define keyword groups
    comp_kws = ["compliant", "pass", "approved", "yes"]
    non_comp_kws = ["non-compliant", "non compliant", "fail", "rejected", "no"]

    # Exclude non-compliant occurrences to check if compliant is genuinely present
    temp_text = text_lower.replace("non-compliant", "").replace("non compliant", "")
    has_comp = any(kw in temp_text for kw in comp_kws)
    has_non_comp = any(kw in text_lower for kw in non_comp_kws)

    # 1. Proximity matching when both keywords are present in the same line
    if has_comp and has_non_comp:
        # Find compliant position by masking non-compliant substrings
        cleaned_for_comp = text_lower.replace("non-compliant", "non-xxxxxxxxx").replace("non compliant", "non xxxxxxxxx")
        comp_pos = -1
        for kw in comp_kws:
            idx = cleaned_for_comp.find(kw)
            if idx != -1:
                comp_pos = idx
                break

        non_comp_pos = -1
        for kw in non_comp_kws:
            idx = text_lower.find(kw)
            if idx != -1:
                non_comp_pos = idx
                break

        if comp_pos != -1 and non_comp_pos != -1:
            def is_checked_neighborhood(pos: int) -> bool:
                # When both labels are on the same line, the checkbox always precedes the label.
                # So we inspect only the left window of the keyword position.
                start_idx = max(0, pos - 10)
                window = text_lower[start_idx:pos + 1]
                
                # Check for filled checkbox indicators: [x], [x, x], [v], [1], [*, [+, [y, x]
                if (re.search(r"\[\s*[x1v*+y]\s*\]", window) or 
                    re.search(r"\[\s*[x1v*+y]", window) or 
                    re.search(r"[x1v*+y]\s*\]", window)):
                    return True
                return False

            comp_checked = is_checked_neighborhood(comp_pos)
            non_comp_checked = is_checked_neighborhood(non_comp_pos)

            if comp_checked and not non_comp_checked:
                return "compliant"
            if non_comp_checked and not comp_checked:
                return "non-compliant"

    # 2. Check single keyword occurrences
    if has_non_comp and not has_comp:
        if (re.search(r"\[\s*[x1v*+y]\s*\]", text_lower) or 
            re.search(r"\[\s*[x1v*+y]", text_lower) or 
            re.search(r"[x1v*+y]\s*\]", text_lower)):
            return "non-compliant"
        if "status:" in text_lower or "result:" in text_lower or "quality:" in text_lower:
            return "non-compliant"

    if has_comp and not has_non_comp:
        if (re.search(r"\[\s*[x1v*+y]\s*\]", text_lower) or 
            re.search(r"\[\s*[x1v*+y]", text_lower) or 
            re.search(r"[x1v*+y]\s*\]", text_lower)):
            return "compliant"
        if "status:" in text_lower or "result:" in text_lower or "quality:" in text_lower:
            return "compliant"

    # 3. Direct plaintext matches (e.g. "status: pass")
    if "status: pass" in text_lower or "status: compliant" in text_lower:
        return "compliant"
    if "status: fail" in text_lower or "status: non-compliant" in text_lower:
        return "non-compliant"

    return None
