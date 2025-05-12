from typing import List, Dict
from modules.summarizer import Summarizer
from modules.reasoning import Reasoning
from config import Config

class RAGService:
    def __init__(self):
        """
        Initialize with respective API keys for summarizer, reasoning, and fallback models
        using the API keys defined in the Config class.
        """
        # Summarizer uses HUGGINGFACE_API_KEY
        self.summarizer = Summarizer(Config.HUGGINGFACE_API_KEY)
        # Reasoning uses HUGGINGFACE_API_KEY1
        self.reasoning = Reasoning(Config.HUGGINGFACE_API_KEY1)

    def retrieve(self, query: str, api_responses: List[Dict]) -> List[Dict]:
        relevant_responses = []
        for response in api_responses:
            data = response.get("data", "")
            if isinstance(data, str) and query.lower() in data.lower():
                relevant_responses.append(response)
        return relevant_responses

    def aggregate(self, relevant_responses: List[Dict]) -> str:
        return "\n".join([resp.get("data", "") for resp in relevant_responses if isinstance(resp.get("data", ""), str)])

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
