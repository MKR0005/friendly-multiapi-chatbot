from typing import List, Dict
from agents.summarizer import Summarizer
from agents.reasoning import Reasoning

class RAGService:
    def __init__(self, api_key: str):
        self.summarizer = Summarizer(api_key)
        self.reasoning = Reasoning(api_key)

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
        Full RAG processing pipeline: retrieve, aggregate, summarize, and reason.
        """
        # Step 1: Retrieve relevant responses
        relevant_responses = self.retrieve(query, api_responses)

        # Step 2: Aggregate responses
        aggregated_response = self.aggregate(relevant_responses)

        # Step 3: Summarize the aggregated content
        summarized_content = self.summarizer.summarize(aggregated_response)

        # Step 4: Apply reasoning
        final_response = self.reasoning.reason(summarized_content)

        return final_response
