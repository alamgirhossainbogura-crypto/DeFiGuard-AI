import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Import our custom modules
from agent_runtime.orchestrator import ScanOrchestrator
from retrieval.elastic_client import ElasticSearchClient

# Load environment variables
load_dotenv()

app = FastAPI(
    title="DeFiGuard AI API",
    description="Autonomous Smart Contract & DeFi Risk Intelligence Platform",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Note: Update specific origins for production deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Orchestrator and Elasticsearch client instances
orchestrator = ScanOrchestrator()
es_client = ElasticSearchClient()

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
    Triggers the autonomous multi-agent security pipeline 
    combining Gemini AI code reasoning and Elasticsearch pattern retrieval.
    """
    # Input validation check
    if not request.contract_code.strip():
        raise HTTPException(status_code=400, detail="Smart contract code cannot be empty or whitespace.")
    
    try:
        # Step 1: Fetch relevant historical vulnerability patterns from Elasticsearch
        similar_vulnerabilities = es_client.search_vulnerabilities(query=request.contract_name, size=3)

        # Step 2: Execute Gemini-powered deep smart contract security audit
        ai_audit_result = await orchestrator.analyze_contract(
            code=request.contract_code, 
            chain_type=request.chain_type
        )

        if ai_audit_result.get("status") == "error":
            raise HTTPException(status_code=500, detail=ai_audit_result.get("message"))

        # Step 3: Return integrated audit intelligence
        return {
            "status": "success",
            "contract_name": request.contract_name,
            "chain_type": request.chain_type,
            "retrieved_patterns": similar_vulnerabilities,
            "ai_analysis": ai_audit_result.get("analysis"),
            "patch_generated": True
        }

    except HTTPException as he:
        # Re-raise explicit HTTP exceptions without modification
        raise he
    except Exception:
        # Prevent internal stack traces or sensitive errors from leaking to the client
        raise HTTPException(status_code=500, detail="An internal error occurred while processing the smart contract scan.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
