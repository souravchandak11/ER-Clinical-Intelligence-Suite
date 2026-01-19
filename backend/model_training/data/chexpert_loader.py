import random
from typing import List, Dict, Any
from torch.utils.data import Dataset

class CheXpertLoader(Dataset):
    """
    Loader for CheXpert style radiology reasoning tasks.
    Simulates multimodal input (Image + Text).
    """
    def __init__(self, use_mock: bool = True):
        self.data = []
        if use_mock:
            self.data = self._generate_mock_data(50)

    def _generate_mock_data(self, num_samples: int) -> List[Dict[str, Any]]:
        conditions = ["Pneumonia", "Pneumothorax", "Cardiomegaly", "Pleural Effusion", "Normal"]
        
        mock_samples = []
        for i in range(num_samples):
            condition = random.choice(conditions)
            
            # In real case, 'image' would be a path or tensor
            # For mock, we use a placeholder or dummy feature vector
            prompt = "Analyze this chest X-ray and report findings."
            
            if condition == "Normal":
                target = "The heart size and mediastinal contours are normal. The lungs are clear. No pneumothorax or pleural effusion."
            else:
                target = f"Findings suggestive of {condition}. Opacification noted in the affected region. Clinical correlation recommended."

            mock_samples.append({
                "instruction": prompt,
                "image_path": f"dummy_path/xr_{i}.jpg",
                "output": target
            })
        return mock_samples

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
