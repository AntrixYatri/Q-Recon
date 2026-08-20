import sys
import os
import unittest
from fastapi.testclient import TestClient

# Ensure backend/app folder is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

try:
    from app.main import app
    client = TestClient(app)
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Skipping FastAPI integration tests: dependencies not installed yet. Error: {str(e)}")
    BACKEND_AVAILABLE = False

class TestQCRBackend(unittest.TestCase):
    def test_health_check_fallback(self):
        """
        Verify that health check returns 200 and matches the expected JSON structure.
        """
        if not BACKEND_AVAILABLE:
            self.skipTest("FastAPI not available")
            
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertIn("service", data)

    def test_analyze_endpoint(self):
        """
        Verify that POST /analyze yields structured results matching project schemas.
        """
        if not BACKEND_AVAILABLE:
            self.skipTest("FastAPI not available")
            
        payload = {"analysis_id": "proj-101"}
        response = client.post("/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data.get("analysis_id"), "proj-101")
        self.assertIn("project", data)
        self.assertIn("summary", data)
        self.assertIn("discrepancies", data)
        
        # Schema field checks
        project = data["project"]
        self.assertIn("road_name", project)
        self.assertIn("package_id", project)
        
        summary = data["summary"]
        self.assertIn("total_discrepancies", summary)
        self.assertIn("critical", summary)
        
        discrepancies = data["discrepancies"]
        if discrepancies:
            first_disc = discrepancies[0]
            self.assertIn("field", first_disc)
            self.assertIn("severity", first_disc)
            self.assertIn("confidence", first_disc)

    def test_results_retrieval(self):
        """
        Verify GET /results/{id} correctly maps to report files.
        """
        if not BACKEND_AVAILABLE:
            self.skipTest("FastAPI not available")
            
        response = client.get("/results/proj-102")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("analysis_id"), "proj-102")

if __name__ == "__main__":
    unittest.main()
