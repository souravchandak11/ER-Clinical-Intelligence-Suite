import time

class MedGemmaMock:
    @staticmethod
    def get_triage_response(chief_complaint: str, vitals: dict, has_image: bool = False):
        """
        Mocks the MedGemma multimodal triage response.
        Simulates processing latency.
        """
        # Simulate neural network latency
        time.sleep(0.5) 
        
        # Simple logic for mock ESI determination
        esi_level = 3
        reasoning = "Stable vitals, routine chief complaint."
        red_flags = []
        
        if vitals.get("hr", 0) > 120 or vitals.get("spo2", 100) < 90:
            esi_level = 2
            reasoning = "Abnormal vitals detected (tachycardia or hypoxia)."
            red_flags.append("Abnormal Vitals")
            
        if "chest pain" in chief_complaint.lower():
            esi_level = 2
            reasoning = "Chest pain in ER setting requires rapid evaluation for ACS."
            red_flags.append("Potential Cardiac Ischemia")
            
        if has_image:
            reasoning += " X-ray image processed and incorporated."
            
        return {
            "clinical_json": {
                "esi_level": esi_level,
                "reasoning": reasoning,
                "confidence_score": 0.92,
                "red_flag_conditions": red_flags,
                "suggested_follow_up": [
                    "When did this start?",
                    "Do you have a history of similar symptoms?",
                    "Are you on any blood thinners?"
                ],
                "recommended_next_steps": ["Consult MD"]
            },
            "patient_text": f"Based on your symptoms and vitals, you are assigned ESI level {esi_level}."
        }
