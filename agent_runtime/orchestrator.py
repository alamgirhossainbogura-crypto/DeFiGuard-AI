import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ScanOrchestrator:
    """
    Orchestrates the multi-agent smart contract risk intelligence pipeline.
    Utilizes Google Gemini to inspect code, find vulnerabilities, and suggest patches.
    """
    def __init__(self):
        # Using Gemini 1.5 Pro for advanced code reasoning and deep context analysis
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def analyze_contract(self, code: str, chain_type: str) -> dict:
        """
        Sends the smart contract code to Gemini with a specialized security auditing prompt.
        Uses asynchronous generation to prevent blocking the FastAPI event loop.
        """
        # Input safety check
        if not code or not code.strip():
            return {
                "status": "error",
                "message": "Contract code cannot be empty."
            }

        prompt = f"""
        You are an elite autonomous DeFi and Smart Contract security auditor.
        Perform a rigorous security audit on the following {chain_type} smart contract code.
        Identify any reentrancy risks, integer overflows, access control flaws, unchecked return values,
        and potential financial exploit vectors.
        
        Smart Contract Code:
        {code}
        
        Provide your analysis in a structured, clean format including:
        1. Overall Trust Score (e.g., A, B+, C)
        2. List of vulnerabilities with severity levels and approximate lines
        3. Actionable remediation or patch recommendations
        """
        
        try:
            # Using generate_content_async for true non-blocking async execution
            response = await self.model.generate_content_async(prompt)
            return {
                "status": "success",
                "analysis": response.text
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
