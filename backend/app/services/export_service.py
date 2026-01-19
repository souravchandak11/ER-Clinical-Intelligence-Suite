import json
from datetime import datetime
from typing import Dict, Any

class ExportService:
    @staticmethod
    def to_plain_text(note: Dict[str, Any]) -> str:
        text = f"CLINICAL NOTE - {datetime.now().isoformat()}\n"
        text += "="*40 + "\n"
        soap = note.get("soap_note", {})
        for section, content in soap.items():
            text += f"{section.upper()}:\n{content}\n\n"
        
        text += "ICD-10 CODES:\n" + ", ".join(note.get("icd10", [])) + "\n\n"
        text += "CPT CODES:\n" + ", ".join(note.get("cpt", [])) + "\n\n"
        text += "HANDOFF SUMMARY:\n" + note.get("handoff", "")
        return text

    @staticmethod
    def to_fhir(note: Dict[str, Any], patient_context: Dict[str, Any]) -> Dict[str, Any]:
        # Simplified FHIR Composition resource
        return {
            "resourceType": "Composition",
            "status": "final",
            "type": {
                "coding": [{"system": "http://loinc.org", "code": "11506-3", "display": "Provider-unspecified Progress note"}]
            },
            "subject": {
                "display": f"Patient ID: {patient_context.get('patient_id', 'Unknown')}"
            },
            "date": datetime.now().isoformat(),
            "author": [{"display": "MedGemma AI Generator"}],
            "title": "Clinical Encounter Note",
            "section": [
                {
                    "title": "SOAP Note",
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>{ExportService.to_plain_text(note).replace(chr(10), '<br/>')}</div>"
                    }
                }
            ]
        }

    @classmethod
    def format_all(cls, note: Dict[str, Any], patient_context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "json": note,
            "plain_text": cls.to_plain_text(note),
            "patient_handout": note.get("patient_handout", ""),
            "fhir": cls.to_fhir(note, patient_context)
        }
