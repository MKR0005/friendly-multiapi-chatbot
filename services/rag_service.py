from typing import List, Dict

class RAGService:
    def __init__(self):
        pass

    def retrieve(self, query: str, api_responses: List[Dict]) -> List[Dict]:
        """
        Simulates retrieval process by filtering API responses based on query.
        """
        relevant_responses = []
        for response in api_responses:
            if query.lower() in response.get("data", "").lower():
                relevant_responses.append(response)
        return relevant_responses

    def aggregate(self, relevant_responses: List[Dict]) -> str:
        """
        Aggregates the relevant responses into a single response string.
        """
        aggregated_response = "\n".join([resp.get("data", "") for resp in relevant_responses])
        return aggregated_response

    def process(self, query: str, api_responses: List[Dict]) -> str:
        """
        Full RAG processing pipeline: retrieve and aggregate.
        """
        relevant_responses = self.retrieve(query, api_responses)
        aggregated_response = self.aggregate(relevant_responses)
        return aggregated_response
