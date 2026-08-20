import os
import json

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))

class ReportService:
    @staticmethod
    def save_analysis_result(analysis_id: str, data: dict) -> str:
        """
        Saves the analysis results as a JSON report in the data directory.
        """
        os.makedirs(DATA_DIR, exist_ok=True)
        report_path = os.path.join(DATA_DIR, f"report_{analysis_id}.json")
        with open(report_path, "w") as f:
            json.dump(data, f, indent=2)
        return report_path

    @staticmethod
    def get_analysis_result(analysis_id: str) -> dict:
        """
        Loads and returns the saved JSON audit report. If not found, triggers a live analysis.
        """
        report_path = os.path.join(DATA_DIR, f"report_{analysis_id}.json")
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                return json.load(f)
        
        # If file does not exist, run a new analysis via the AnalysisService
        from app.services.analysis_service import AnalysisService
        live_result = AnalysisService.run_analysis(analysis_id)
        ReportService.save_analysis_result(analysis_id, live_result)
        return live_result
