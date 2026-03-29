import json
import os
from datetime import datetime


class PerformanceTracker:
    """
    Tracks scraper performance per county:
    - records found
    - success/fail
    - last run time
    """

    def __init__(self, file_path="performance.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def log_run(self, county, state, records_found, success=True, error=None):

        key = f"{county}-{state}"

        if key not in self.data:
            self.data[key] = {
                "runs": 0,
                "total_records": 0,
                "failures": 0,
                "last_run": None,
                "last_error": None
            }

        self.data[key]["runs"] += 1
        self.data[key]["total_records"] += records_found
        self.data[key]["last_run"] = datetime.utcnow().isoformat()

        if not success:
            self.data[key]["failures"] += 1
            self.data[key]["last_error"] = str(error)

        self._save()

    def get_summary(self):
        return self.data
