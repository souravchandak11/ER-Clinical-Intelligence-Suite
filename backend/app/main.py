from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import base64
import uvicorn
import os
import time
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pyinstrument import Profiler
from fastapi.responses import HTMLResponse

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.services.ollama_service import OllamaService
from app.services.documentation_service import DocumentationService
from app.services.triage_service import TriageService
from app.services.privacy import deidentify_text
from app.services.audit import log_audit_event, engine
from sqlmodel import SQLModel

# Placeholder for MultimodalPreprocessor and SOAPResponse if they are new types
# from backend.app.services.multimodal_preprocessor import MultimodalPreprocessor
# class SOAPResponse(BaseModel):
#     ...

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="ER Clinical Intelligence Suite")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caching Initialization and Database Initialization
@app.on_event("startup")
async def startup_event():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
        
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        redis = aioredis.from_url(redis_url, encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    except Exception as e:
        print(f"Warning: Could not initialize cache: {e}")

# Profiling Middleware
@app.middleware("http")
async def profile_request(request: Request, call_next):
    if request.query_params.get("profile"):
        profiler = Profiler(interval=0.0001)
        profiler.start()
        response = await call_next(request)
        profiler.stop()
        return HTMLResponse(profiler.output_html())
    return await call_next(request)

# Global instances
# Assuming MultimodalPreprocessor is defined elsewhere or will be added
# preprocessor = MultimodalPreprocessor()

# Initialize Services
ollama = OllamaService()
doc_service = DocumentationService()
triage_service = TriageService()


class Vitals(BaseModel):
    hr: int = Field(..., ge=0, le=300, description="Heart Rate")
    bp_sys: int = Field(..., ge=0, le=300, description="Systolic Blood Pressure")
    bp_dia: int = Field(..., ge=0, le=200, description="Diastolic Blood Pressure")
    spo2: int = Field(..., ge=0, le=100, description="Oxygen Saturation")
    temp: float = Field(..., ge=70, le=115, description="Temperature in Fahrenheit")
    rr: int = Field(..., ge=0, le=100, description="Respiratory Rate")

class TriageResponse(BaseModel):
    esi_level: int
    reasoning: str
    confidence: float
    red_flags: List[str]
    follow_up_questions: List[str]
    recommended_next_steps: List[str]
    patient_explanation: str

class TriageRequest(BaseModel):
    chief_complaint: str
    vitals: Vitals
    image_base64: Optional[str] = None

class NoteRequest(BaseModel):
    encounter_text: str
    patient_context: Optional[str] = None
    encounter_type: str = "Emergency"

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ER Clinical Intelligence Suite"}

@app.post("/api/triage", response_model=TriageResponse)
@limiter.limit("5/minute")
@cache(expire=60)
async def multimodal_triage(
    request: Request,
    payload: TriageRequest
):
    try:
        # Log the action (HIPAA requirement)
        log_audit_event(user_id="anonymous_er_staff", action="TRIAGE_MULTIMODAL")
        
        # De-identify clinical notes before processing
        scrubbed_text = deidentify_text(payload.chief_complaint)
        
        # Simulate or call TriageService
        # For the test suite, we want consistent results
        result = await triage_service.process_triage(scrubbed_text, payload.vitals.dict(), payload.image_base64)
        
        # Map TriageService output (nested) to API Model (flat)
        clinical = result.get("clinical_json", {})
        
        return {
            "esi_level": clinical.get("esi_level", 3),
            "reasoning": clinical.get("reasoning", "Automated triage assessment based on vitals and notes."),
            "confidence": clinical.get("confidence_score", 0.0),
            "red_flags": clinical.get("red_flag_conditions", []),
            "follow_up_questions": clinical.get("suggested_follow_up", []),
            "recommended_next_steps": clinical.get("recommended_next_steps", []),
            "patient_explanation": result.get("patient_text", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-note")
@limiter.limit("10/minute")
@cache(expire=300)
async def generate_note(request: Request, payload: NoteRequest):
    try:
        log_audit_event(user_id="anonymous_er_staff", action="GENERATE_SOAP")
        
        # De-identify clinical notes
        scrubbed_text = deidentify_text(payload.encounter_text)
        
        patient_context = {"patient_id": "P-123"} # Default or parsed from payload.patient_context
        if payload.patient_context:
             patient_context["context"] = payload.patient_context

        return await doc_service.generate_note(scrubbed_text, patient_context, payload.encounter_type)
    except Exception as e:
        logger.error(f"Note generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
