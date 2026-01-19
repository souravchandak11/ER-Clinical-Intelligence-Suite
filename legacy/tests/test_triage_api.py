import pytest
from fastapi.testclient import TestClient
from backend.app.api.triage import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router, prefix="/api")

client = TestClient(app)

def test_triage_success():
    payload = {
        "text_input": "Severe abdominal pain for 2 hours",
        "vitals": {
            "HR": 95,
            "BP": "130/85",
            "SpO2": 96,
            "temp": 99.1,
            "RR": 18
        }
    }
    response = client.post("/api/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "clinical_json" in data
    assert "patient_text" in data
    assert data["clinical_json"]["esi_level"] in [1, 2, 3, 4, 5]

def test_triage_with_image():
    # Mock base64 image string (a tiny valid png pixel)
    base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    payload = {
        "text_input": "Shortness of breath and cough",
        "vitals": {
            "HR": 115,
            "BP": "110/70",
            "SpO2": 88,
            "temp": 101.5,
            "RR": 26
        },
        "image": base64_image
    }
    response = client.post("/api/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Should be ESI 1 or 2 due to low SpO2 and high HR
    assert data["clinical_json"]["esi_level"] in [1, 2]

def test_triage_vitals_validation():
    payload = {
        "text_input": "Test",
        "vitals": {
            "HR": 95,
            "BP": "130/85",
            "SpO2": 150, # Invalid SpO2
            "temp": 99.1,
            "RR": 18
        }
    }
    response = client.post("/api/triage", json=payload)
    assert response.status_code == 422 # Pydantic validation error
