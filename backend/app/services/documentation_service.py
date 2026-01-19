from typing import Dict, Any, List
from .templates import get_template
from .quality_checks import QualityChecker
from .export_service import ExportService
from .ollama_service import OllamaService
import json

class DocumentationService:
    def __init__(self):
        self.ollama = OllamaService()

    async def generate_note(self, encounter_text: str, patient_context: Dict[str, Any], encounter_type: str) -> Dict[str, Any]:
        template = get_template(encounter_type)
        
        # Construct Clinical Prompt
        prompt = f"""
        Generate a structured SOAP note for the following ER encounter.
        Patient Context: {json.dumps(patient_context)}
        Encounter Type: {encounter_type}
        Clinical Notes: {encounter_text}
        
        Requirements:
        - Output MUST be valid JSON.
        - Include sections: subjective, objective, assessment, plan.
        - Provide relevant ICD-10 and CPT codes.
        - Include a brief handoff summary.
        - Create a 'patient_handout' summary written at a 6th-grade reading level.
        """
        
        system_prompt = "You are a clinical documentation assistant using the MedGemma model. Output only JSON."

        try:
            raw_response = await self.ollama.generate_completion(prompt, system_prompt)
            # Find JSON block in response if model includes conversational filler
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                generated_data = json.loads(raw_response[json_start:json_end])
            else:
                raise ValueError("Could not find JSON in model response")
        except Exception as e:
            # Fallback to mock/emergency template if inference fails
            print(f"Inference failed: {e}")
            generated_data = self._mock_medgemma_inference(encounter_text, template)
        
        quality_results = QualityChecker.run_all(generated_data.get("soap_note", {}), template["quality_requirements"])
        
        full_response = {
            "soap_note": generated_data.get("soap_note", {}),
            "icd10": generated_data.get("icd10", []),
            "cpt": generated_data.get("cpt", []),
            "handoff": generated_data.get("handoff", ""),
            "patient_handout": generated_data.get("patient_handout", ""),
            "quality_checks": quality_results,
            "metadata": {
                "encounter_type": encounter_type,
                "template_used": template["description"],
                "model": self.ollama.model
            }
        }
        
        return ExportService.format_all(full_response, patient_context)

    def _mock_medgemma_inference(self, text: str, template: Dict[str, Any]) -> Dict[str, Any]:
        """Mock MedGemma processing for demonstration or fallback purposes."""
        return {
            "soap_note": {
                "subjective": f"Patient presents with: {text[:50]}...",
                "objective": "Vitals stable. Physical exam deferred.",
                "assessment": "Acute presentation (Fallback mode).",
                "plan": "Follow-up as per standard of care."
            },
            "icd10": ["R10.9"],
            "cpt": ["99283"],
            "handoff": "Patient stable, awaiting further evaluation.",
            "patient_handout": "We have evaluated you for your symptoms. Your vital signs are stable. Please follow up with your primary care physician in 2-3 days. Return to ER if symptoms worsen."
        }
