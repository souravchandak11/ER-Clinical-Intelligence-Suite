import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import json
from unittest.mock import patch, MagicMock
from tests.mocks.medgemma_mock import MedGemmaMock

client = TestClient(app)

def test_triage_flow_normal():
    vitals = {
        "hr": 70,
        "bp_sys": 115,
        "bp_dia": 75,
        "spo2": 99,
        "temp": 98.4,
        "rr": 14
    }
    
    # Mock the internal triage_service.process_triage call
    mock_result = MedGemmaMock.get_triage_response("Stubbed toe", vitals)
    
    with patch("backend.app.main.triage_service.process_triage", return_value=mock_result), \
         patch("backend.app.main.log_audit_event"):
        response = client.post(
            "/triage/multimodal",
            data={
                "chief_complaint": "Stubbed toe, slight pain.",
                "vitals_json": json.dumps(vitals)
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["esi_level"] == 3
        assert "Stable vitals" in data["reasoning"]

def test_triage_flow_urgent():
    vitals = {
        "hr": 130,
        "bp_sys": 140,
        "bp_dia": 90,
        "spo2": 88,
        "temp": 101.5,
        "rr": 28
    }
    
    mock_result = MedGemmaMock.get_triage_response("Shortness of breath", vitals)
    
    with patch("backend.app.main.triage_service.process_triage", return_value=mock_result), \
         patch("backend.app.main.log_audit_event"):
        response = client.post(
            "/triage/multimodal",
            data={
                "chief_complaint": "Severe shortness of breath and chest tightness.",
                "vitals_json": json.dumps(vitals)
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["esi_level"] == 2
        assert "Abnormal vitals" in data["reasoning"]

def test_triage_invalid_vitals_json():
    response = client.post(
        "/triage/multimodal",
        data={
            "chief_complaint": "Test",
            "vitals_json": "invalid-json"
        }
    )
    # The endpoint catches json.loads errors and raises 422 if it fails Vitals(**dict)
    # In main.py: try: vitals_dict = json.loads(vitals_json); vitals = Vitals(**vitals_dict)
    assert response.status_code == 500 or response.status_code == 422 # Depends on where it fails
