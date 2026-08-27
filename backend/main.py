import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="DeFiGuard AI API",
    description="Autonomous Smart Contract & DeFi Risk Intelligence Platform",
    version="1.0.0"
)

# Enable CORS for frontend integration (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    contract_code: str = Field(..., description="The raw smart contract code (Solidity/Rust)")
    contract_name: str = Field(..., description="Name of the smart contract")
    chain_type: str = Field(default="solidity", description="Blockchain type/language")

@app.get("/")
def read_root():
    """Health check endpoint to verify API status."""
    return {"status": "online", "system": "DeFiGuard AI Agent Pipeline Active"}

@app.post("/run-scan")
def run_contract_scan(request: ScanRequest):
    """
    Triggers the autonomous multi-agent security pipeline 
    to scan smart contract code for vulnerabilities.
    """
    # Input validation check
    if not request.contract_code.strip():
        raise HTTPException(status_code=400, detail="Smart contract code cannot be empty or whitespace.")
    
    # TODO: Integrate ScanOrchestrator here to process real AI analysis
    # Currently returning a structured mock response for pipeline testing
    return {
        "status": "success",
        "contract_name": request.contract_name,
        "trust_score": "B+",
        "vulnerabilities_found": 2,
        "details": [
            {"type": "Reentrancy Risk", "severity": "High", "line": 42},
            {"type": "Unchecked Return Value", "severity": "Medium", "line": 88}
        ],
        "patch_generated": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
