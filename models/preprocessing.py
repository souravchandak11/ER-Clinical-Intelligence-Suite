from PIL import Image
import torch
from transformers import AutoProcessor

class MultimodalPreprocessor:
    def __init__(self, model_id: str = "google/medgemma-7b"):
        # MedGemma might use a specific processor for multimodal tasks
        # Placeholder for actual processor initialization
        self.processor = None 
        # For now, we'll use standard PIL and torch transforms logic
        print(f"Initializing preprocessor for {model_id}")

    def preprocess_text(self, text: str):
        """
        Clean and tokenize clinical notes.
        """
        # Add medical-specific cleaning here
        cleaned_text = text.strip().replace("\n", " ")
        return cleaned_text

    def preprocess_image(self, image_base64: str = None):
        """
        Load and resize X-ray images from base64 string.
        """
        if not image_base64:
            return None
            
        import base64
        import io
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            return image
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None

    def prepare_multimodal_input(self, text: str, vitals: dict, image_base64: str = None):
        """
        Combines text, vitals, and image for the model.
        """
        cleaned_text = self.preprocess_text(text)
        
        # Format vitals into a clinical string for the model
        vitals_str = f"Vitals: HR {vitals.get('HR')}, BP {vitals.get('BP')}, SpO2 {vitals.get('SpO2')}%, Temp {vitals.get('temp')}, RR {vitals.get('RR')}."
        combined_prompt = f"{cleaned_text}\n{vitals_str}"
        
        image = self.preprocess_image(image_base64)
        
        return {
            "text": combined_prompt,
            "image": image
        }
