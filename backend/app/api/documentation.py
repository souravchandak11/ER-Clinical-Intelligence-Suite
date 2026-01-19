from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from ..services.documentation_service import DocumentationService

router = APIRouter()
doc_service = DocumentationService()

class GenerateNoteRequest(BaseModel):
    encounter_text: str
    patient_context: Dict[str, Any]
    encounter_type: str

class QualityCheckResult(BaseModel):
    is_complete: bool
    issues: List[str]

class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str

class GenerateNoteResponse(BaseModel):
    json: Dict[str, Any]
    plain_text: str
    patient_handout: str
    fhir: Dict[str, Any]

@router.post("/generate-note", response_model=GenerateNoteResponse)
async def generate_note(request: GenerateNoteRequest):
    try:
        note = await doc_service.generate_note(
            request.encounter_text,
            request.patient_context,
            request.encounter_type
        )
        return note
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
