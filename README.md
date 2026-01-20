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

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.9+ 
- Ollama (with MedGemma model)

### Installation
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/souravchandak11/ER-Clinical-Intelligence-Suite.git
    cd ER-Clinical-Intelligence-Suite
    ```

2.  **Setup Backend**
    ```bash
    cd backend
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload
    ```

3.  **Setup Frontend**
    ```bash
    npm install
    npm run dev
    ```

4.  **Access the Dashboard**
    Open `http://localhost:3000` to view the personalized clinician workspace.

## 🌐 Deployment (Cloudflare Tunnel)

Since the ER Clinical Intelligence Suite relies on local AI (MedGemma via Ollama), we recommend using **Cloudflare Tunnel** to securely expose your local backend to the internet.

### 1. Setup Cloudflare Tunnel
1.  **Install**: Download and install `cloudflared`.
2.  **Auth**: Run `cloudflared tunnel login`.
3.  **Create**: `cloudflared tunnel create er-suite`.
4.  **Route**: `cloudflared tunnel route dns er-suite your-domain.com`.
5.  **Run**: `cloudflared tunnel run --url http://localhost:8000 er-suite`.

### 2. Update Vercel
Set `BACKEND_URL` in Vercel to `https://your-domain.com`.

---

## 📈 Technical Roadmap
- [x] Multimodal Triage Support
- [x] SOAP Note Generation
- [x] Interactive 3D Anatomy Visualizer
- [ ] Real-time HL7/FHIR Integration
- [ ] Multi-patient Monitoring Queue
- [ ] EHR-integrated Export Plugin
