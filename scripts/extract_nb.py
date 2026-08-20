import json
import os

notebook_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks", "SIH_QCR_AI_Engine (6).ipynb"))
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks", "extracted_code.py"))

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

code_cells = []
for cell in nb.get("cells", []):
    if cell.get("cell_type") == "code":
        source = cell.get("source", [])
        if source:
            code_cells.append(f"# {'='*60}\n# CELL\n# {'='*60}")
            code_cells.append("".join(source))
            code_cells.append("\n\n")

with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(code_cells))

print(f"Extracted code written to {output_path}")
