import os
import json
from data.utils.hipaa_utils import deidentify_text

class MIMICLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_note(self, note_id: str):
        # Simulated loading of a MIMIC-IV note
        # In practice, this would read from a database or CSV
        raw_note = "Patient presents with acute chest pain. HR 110, BP 140/90. History of COPD."
        return deidentify_text(raw_note)

class CheXpertLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def get_image_path(self, patient_id: str):
        # Simulated path mapping
        return os.path.join(self.data_dir, "sample_xray.jpg")

class ESILoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def get_triage_example(self, case_id: str):
        # Simulated ESI decision logic/data
        return {
            "vitals": {"temp": 98.6, "hr": 110, "rr": 24},
            "complaint": "Shortness of breath",
            "esi_level": 2
        }
