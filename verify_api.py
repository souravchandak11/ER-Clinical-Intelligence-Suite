import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_triage():
    print("Testing Triage API...")
    payload = {
        "text_input": "I have severe chest pain radiating to my left arm.",
        "vitals": {"HR": 110, "BP": "140/90", "SpO2": 98, "temp": 98.6, "RR": 22}
    }
    try:
        response = requests.post(f"{BASE_URL}/triage", json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Check for Adaptive Questions
        questions = data.get("clinical_json", {}).get("follow_up_questions", [])
        if questions:
            print(f"✅ Adaptive Questions Received: {len(questions)}")
            print(f"   Example: {questions[0]}")
        else:
            print("❌ No Adaptive Questions found.")
            
    except Exception as e:
        print(f"❌ Triage Test Failed: {e}")

def test_note():
    print("\nTesting Note Generation API...")
    payload = {
        "encounter_text": "Patient with chest pain. EKG shows ST elevation. Administered aspirin.",
        "patient_context": {"age": 65, "gender": "Male"},
        "encounter_type": "Emergency"
    }
    try:
        response = requests.post(f"{BASE_URL}/generate-note", json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Check for Patient Handout
        handout = data.get("patient_handout")
        if handout:
            print(f"✅ Patient Handout Received: {len(handout)} chars")
            print(f"   Preview: {handout[:50]}...")
        else:
            print("❌ No Patient Handout found.")
            
    except Exception as e:
        print(f"❌ Note Test Failed: {e}")

if __name__ == "__main__":
    test_triage()
    test_note()
