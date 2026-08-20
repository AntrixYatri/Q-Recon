import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ai_engine.preprocessing.schema_normalizer import normalize_field_name
from ai_engine.data_integration.canonical_schema import CanonicalRecord

class TestSchemaMapping(unittest.TestCase):
    def test_alias_normalization(self):
        # Check standard normalizations
        self.assertEqual(normalize_field_name("road"), "road_name")
        self.assertEqual(normalize_field_name("road_name"), "road_name")
        self.assertEqual(normalize_field_name("name of road"), "road_name")
        self.assertEqual(normalize_field_name("inspection dt"), "inspection_date")
        self.assertEqual(normalize_field_name("district name"), "district")
        self.assertEqual(normalize_field_name("district"), "district")
        self.assertEqual(normalize_field_name("measured"), "measured_value")

    def test_canonical_record_set_get(self):
        record = CanonicalRecord()
        record.set_field("road_name", "NH-4 Bypass", "QCR", "road_name")
        self.assertEqual(record.get_value("road_name"), "NH-4 Bypass")
        
        with self.assertRaises(KeyError):
            record.set_field("invalid_field_name", "Value", "QCR", "invalid")

if __name__ == "__main__":
    unittest.main()
