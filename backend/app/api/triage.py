import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
from ..services.triage_service import TriageService

router = APIRouter()
logger = logging.getLogger(__name__)

# Request Models
class Vitals(BaseModel):
    HR: int = Field(..., description="Heart Rate (bpm)")
    BP: str = Field(..., description="Blood Pressure (e.g., '120/80')")
    SpO2: int = Field(..., description="Oxygen Saturation (%)")
    temp: float = Field(..., description="Body Temperature (F/C)")
    RR: int = Field(..., description="Respiratory Rate (breaths/min)")

    @validator('SpO2')
    def validate_spo2(cls, v):
        if v < 0 or v > 100:
            raise ValueError('SpO2 must be between 0 and 100')
        return v

class TriageRequest(BaseModel):
    text_input: str = Field(..., description="Patient's chief complaint")
    vitals: Vitals
    image: Optional[str] = Field(None, description="Base64 encoded X-ray image (optional)")

# Response Models
class TriageClinicalData(BaseModel):
    esi_level: int = Field(..., ge=1, le=5)
    confidence_score: float
    red_flag_conditions: List[str]
    follow_up_questions: List[str] = Field(..., description="3 focused follow-up questions for the nurse")
    suggested_follow_up: List[str]
    recommended_next_steps: List[str]

class TriageResponse(BaseModel):
    clinical_json: TriageClinicalData
    patient_text: str

# Dependency
def get_triage_service():
    return TriageService()

@router.post("/triage", response_model=TriageResponse, summary="Process patient triage")
async def process_triage(
    request: TriageRequest, 
    service: TriageService = Depends(get_triage_service)
):
    """
    Multimodal triage endpoint using MedGemma.
    Multimodal triage endpoint using MedGemma.
    Accepts chief complaint, vitals, and optional X-ray image.
    Returns ESI level, red flags, follow-up questions, and clinical recommendations.
    """
    try:
        logger.info(f"Received triage request: {request.text_input[:50]}")
        result = await service.process_triage(
            request.text_input,
            request.vitals.dict(),
            request.image
        )
        return result
    except Exception as e:
        logger.error(f"Error processing triage request: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred while processing the triage request."
        )
