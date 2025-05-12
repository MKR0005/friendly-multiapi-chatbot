from typing import List, Dict
from agents.summarizer import Summarizer
from agents.reasoning import Reasoning
from config import Config

class RAGService:
    def __init__(self):
        # Initialize with respective API keys for summarizer, reasoning, and fallback models
        self.summarizer = Summarizer(Config.HUGGINGFACE_API_KEY)  # Summarizer uses HUGGINGFACE_API_KEY
        self.reasoning = Reasoning(Config.HUGGINGFACE_API_KEY1)   # Reasoning uses HUGGINGFACE_API_KEY1

    def retrieve(self, query: str, api_responses: List[Dict]) -> List[Dict]:
        """
        Retrieve relevant responses from the API responses based on the query.
        """
        relevant_responses = []
        for response in api_responses:
            data = response.get("data", "")
            if isinstance(data, str) and query.lower() in data.lower():
                relevant_responses.append(response)
        return relevant_responses

    def aggregate(self, relevant_responses: List[Dict]) -> str:
        """
        Aggregate the relevant responses into a single string.
        """
        return "\n".join([resp.get("data", "") for resp in relevant_responses if isinstance(resp.get("data", ""), str)])

    def process(self, query: str, api_responses: List[Dict]) -> str:
        """
        Process the query by retrieving relevant data, aggregating it,
        summarizing it, and reasoning based on the summary.
        """
        try:
            # Step 1: Retrieve relevant responses based on the query
            relevant_responses = self.retrieve(query, api_responses)

            if not relevant_responses:
                return "No relevant information found to answer your query."

            # Step 2: Aggregate the relevant responses
            aggregated_response = self.aggregate(relevant_responses)

            if not aggregated_response.strip():
                return "Relevant information was empty or could not be aggregated."

            # Step 3: Summarize the aggregated content using the Summarizer
            summarized_content = self.summarizer.summarize(aggregated_response)

            if not summarized_content.strip():
                return "Summarization resulted in empty content."

            # Step 4: Reason based on the summarized content using the Reasoning model
            final_response = self.reasoning.reason(query, summarized_content)

            return final_response

        except Exception as e:
            # Catch any unexpected errors and log them
            return f"An error occurred while processing the request: {str(e)}"
