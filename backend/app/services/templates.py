from typing import Dict, Any

SPECIALTY_TEMPLATES = {
    "ER visit": {
        "description": "Emergency Department encounter with focus on acute presentation and triage.",
        "prompt_vignette": "Generate a SOAP note for an Emergency Department visit. Focus on chief complaint, acuity, and stabilization plan.",
        "quality_requirements": ["Acuity assessment", "Stabilization plan"]
    },
    "follow-up": {
        "description": "Routine follow-up for chronic or resolving issues.",
        "prompt_vignette": "Generate a clinical note for a follow-up visit. Focus on progress, medication compliance, and long-term management.",
        "quality_requirements": ["Progress assessment", "Medication reconciliation"]
    },
    "general": {
        "description": "Standard clinical encounter.",
        "prompt_vignette": "Generate a comprehensive structured SOAP note.",
        "quality_requirements": ["Completeness", "Clear Assessment & Plan"]
    }
}

def get_template(specialty: str) -> Dict[str, Any]:
    return SPECIALTY_TEMPLATES.get(specialty, SPECIALTY_TEMPLATES["general"])
