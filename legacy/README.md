# ER Clinical Intelligence Suite

A multimodal AI-driven suite for Emergency Room clinical intelligence, built for the MedGemma Impact Challenge.

## Features
- **Multimodal Triage**: Analyzes clinical notes, vitals, and chest X-rays to suggest ESI levels.
- **Auto-Documentation**: Converts clinical notes into structured SOAP format using MedGemma.
- **Offline Capable**: Designed for edge deployment on hospital hardware.
- **HIPAA Compliant**: Integrated de-identification and secure data handling.

## Tech Stack
- **Backend**: FastAPI, MedGemma (7B, 4-bit quantized), PyTorch, Hugging Face Transformers.
- **Frontend**: React (Medical UI Components).
- **Deployment**: Docker, Docker Compose (NVIDIA GPU support).
- **Data**: MIMIC-IV, CheXpert, ESI Triage datasets.

## Getting Started
1. **Model Access**: Ensure you have access to `google/medgemma-7b`.
2. **Environment**: 
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Run Locally**:
   ```bash
   python -m backend.app.main
   ```
4. **Docker**:
   ```bash
   docker-compose up --build
   ```

## Architecture
- `backend/`: FastAPI services and MedGemma integration.
- `models/`: Model loading and preprocessing logic.
- `data/`: HIPAA-compliant data pipeline.
- `frontend/`: React-based medical interface.
- `docs/`: Technical diagrams and specs.
