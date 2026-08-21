import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.extraction.key_value_extractor import extract_key_values_from_lines
from ai_engine.extraction.table_extractor import extract_table_from_detections

class TestTestDatasheetExtraction(unittest.TestCase):
    def test_key_value_extractor_colon_split(self):
        lines = [
            {"text": "Project Code: PRJ-PMGSY-12345"},
            {"text": "Road Name: Shedbal Govt Hospital Link Road"},
            {"text": "Test Date:"},
            {"text": "12 Aug 2026"}
        ]
        res = extract_key_values_from_lines(lines)
        self.assertEqual(res.get("project_code"), "PRJ-PMGSY-12345")
        self.assertEqual(res.get("road_name"), "Shedbal Govt Hospital Link Road")
        self.assertEqual(res.get("inspection_date"), "12 Aug 2026")

    def test_key_value_extractor_no_colon(self):
        lines = [
            {"text": "Project Code PRJ-PMGSY-12345"},
            {"text": "Road Name Shedbal Govt Hospital Link Road"}
        ]
        res = extract_key_values_from_lines(lines)
        self.assertEqual(res.get("project_code"), "PRJ-PMGSY-12345")
        self.assertEqual(res.get("road_name"), "Shedbal Govt Hospital Link Road")

    def test_table_cell_clustering(self):
        # Setup mock detections for a horizontal table structure
        # Row 1 (Headers): Parameter (x=100-300), Required (x=400-550), Measured (x=600-750), Unit (x=800-900)
        # Row 2 (Data): Pavement Thickness, 150, 120, mm
        detections = [
            # Headers (Y=200)
            {"text": "Parameter", "xc": 200, "yc": 200, "height": 30, "x1": 100, "x2": 300},
            {"text": "Required", "xc": 475, "yc": 200, "height": 30, "x1": 400, "x2": 550},
            {"text": "Measured", "xc": 675, "yc": 200, "height": 30, "x1": 600, "x2": 750},
            {"text": "Unit", "xc": 850, "yc": 200, "height": 30, "x1": 800, "x2": 900},
            
            # Data Row (Y=270)
            {"text": "Pavement", "xc": 150, "yc": 270, "height": 30, "x1": 100, "x2": 200},
            {"text": "Thickness", "xc": 250, "yc": 270, "height": 30, "x1": 210, "x2": 300},
            {"text": "150", "xc": 475, "yc": 270, "height": 30, "x1": 450, "x2": 500},
            {"text": "120", "xc": 675, "yc": 270, "height": 30, "x1": 650, "x2": 700},
            {"text": "mm", "xc": 850, "yc": 270, "height": 30, "x1": 830, "x2": 870}
        ]
        
        rows = extract_table_from_detections(detections)
        self.assertEqual(len(rows), 1)
        
        row = rows[0]
        self.assertEqual(row.get("parameter"), "Pavement Thickness")
        self.assertEqual(row.get("required"), "150")
        self.assertEqual(row.get("measured"), "120")
        self.assertEqual(row.get("unit"), "mm")

if __name__ == "__main__":
    unittest.main()
