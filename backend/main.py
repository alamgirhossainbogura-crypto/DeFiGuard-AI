import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agent_runtime.runner import run_scan

load_dotenv()

app = FastAPI(
    title="DeFiGuard AI API",
    description="Autonomous Smart Contract & DeFi Risk Intelligence Platform",
    version="2.0.0",
)

# CORS: explicit origins from env, no wildcard - fixes the open-CORS issue
# from v1. ALLOWED_ORIGINS is a comma-separated list, e.g.
# "http://localhost:8501,https://your-frontend.run.app"
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

MAX_CONTRACT_CODE_LENGTH = 50_000  # guard against oversized payloads driving up Gemini cost


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
    Triggers the autonomous ADK agent pipeline, which combines Gemini
    code reasoning with Elasticsearch historical pattern retrieval.
    The agent itself decides when to call the retrieval tool.
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

    # New user/session id per scan - stateless from the API's point of view.
    session_id = str(uuid.uuid4())

    try:
        analysis_text = await run_scan(
            user_id="api_user",
            session_id=session_id,
            prompt=prompt,
        )
        return {
            "status": "success",
            "contract_name": request.contract_name,
            "chain_type": request.chain_type,
            "ai_analysis": analysis_text,
        }
    except HTTPException:
        raise
    except Exception:
        # Never leak raw exception text to the client - log server-side instead.
        # Wire this up to real logging (e.g. Cloud Logging) before deployment.
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the smart contract scan.",
        )


if __name__ == "__main__":
    import uvicorn

    reload_enabled = os.getenv("ENV", "development") == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload_enabled)
