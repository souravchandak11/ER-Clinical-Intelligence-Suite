from locust import HttpUser, task, between
import random

class ERCachingUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def test_triage(self):
        # Common queries to test caching
        queries = [
            "Patient with severe chest pain and shortness of breath.",
            "Minor fall, scraped knee, no loss of consciousness.",
            "High fever 102F, persistent cough for 3 days."
        ]
        self.client.post("/triage/multimodal", data={
            "text": random.choice(queries),
            "hr": 110,
            "bp_sys": 140,
            "bp_dia": 90,
            "spo2": 94,
            "temp": 99.5,
            "rr": 22
        })

    @task(1)
    def test_documentation(self):
        self.client.post("/document/soap", params={
            "notes": "Patient reports worsening headache and nausea. Vitals stable.",
            "patient_id": "P-456",
            "encounter_type": "ER visit"
        })

    @task(5)
    def test_health(self):
        self.client.get("/health")
