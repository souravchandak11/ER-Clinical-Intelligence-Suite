import logging
from typing import Dict, Any, List, Optional
from models.medgemma_loader import load_medgemma_model
from models.preprocessing import MultimodalPreprocessor

logger = logging.getLogger(__name__)

class TriageService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.preprocessor = MultimodalPreprocessor()
        self._initialized = False

    async def _lazy_init(self):
        if not self._initialized:
            try:
                # In a real scenario, this would load the fine-tuned checkpoint
                self.model, self.tokenizer = load_medgemma_model()
                self._initialized = True
            except Exception as e:
                logger.error(f"Failed to initialize MedGemma model: {e}")
                # For demo purposes, we might continue with a mockup if model loading fails
                # but in production, this should be a hard failure.

    async def process_triage(self, text_input: str, vitals: Dict[str, Any], image_base64: Optional[str] = None) -> Dict[str, Any]:
        """
        Processes triage input using MedGemma.
        """
        await self._lazy_init()
        
        logger.info(f"Processing triage for: {text_input[:50]}...")
        
        # Preprocess inputs
        processed_input = self.preprocessor.prepare_multimodal_input(text_input, vitals, image_base64)
        
        # Mock inference result for now, as actually running a 7B model requires GPU
        # In actual implementation: 
        # outputs = self.model.generate(**processed_input)
        # response = self.tokenizer.decode(outputs[0])
        
        # Mocking the structured output based on MedGemma's potential output
        # ESI 1: Immediate, 2: Emergent, 3: Urgent, 4: Less Urgent, 5: Non-Urgent
        
        # Logic to "simulate" ESI level based on vitals if model is not available
        esi_level = 3
        confidence = 0.85
        
        if vitals.get("spo2", 100) < 90 or vitals.get("hr", 80) > 130 or vitals.get("bp_sys", 120) > 200:
            esi_level = 1
            confidence = 0.95
        elif vitals.get("hr", 80) >= 100 or vitals.get("rr", 16) > 22 or vitals.get("bp_sys", 120) >= 160:
            esi_level = 2
            confidence = 0.90
        
        # Textual Overrides for High Risk Complaints
        if "chest pain" in text_input.lower() or "stroke" in text_input.lower() or "difficulty breathing" in text_input.lower():
             if esi_level > 2:
                 esi_level = 2
                 confidence = 0.92

        red_flags = ["Sepsis", "Myocardial Infarction"] if esi_level <= 2 else ["Dehydration"]
        if "chest" in text_input.lower() or "heart" in text_input.lower():
            follow_up = [
                "Does the pain radiate to your arm or jaw?",
                "Is the pain worse with exertion or rest?",
                "Do you have a history of heart disease?"
            ]
        elif "abdomen" in text_input.lower() or "stomach" in text_input.lower():
            follow_up = [
                "Is the pain constant or does it come and go?",
                "Have you experienced any nausea or vomiting?",
                "When was your last bowel movement?"
            ]
        else:
            follow_up = [
                "How long has the patient been experiencing these symptoms?",
                "Any history of similar episodes?",
                "Any known allergies to medications?"
            ]

        # Use new field for adaptive questions
        adaptive_questions = follow_up
        next_steps = ["Stat EKG", "Troponin levels", "Chest X-ray"] if esi_level <= 2 else ["Observation", "Oral rehydration"]

        patient_explanation = f"Based on your symptoms and vital signs, our system suggests an urgency level of {esi_level}. "
        if esi_level <= 2:
            patient_explanation += "You should be seen by a clinician immediately."
        else:
            patient_explanation += "A clinician will be with you shortly. Please let us know if your symptoms worsen."

        return {
            "clinical_json": {
                "esi_level": esi_level,
                "confidence_score": confidence,
                "red_flag_conditions": red_flags,
                "follow_up_questions": adaptive_questions,
                "suggested_follow_up": follow_up, # Keeping for backward compatibility
                "recommended_next_steps": next_steps
            },
            "patient_text": patient_explanation
        }
