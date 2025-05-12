from typing import List, Dict
from modules.summarizer import Summarizer
from modules.reasoning import Reasoning
from config import Config

class RAGService:
    def __init__(self):
        # Access the summarizer API configuration
        summarizer_config = Config.API_CONFIG.get("summarizer_api_key")
        if not summarizer_config:
            raise ValueError("Summarizer API configuration not found.")
        
        api_key = summarizer_config["headers"]["Authorization"].replace("Bearer ", "")
        self.summarizer = Summarizer(api_key)

    def retrieve(self, query: str, api_responses: List[Dict]) -> List[Dict]:
        relevant_responses = []
        for response in api_responses:
            if query.lower() in response.get("data", "").lower():
                relevant_responses.append(response)
        return relevant_responses

    def aggregate(self, relevant_responses: List[Dict]) -> str:
        aggregated_response = "\n".join([resp.get("data", "") for resp in relevant_responses])
        return aggregated_response
    def process(self, query: str, api_responses: List[Dict]) -> str:
        try:
            relevant_responses = self.retrieve(query, api_responses)
            if not relevant_responses:
                return "No relevant information found to answer your query."

            aggregated_response = self.aggregate(relevant_responses)
            if not aggregated_response.strip():
                return "Relevant information was empty or could not be aggregated."

            summarized_content = self.summarizer.summarize(aggregated_response)
            if not summarized_content.strip():
                return "Summarization resulted in empty content."

            final_response = self.reasoning.reason(query, summarized_content)
            return final_response

        except Exception as e:
            return f"An error occurred while processing the request: {str(e)}"
