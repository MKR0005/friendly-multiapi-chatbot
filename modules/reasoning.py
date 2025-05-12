import os
import requests
from utils.logger import Logger

class Reasoning:
    def __init__(self, api_key=None, model_name="google/flan-t5-large"):
        """
        Initializes the Reasoning class with the API key and model name.
        
        Args:
        - api_key (str, optional): API key for Hugging Face.
        - model_name (str): The name of the Hugging Face model to use.
        """
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model_name = model_name
        self.endpoint = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.logger = Logger()

    def reason(self, question: str, context: str) -> str:
        """
        Given a question and context, generates a response using the Hugging Face model.
        
        Args:
        - question (str): The question to answer.
        - context (str): The context to help generate the answer.
        
        Returns:
        - str: The generated answer.
        """
        if not self.api_key:
            self.logger.log_error("Missing Hugging Face API key.")
            return "API key missing"

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": f"Question: {question}\nContext: {context}",
            "parameters": {"min_length": 30, "max_length": 150}
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Check if the response format is as expected
            if isinstance(result, list) and "generated_text" in result[0]:
                return result[0]["generated_text"]
            else:
                self.logger.log_warning("Unexpected response format from reasoning model.")
                return "Unexpected response format"
        except requests.RequestException as e:
            self.logger.log_error(f"Request error in reasoning: {e}")
            return "Request error"
        except Exception as e:
            self.logger.log_error(f"Error in reasoning: {e}")
            return "Error in reasoning"
