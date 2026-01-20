# ER Clinical Intelligence Suite 🏥⚡

### *Next-Generation AI Dashboard for Emergency Medicine*

![Dashboard Preview](https://github.com/souravchandak11/ER-Clinical-Intelligence-Suite/raw/main/public/preview.png) *(Placeholder for your image)*

---

## 🛑 The Core Problem
Emergency Departments (EDs) worldwide are facing a triple crisis:
1.  **Triage Delays**: Manual triage takes too long, leading to patient "boarding" and delayed care for critical cases.
2.  **Documentation Burden**: Physicians spend **2 hours on paperwork for every 1 hour of care**, leading to severe burnout.
3.  **Multimodal Gaps**: Vital signs, physician notes, and imaging (X-rays) are often siloed, preventing a holistic view of patient urgency.

## ✅ What it Solves
The ER Clinical Intelligence Suite acts as an **AI-powered co-pilot for clinicians**, accelerating the journey from the waiting room to the treatment zone.

- **Unified Triage**: Combines text-based complaints, live vitals, and diagnostic images into a single urgency score (ESI Level).
- **Instant Documentation**: Converts unstructured doctor-patient conversations into structured, audit-ready SOAP notes in seconds.
- **Visual Intelligence**: Provides interactive 3D anatomical models to visualize patient condition and health metrics at a glance.

## 🛠️ How it Solves (The Tech)
### 1. Multimodal AI Integration
Using a fine-tuned **MedGemma** model, the suite performs high-stakes clinical tasks:
- **Triage Analysis**: A multimodal pipeline that processes text (complaints), data (vitals), and images (LoRA-weighted X-ray reasoning).
- **SOAP Engine**: Specialized LLM prompts generate Subjective, Objective, Assessment, and Plan sections with automatic **ICD-10 & CPT coding**.

### 2. Clinical Privacy & Security
- **PII Scrubbing**: Built-in de-identification engine that removes Personal Health Information (PHI) before AI processing, ensuring HIPAA compliance.
- **Audit Logging**: Every AI-generated clinical decision is logged for medical-legal verification.

### 3. Integrated Experience
- **Frontend**: A high-performance **Next.js** dashboard using **tRPC** for type-safe server communication and **Glassmorphism** UI for a premium, low-friction clinician experience.
- **Backend**: A robust **FastAPI** service with Redis caching and rate-limiting to handle the high density of ER data.

---

## 🌐 Live Demo & Deployment

The application is deployed as a hybrid architecture using **Vercel** for the frontend and a **Cloudflare Tunnel** to securely bridge to a local backend powered by **MedGemma** via **Ollama**.

*   **Frontend (Vercel):** [https://clinical-intelligence-suite.vercel.app/](https://clinical-intelligence-suite.vercel.app/)
*   **Backend (Local via Cloudflare):** `https://dec-plays-icons-nhs.trycloudflare.com`

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- **Node.js**: 18.x or 20.x
- **Python**: 3.9+
- **Docker**: For running PostgreSQL and Redis
- **Ollama**: To serve the MedGemma model locally

### 1. Installation
```bash
git clone https://github.com/souravchandak11/ER-Clinical-Intelligence-Suite.git
cd ER-Clinical-Intelligence-Suite
npm install
```

### 2. Infrastructure (Databases)
Start the database and cache using Docker:
```bash
docker-compose up -d db redis
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Note: Ensure Ollama is running (`ollama serve`) and the MedGemma model is pulled (`ollama pull medgemma`).*

### 4. Frontend Setup
```bash
# From the root directory
npm run dev
```
Open `http://localhost:3000`.

---

## ☁️ Setting Up the Hybrid Cloud (Cloudflare Tunnel)

To allow the Vercel-hosted frontend to communicate with your local PC's AI models:

1.  **Expose the Backend:**
    ```bash
    cloudflared tunnel --url http://localhost:8000
    ```
    *This will generate a temporary URL like `https://xyz.trycloudflare.com`.*

2.  **Configure Vercel:**
    - Go to your Vercel Project Settings -> Environment Variables.
    - Set `BACKEND_URL` to your Cloudflare URL.
    - Redeploy the application.

---

## 📈 Technical Roadmap
- [x] Multimodal Triage Support (Text, Vitals, Images)
- [x] SOAP Note Generation with ICD-10 Coding
- [x] Interactive 3D Anatomy Visualizer
- [x] Secure Cloud-to-Local Bridge (Cloudflare Tunnel)
- [ ] Real-time HL7/FHIR Integration
- [ ] Multi-patient Monitoring Queue
- [ ] EHR-integrated Export Plugin

