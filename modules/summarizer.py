import os
import requests
from typing import Any, Dict
from utils.logger import Logger

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"  # Example summarization model
        self.logger = Logger()

    def summarize(self, content: str) -> str:
        if not self.api_key:
            self.logger.log_error("Missing Hugging Face API key.")
            return "API key missing"

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": content,
            "parameters": {"min_length": 30, "max_length": 150}
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]
            else:
                self.logger.log_warning("Unexpected response format from summarization model.")
                return "Unexpected response format"
        except Exception as e:
            self.logger.log_error(f"Error in summarization: {e}")
            return "Error in summarization"
