import os
from dotenv import load_dotenv
from google.adk.agents import Agent

from retrieval.elastic_client import ElasticSearchClient

load_dotenv()

# Single shared client instance - reused across requests, not recreated per-call
es_client = ElasticSearchClient()


def search_known_vulnerabilities(contract_name: str) -> dict:
    """Searches the historical exploit database for known vulnerability
    patterns that match this contract's name or description.

    Args:
        contract_name: The name of the smart contract being audited.

    Returns:
        A dict with a status and a list of matched historical patterns.
    """
    results = es_client.search_vulnerabilities(query=contract_name, size=3)
    return {"status": "success", "matches": results}


# NOTE: verify this model id against the current Vertex AI / Google AI Studio
# console before submission - Google renames/rotates these periodically.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

root_agent = Agent(
    model=GEMINI_MODEL,
    name="defiguard_audit_agent",
    description=(
        "Autonomous security auditor for DeFi smart contracts. "
        "Combines historical exploit retrieval with deep code reasoning."
    ),
    instruction="""You are an elite autonomous DeFi and Smart Contract security auditor.

    When given smart contract code and a contract name:
    1. Call search_known_vulnerabilities with the contract name to check for
       matching historical exploit patterns before forming your judgment.
    2. Perform a rigorous security audit covering: reentrancy risks, integer
       overflows/underflows, access control flaws, unchecked return values,
       and financial exploit vectors.
    3. Return a structured report containing:
       - An overall Trust Score (A, B+, C, etc.)
       - A list of vulnerabilities with severity levels and approximate line numbers
       - Actionable remediation or patch recommendations

    Ground your findings in the actual code provided - do not invent line
    numbers or vulnerabilities that are not present in the code.""",
    tools=[search_known_vulnerabilities],
)
