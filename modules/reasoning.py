import requests
from typing import Any, Dict
import os

class Reasoning:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.endpoint = "https://api-inference.huggingface.co/models/google/flan-t5-large"  # Example model

    def reason(self, question: str, context: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": f"Question: {question}\nContext: {context}",
            "parameters": {"min_length": 30, "max_length": 150}
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            answer = response.json()[0]['generated_text']
            return answer
        except Exception as e:
            print(f"Error in reasoning: {e}")
            return "Error in reasoning"
