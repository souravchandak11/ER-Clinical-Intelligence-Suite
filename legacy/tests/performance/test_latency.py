import time
import json
from fastapi.testclient import TestClient
from backend.app.main import app
from unittest.mock import patch
from tests.mocks.medgemma_mock import MedGemmaMock

client = TestClient(app)

def test_api_latency():
    vitals = {
        "hr": 80, "bp_sys": 120, "bp_dia": 80,
        "spo2": 98, "temp": 98.6, "rr": 16
    }
    
    mock_result = MedGemmaMock.get_triage_response("Perf test", vitals)
    
    start_time = time.time()
    
    with patch("backend.app.main.triage_service.process_triage", return_value=mock_result), \
         patch("backend.app.main.log_audit_event"):
        response = client.post(
            "/triage/multimodal",
            data={
                "chief_complaint": "Performance test case.",
                "vitals_json": json.dumps(vitals)
            }
        )
    
    end_time = time.time()
    latency = end_time - start_time
    
    print(f"\nAPI Latency: {latency:.4f} seconds")
    
    assert response.status_code == 200
    assert latency < 2.0, f"Latency {latency:.4f}s exceeded 2.0s limit"
