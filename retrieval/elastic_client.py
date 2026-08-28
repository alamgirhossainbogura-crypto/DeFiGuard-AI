import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()


class ElasticSearchClient:
    """
    Handles retrieval of known vulnerability patterns and exploit
    signatures from Elasticsearch to augment the AI audit context.
    """

    def __init__(self):
        # Fixed: reads the same env var names documented in .env.example
        # and README (previously read a nonexistent ELASTICSEARCH_URL var,
        # so it silently always fell back to localhost).
        self.es_endpoint = os.getenv("ELASTIC_ENDPOINT")
        self.es_api_key = os.getenv("ELASTIC_API_KEY")

        self.client = None
        if self.es_endpoint:
            try:
                self.client = Elasticsearch(
                    self.es_endpoint,
                    api_key=self.es_api_key,
                )
            except Exception as e:
                print(f"Warning: Elasticsearch connection failed: {str(e)}")
        else:
            print("Warning: ELASTIC_ENDPOINT not set - vulnerability retrieval will use fallback data.")

    def search_vulnerabilities(self, query: str, size: int = 3) -> list:
        """
        Performs a text search for similar smart contract vulnerability patterns.
        Falls back to clearly-labeled mock data if Elasticsearch is unreachable,
        so the caller/UI can distinguish real matches from fallback ones.
        """
        if not self.client or not self.client.ping():
            return [
                {
                    "id": "VULN-001",
                    "title": "Standard Reentrancy in withdraw()",
                    "severity": "High",
                    "source": "mock_fallback",
                },
                {
                    "id": "VULN-002",
                    "title": "Unchecked Low-Level Call Return",
                    "severity": "Medium",
                    "source": "mock_fallback",
                },
            ]

        index_name = "defiguard_vulnerabilities"
        try:
            body = {
                "query": {"match": {"description": query}},
                "size": size,
            }
            response = self.client.search(index=index_name, body=body)
            hits = response.get("hits", {}).get("hits", [])
            return [{**hit["_source"], "source": "elasticsearch"} for hit in hits]
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []
