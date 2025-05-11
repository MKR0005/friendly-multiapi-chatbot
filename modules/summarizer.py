import requests
from typing import Any, Dict
import os

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.endpoint = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"  # Example model

    def summarize(self, text: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": text,
            "parameters": {"min_length": 30, "max_length": 150}
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            summary = response.json()[0]['summary_text']
            return summary
        except Exception as e:
            print(f"Error in summarizer: {e}")
            return "Error in summarization"

