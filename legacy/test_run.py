import requests
import json

base_url = "http://localhost:8000/triage/multimodal"

print("--- STARTING API TEST ---")

# High Risk
high_risk = {
    "chief_complaint": "Severe chest pain",
    "vitals_json": json.dumps({"hr": 140, "bp_sys": 160, "bp_dia": 100, "spo2": 88, "temp": 98.6, "rr": 28})
}
try:
    r1 = requests.post(base_url, data=high_risk)
    print("\nHIGH RISK RESPONSE:")
    print(json.dumps(r1.json(), indent=2))
except Exception as e:
    print(f"High risk failed: {e}")
    
# Low Risk
low_risk = {
    "chief_complaint": "Stubbed toe",
    "vitals_json": json.dumps({"hr": 70, "bp_sys": 120, "bp_dia": 80, "spo2": 99, "temp": 98.6, "rr": 16})
}
try:
    r2 = requests.post(base_url, data=low_risk)
    print("\nLOW RISK RESPONSE:")
    print(json.dumps(r2.json(), indent=2))
except Exception as e:
    print(f"Low risk failed: {e}")
    
print("\n--- TEST COMPLETE ---")
