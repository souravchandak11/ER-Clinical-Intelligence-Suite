import random
import json
from typing import List, Dict, Any
from torch.utils.data import Dataset

class ESIDatasetLoader(Dataset):
    """
    Loader for ESI Triage guidelines.
    Focuses on classification training (Urgency Level 1-5).
    """
    def __init__(self, use_mock: bool = True):
        self.data = []
        if use_mock:
            self.data = self._generate_mock_data(200)

    def _generate_mock_data(self, num_samples: int) -> List[Dict[str, Any]]:
        mock_samples = []
        for i in range(num_samples):
            # Generate random vitals
            hr = random.randint(50, 150)
            sbp = random.randint(80, 200)
            spo2 = random.randint(85, 100)
            
            # Simple heuristic for ground truth in mock data
            if hr > 130 or spo2 < 90:
                esi = 1
            elif hr > 110 or sbp > 160:
                esi = 2
            elif hr > 90 or sbp > 140:
                esi = 3
            else:
                esi = 4

            prompt = f"Triage Assessment: HR {hr}, BP {sbp}/90, SpO2 {spo2}%. Determine ESI Level."
            target = f"ESI Level {esi}"

            mock_samples.append({
                "instruction": prompt,
                "output": target
            })
        return mock_samples

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
