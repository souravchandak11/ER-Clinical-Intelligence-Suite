import pytest
from fastapi.testclient import TestClient
from backend.app.api.documentation import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router, prefix="/api")

client = TestClient(app)

def test_generate_note_success():
    payload = {
        "encounter_text": "Patient has severe 10/10 abdominal pain, guarding present.",
        "patient_context": {"patient_id": "P123", "age": 45, "gender": "F"},
        "encounter_type": "ER visit"
    }
    response = client.post("/api/generate-note", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Check JSON structure
    assert "json" in data
    assert "plain_text" in data
    assert "fhir" in data
    
    # Check SOAP content
    soap = data["json"]["soap_note"]
    assert "subjective" in soap
    assert "objective" in soap
    assert "assessment" in soap
    assert "plan" in soap
    
    # Check export formats
    assert "CLINICAL NOTE" in data["plain_text"]
    assert data["fhir"]["resourceType"] == "Composition"

def test_generate_note_template_missing():
    # Should fall back to 'general' template
    payload = {
        "encounter_text": "Simple checkup.",
        "patient_context": {"patient_id": "P456"},
        "encounter_type": "unknown-specialty"
    }
    response = client.post("/api/generate-note", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["json"]["metadata"]["encounter_type"] == "unknown-specialty"
    assert data["json"]["metadata"]["template_used"] == "Standard clinical encounter."
