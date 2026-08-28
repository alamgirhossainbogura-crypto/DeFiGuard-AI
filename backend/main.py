import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agent_runtime.runner import run_scan
from retrieval.firestore_client import ScanHistoryClient

load_dotenv()

app = FastAPI(
    title="DeFiGuard AI API",
    description="Autonomous Smart Contract & DeFi Risk Intelligence Platform",
    version="2.1.0",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

history_client = ScanHistoryClient()

MAX_CONTRACT_CODE_LENGTH = 50_000


class ScanRequest(BaseModel):
    contract_code: str = Field(..., description="The raw smart contract code (Solidity/Rust)")
    contract_name: str = Field(..., description="Name of the smart contract")
    chain_type: str = Field(default="solidity", description="Blockchain type/language")


@app.get("/")
def read_root():
    """Health check endpoint to verify API status."""
    return {"status": "online", "system": "DeFiGuard AI Agent Pipeline Active"}


@app.post("/run-scan")
async def run_contract_scan(request: ScanRequest):
    """
    Triggers the autonomous ADK agent pipeline, then persists the result
    to Firestore for scan history.
    """
    if not request.contract_code.strip():
        raise HTTPException(status_code=400, detail="Smart contract code cannot be empty or whitespace.")

    if len(request.contract_code) > MAX_CONTRACT_CODE_LENGTH:
        raise HTTPException(status_code=413, detail="Smart contract code exceeds the maximum allowed size.")

    prompt = f"""Contract name: {request.contract_name}
Chain type: {request.chain_type}

Smart contract code:
{request.contract_code}
"""

    session_id = str(uuid.uuid4())

    try:
        analysis_text = await run_scan(
            user_id="api_user",
            session_id=session_id,
            prompt=prompt,
        )

        scan_id = await history_client.save_scan(
            contract_name=request.contract_name,
            chain_type=request.chain_type,
            ai_analysis=analysis_text,
        )

        return {
            "status": "success",
            "scan_id": scan_id,
            "contract_name": request.contract_name,
            "chain_type": request.chain_type,
            "ai_analysis": analysis_text,
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the smart contract scan.",
        )


@app.get("/scan-history")
async def get_scan_history(limit: int = 10):
    """Returns recent past scans from Firestore."""
    scans = await history_client.get_recent_scans(limit=limit)
    return {"status": "success", "scans": scans}


if __name__ == "__main__":
    import uvicorn

    reload_enabled = os.getenv("ENV", "development") == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload_enabled)
