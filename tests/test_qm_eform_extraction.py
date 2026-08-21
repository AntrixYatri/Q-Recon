import unittest
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.extraction.section_detector import detect_sections, get_section_for_yc
from ai_engine.extraction.checkbox_parser import parse_checkbox_status

class TestQMEFormExtraction(unittest.TestCase):
    def test_section_boundary_detection(self):
        lines = [
            {"text": "QUALITY MONITORING REPORT", "y": 100},
            {"text": "1. PROJECT DETAILS", "y": 200},
            {"text": "Road Name: ABC Link", "y": 250},
            {"text": "2. INSPECTION DETAILS", "y": 400},
            {"text": "Inspector Name: John Doe", "y": 450},
            {"text": "3. QUALITY OBSERVATIONS", "y": 600},
            {"text": "Thickness: 150mm", "y": 700},
            {"text": "4. REMARKS", "y": 900},
            {"text": "Acceptable limits", "y": 950}
        ]
        
        sections = detect_sections(lines)
        
        self.assertIn("project", sections)
        self.assertIn("inspection", sections)
        self.assertIn("quality", sections)
        self.assertIn("remarks", sections)
        
        self.assertEqual(sections["project"], (200, 400))
        self.assertEqual(sections["inspection"], (400, 600))
        self.assertEqual(sections["quality"], (600, 900))
        self.assertEqual(sections["remarks"], (900, float("inf")))
        
        # Test locating section for coordinate yc
        self.assertEqual(get_section_for_yc(250, sections), "project")
        self.assertEqual(get_section_for_yc(500, sections), "inspection")
        self.assertEqual(get_section_for_yc(750, sections), "quality")
        self.assertEqual(get_section_for_yc(1000, sections), "remarks")
        self.assertEqual(get_section_for_yc(150, sections), "unknown")

    def test_checkbox_parsing_compliant(self):
        self.assertEqual(parse_checkbox_status("[X] Compliant"), "compliant")
        self.assertEqual(parse_checkbox_status("[x] Pass"), "compliant")
        self.assertEqual(parse_checkbox_status("Result: [X] Approved"), "compliant")
        self.assertEqual(parse_checkbox_status("Status: Pass"), "compliant")

    def test_checkbox_parsing_non_compliant(self):
        self.assertEqual(parse_checkbox_status("[X] Non-Compliant"), "non-compliant")
        self.assertEqual(parse_checkbox_status("[x] Fail"), "non-compliant")
        self.assertEqual(parse_checkbox_status("Result: [X] Rejected"), "non-compliant")
        self.assertEqual(parse_checkbox_status("Quality Status: Non-Compliant"), "non-compliant")

if __name__ == "__main__":
    unittest.main()
