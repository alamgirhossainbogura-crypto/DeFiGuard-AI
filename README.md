# 🛡️ DeFiGuard AI

**Autonomous Smart Contract & DeFi Risk Intelligence Platform** powered by Google Gemini, Google ADK, Elasticsearch, Firestore, and FastAPI.

---

## 🌟 Overview

DeFiGuard-AI is an autonomous agentic security platform built with **Google's Agent Development Kit (ADK)** to inspect, reason about, and report vulnerabilities in smart contracts (Solidity/Rust) before deployment. The agent combines deep-code reasoning from **Gemini 3.5** with hybrid historical threat retrieval via **Elasticsearch**, and persists scan history to **Google Cloud Firestore**.

Built for the **All Things Agentic Hackathon** — Taskmaster track.

🔗 **GitHub Repository:** [alamgirhossainbogura-crypto/DeFiGuard-AI](https://github.com/alamgirhossainbogura-crypto/DeFiGuard-AI)

---

## 🚀 Key Features

- **Autonomous ADK Agent:** Built on Google's Agent Development Kit — the agent independently decides when to call the vulnerability-retrieval tool versus reasoning directly over the code, rather than following a hardcoded pipeline.
- **Hybrid Threat Retrieval:** Elasticsearch tool integration matches smart contract names/patterns against known historical exploit signatures.
- **Persistent Scan History:** Every scan result is written to Firestore, so past audits can be retrieved via `/scan-history`.
- **High-Performance Backend:** FastAPI with scoped CORS, input validation, and safe error handling (no internal errors leaked to clients).
- **Interactive Frontend:** Streamlit dashboard with real backend health checks (no hardcoded status).
- **Cloud-Native:** Containerized with Docker and deployed on **Google Cloud Run**.

---

## 🏗️ Architecture & Project Structure
```text
DeFiGuard-AI/
│
├── agent_runtime/
│ ├── orchestrator.py # ADK Agent definition + Elasticsearch tool
│ └── runner.py # ADK Runner + session management
│
├── backend/
│ └── main.py # FastAPI server & API endpoint routing
│
├── frontend/
│ └── app.py # Streamlit web dashboard interface
│
├── retrieval/
│ ├── elastic_client.py # Elasticsearch historical threat retriever
│ └── firestore_client.py # Firestore scan history persistence
│
├── Dockerfile # Container definition for Cloud Run
├── .env.example # Environment variables template
├── .gitignore
├── LICENSE # Apache 2.0 License
├── README.md
└── requirements.txt
```
---
*(Architecture diagram: see `docs/architecture.png` — TODO: add diagram)*

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Model** | Google Gemini 3.5 (via Gemini API / Google AI Studio) |
| **Agent Framework** | Google Agent Development Kit (`google-adk==2.5.0`) |
| **Retrieval** | Elasticsearch (BM25 pattern matching) |
| **Persistence** | Google Cloud Firestore |
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Streamlit, Requests |
| **Cloud Infra** | Google Cloud Run |

---

## 🚀 Getting Started & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/alamgirhossainbogura-crypto/DeFiGuard-AI.git
cd DeFiGuard-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash

ELASTIC_ENDPOINT=your_elasticsearch_endpoint_here
ELASTIC_API_KEY=your_elasticsearch_api_key_here

GOOGLE_CLOUD_PROJECT=your_gcp_project_id_here

ALLOWED_ORIGINS=http://localhost:8501
```

### 4. Run the Backend Server (local)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Launch the Frontend Dashboard
In a new terminal:
```bash
streamlit run frontend/app.py
```

### 6. Deploy to Google Cloud Run
```bash
gcloud run deploy defiguard-backend \
  --source . \
  --region us-central1 \
  --set-env-vars GEMINI_MODEL=gemini-3.5-flash,GOOGLE_CLOUD_PROJECT=your_gcp_project_id \
  --allow-unauthenticated
```
After deployment, update `ALLOWED_ORIGINS` in your backend env and `API_URL` in `frontend/app.py` to point to the deployed Cloud Run URL.

---
### ⚠️ Deployment Status

Cloud Run deployment was fully prepared (Dockerfile, deploy command, and 
environment configuration are included above and were tested against a 
live GCP project). However, deployment could not be completed at 
submission time because Google Cloud requires a payment method on file 
to activate billing — even for free-tier usage — and the author did not 
have access to a credit/debit card or bank account at the time of 
submission.

The backend and ADK agent were fully tested and verified working locally 
(see demo video). All code is Cloud Run-ready; deployment requires only 
running the command in Step 6 once a billing account is linked.

---
## 📄 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.
