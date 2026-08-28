import os
import uuid
from datetime import datetime, timezone

from google.cloud import firestore


class ScanHistoryClient:
    """
    Persists smart contract scan results to Firestore, so past audits
    can be retrieved instead of recomputed. This is what gives the
    agent pipeline actual state across requests.
    """

    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.client = None
        if project_id:
            try:
                self.client = firestore.AsyncClient(project=project_id)
            except Exception as e:
                print(f"Warning: Firestore connection failed: {str(e)}")
        else:
            print("Warning: GOOGLE_CLOUD_PROJECT not set - scan history will not be persisted.")

    async def save_scan(self, contract_name: str, chain_type: str, ai_analysis: str) -> str:
        """Saves a completed scan result. Returns the new document id, or empty string if unavailable."""
        if not self.client:
            return ""

        scan_id = str(uuid.uuid4())
        try:
            doc_ref = self.client.collection("scans").document(scan_id)
            await doc_ref.set({
                "contract_name": contract_name,
                "chain_type": chain_type,
                "ai_analysis": ai_analysis,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            return scan_id
        except Exception as e:
            print(f"Firestore save error: {str(e)}")
            return ""

    async def get_recent_scans(self, limit: int = 10) -> list:
        """Returns the most recent scans, newest first."""
        if not self.client:
            return []

        try:
            query = (
                self.client.collection("scans")
                .order_by("created_at", direction=firestore.Query.DESCENDING)
                .limit(limit)
            )
            results = []
            async for doc in query.stream():
                data = doc.to_dict()
                data["id"] = doc.id
                results.append(data)
            return results
        except Exception as e:
            print(f"Firestore query error: {str(e)}")
            return []
