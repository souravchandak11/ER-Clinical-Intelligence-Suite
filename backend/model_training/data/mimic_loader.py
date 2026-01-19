import json
import random
from typing import List, Dict, Any
from torch.utils.data import Dataset

class MIMICDatasetLoader(Dataset):
    """
    Loader for MIMIC-IV style discharge summaries for SOAP note training.
    Includes a mock generator for pipeline verification.
    """
    def __init__(self, use_mock: bool = True, data_path: str = None):
        self.data = []
        if use_mock:
            self.data = self._generate_mock_data(100)
        elif data_path:
            self._load_from_path(data_path)

    def _generate_mock_data(self, num_samples: int) -> List[Dict[str, Any]]:
        complaints = ["Chest pain", "Shortness of breath", "Abdominal pain", "Laceration", "Fever"]
        vitals_pool = [
            {"hr": 110, "bp": "160/90", "spo2": 93, "temp": 99, "rr": 22},
            {"hr": 70, "bp": "120/80", "spo2": 98, "temp": 98.6, "rr": 16},
            {"hr": 95, "bp": "140/85", "spo2": 96, "temp": 101, "rr": 20}
        ]
        
        mock_samples = []
        for i in range(num_samples):
            cc = random.choice(complaints)
            vitals = random.choice(vitals_pool)
            
            # Simulated Prompt
            prompt = f"Patient presents with {cc}. Vitals: HR {vitals['hr']}, BP {vitals['bp']}, SpO2 {vitals['spo2']}%. Generate SOAP note."
            
            # Simulated Target (SOAP Note)
            target = {
                "subjective": f"Patient reports onset of {cc.lower()} approximately {random.randint(1, 5)} hours ago.",
                "objective": f"Vitals: HR {vitals['hr']}, BP {vitals['bp']}. Exam reveals alert patient in mild distress.",
                "assessment": f"Acute presentation of {cc}. Differential includes cardiac and respiratory causes.",
                "plan": "Perform ECG, order CBC and Troponin. Monitor vitals."
            }
            
            mock_samples.append({
                "instruction": prompt,
                "output": json.dumps(target)
            })
        return mock_samples

    def _load_from_path(self, path: str):
        # Implementation for real MIMIC JSONL files
        with open(path, 'r') as f:
            for line in f:
                self.data.append(json.loads(line))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
