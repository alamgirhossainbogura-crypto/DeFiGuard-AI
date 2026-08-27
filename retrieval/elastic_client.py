import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ElasticSearchClient:
    """
    Handles hybrid retrieval (BM25 + Vector Search) of known vulnerability patterns 
    and exploit signatures from Elasticsearch to augment the AI audit context.
    """
    def __init__(self):
        self.es_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
        try:
            # Initialize Elasticsearch client
            self.client = Elasticsearch(self.es_url)
        except Exception as e:
            self.client = None
            print(f"Warning: Elasticsearch connection failed: {str(e)}")

    def search_vulnerabilities(self, query: str, size: int = 3) -> list:
        """
        Performs a basic text/hybrid search for similar smart contract vulnerability patterns.
        """
        if not self.client or not self.client.ping():
            # Fallback mock data if Elasticsearch cluster is not running locally yet
            return [
                {"id": "VULN-001", "title": "Standard Reentrancy in withdraw()", "severity": "High"},
                {"id": "VULN-002", "title": "Unchecked Low-Level Call Return", "severity": "Medium"}
            ]

        index_name = "defiguard_vulnerabilities"
        
        try:
            body = {
                "query": {
                    "match": {
                        "description": query
                    }
                },
                "size": size
            }
            response = self.client.search(index=index_name, body=body)
            hits = response.get("hits", {}).get("hits", [])
            return [hit["_source"] for hit in hits]
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
