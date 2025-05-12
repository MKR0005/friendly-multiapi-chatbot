from typing import List, Dict
from agents.summarizer import Summarizer
from agents.reasoning import Reasoning
# from utils.logger import Logger  # Uncomment if you want to log
# logger = Logger()

class RAGService:
    def __init__(self, api_key: str):
        self.summarizer = Summarizer(api_key)
        self.reasoning = Reasoning(api_key)

    def retrieve(self, query: str, api_responses: List[Dict]) -> List[Dict]:
        """
        Filters API responses based on query relevance.
        """
        relevant_responses = []
        for response in api_responses:
            data = response.get("data", "")
            if isinstance(data, str) and query.lower() in data.lower():
                relevant_responses.append(response)
        return relevant_responses

    def aggregate(self, relevant_responses: List[Dict]) -> str:
        """
        Joins all relevant data fields into a single string.
        """
        return "\n".join([resp.get("data", "") for resp in relevant_responses if isinstance(resp.get("data", ""), str)])

    def process(self, query: str, api_responses: List[Dict]) -> str:
        """
        Full RAG pipeline: retrieve → aggregate → summarize → reason.
        """
        relevant_responses = self.retrieve(query, api_responses)
        
        if not relevant_responses:
            return "No relevant information found to answer your query."

        aggregated_response = self.aggregate(relevant_responses)

        if not aggregated_response.strip():
            return "Relevant information was empty or could not be aggregated."

        summarized_content = self.summarizer.summarize(aggregated_response)
        final_response = self.reasoning.reason(summarized_content)

        return final_response
