import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.pipeline import analyze_documents

class TestMultiDocumentPipeline(unittest.TestCase):
    def test_multi_document_pipeline_workflow(self):
        # Case 8: Three-document disagreement (consensus checking)
        from ai_engine.testing.pmgsy_fixture_factory import create_pmgsy_grounded_base_record
        from ai_engine.testing.discrepancy_scenario_factory import create_scenario
        
        base_record = create_pmgsy_grounded_base_record(15, seed=42)
        document_inputs = create_scenario(base_record, "majority_consensus")

        res = analyze_documents(document_inputs)
        self.assertEqual(res["processing_status"], "success")
        self.assertEqual(res["documents_analyzed"], 3)
        self.assertEqual(res["summary"]["total_discrepancies"], 1) # Only 1 discrepancy (the outlier TEST-001)

        disc = res["discrepancies"][0]
        self.assertEqual(disc["field"], "measured_value")
        self.assertEqual(disc["discrepancy_type"], "numerical_mismatch")

if __name__ == "__main__":
    unittest.main()
