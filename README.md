# 🛡️ DeFiGuard AI

> **Autonomous Smart Contract & DeFi Risk Intelligence Platform** powered by Google Gemini, Elasticsearch, and FastAPI.

---

## 🌟 Overview

DeFiGuard-AI is an autonomous multi-agent security platform engineered to inspect, reason about, and patch vulnerabilities in smart contracts (Solidity/Rust) before deployment. By combining deep-code reasoning from **Google Gemini 1.5 Pro** with hybrid historical threat retrieval via **Elasticsearch**, DeFiGuard-AI acts as an elite virtual security auditor for decentralized finance.

🔗 **GitHub Repository:** [alamgirhossainbogura-crypto/DeFiGuard-AI](https://github.com/alamgirhossainbogura-crypto/DeFiGuard-AI)

---

## 🚀 Key Features

* **Multi-Agent AI Reasoning:** Utilizes Google Gemini 1.5 Pro to analyze complex control flows, access control flaws, reentrancy vulnerabilities, and exploit vectors.
* **Hybrid Threat Retrieval:** Integrates Elasticsearch to match smart contract names/patterns against known historical exploit signatures.
* **High-Performance Backend:** Built with FastAPI, featuring robust CORS middleware, automated input sanitization, and strict exception handling.
* **Interactive Frontend:** Powered by Streamlit, offering a modern cyber/DeFi dark-themed UI for seamless scanning and result visualization.

---

## 🏗️ Architecture & Project Structure

text
DeFiGuard-AI/
│
├── agent_runtime/
│   └── orchestrator.py        # Autonomous Gemini AI auditing orchestrator
│
├── backend/
│   └── main.py                # FastAPI server & API endpoint routing
│
├── frontend/
│   └── app.py                 # Streamlit web dashboard interface
│
├── retrieval/
│   └── elastic_client.py      # Elasticsearch historical threat retriever
│
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── LICENSE                    # Apache 2.0 License
├── README.md                  # Project Documentation
└── requirements.txt           # Python dependencies
---

## ⚙️ Tech Stack
​AI & LLM: Google Gemini 1.5 Pro (google-generativeai)
​Backend: FastAPI, Uvicorn, Pydantic, Python-Dotenv
​Database & Retrieval: Elasticsearch
​Frontend: Streamlit, Requests

## ​🚀 Getting Started & Local Setup

​1.  Clone the Repository 
git clone [https://github.com/alamgirhossainbogura-crypto/DeFiGuard-AI.git](https://github.com/alamgirhossainbogura-crypto/DeFiGuard-AI.git)
cd DeFiGuard-AI

2. Install Dependencies
pip install -r requirements.txt

3. Configure Environment Variables
​Create a .env file in the root directory based on .env.example and add your API keys:
GEMINI_API_KEY=your_google_gemini_api_key_here
ELASTIC_ENDPOINT=your_elasticsearch_endpoint_here
ELASTIC_API_KEY=your_elasticsearch_api_key_here
4. Run the Backend Server
    cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

5. Launch the Frontend Dashboard
​Open a new terminal window, navigate to the project root, and run:
streamlit run frontend/app.py
---
## 📄 License
​Distributed under the Apache 2.0 License. See LICENSE for more information.
