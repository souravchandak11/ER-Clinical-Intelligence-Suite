import base64
import io
from PIL import Image
from typing import Optional

class MultimodalPreprocessor:
    """
    Preprocessor for multimodal inputs (images) for MedGemma.
    Handles Base64 decoding, resizing, and normalization if needed.
    """
    
    @staticmethod
    def process_image(image_base64: Optional[str]) -> Optional[Image.Image]:
        """
        Convert base64 string to PIL Image.
        
        Args:
            image_base64: Base64 encoded image string (with or without data URI prefix).
            
        Returns:
            PIL Image object or None if input is invalid/empty.
        """
        if not image_base64:
            return None
            
        try:
            # Remove data URI prefix if present
            if "base64," in image_base64:
                image_base64 = image_base64.split("base64,")[1]
                
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB (remove alpha channel if present)
            if image.mode != "RGB":
                image = image.convert("RGB")
                
            return image
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def prepare_multimodal_input(self, text: str, vitals: dict, image_base64: Optional[str] = None):
        """
        Prepare inputs for the model.
        Returns a dictionary of inputs.
        """
        image = self.process_image(image_base64)
        # In a real implementation this would tokenize and tensorize
        return {
            "text": text,
            "vitals": vitals,
            "image_obj": image
        }
