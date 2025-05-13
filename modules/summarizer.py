# modules/summarizer.py
import os
import requests
from utils.logger import Logger

class Summarizer:
    def __init__(self, api_key=None, model_name="mistralai/Mistral-7B-Instruct-v0.3"):
        """
        Initializes the Summarizer class with the API key and model name.

        Args:
        - api_key (str, optional): API key for Hugging Face.
        - model_name (str): The name of the Hugging Face model to use for summarization.
        """
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY1")  # Update to HUGGINGFACE_API_KEY1
        self.model_name = model_name
        self.endpoint = f"https://api-inference.huggingface.co/models/{self.model_name}"
        self.logger = Logger()

    def summarize(self, content: str, min_length: int = 30, max_length: int = 150) -> str:
        """
        Summarizes the given content using the Hugging Face model.

        Args:
        - content (str): The content to summarize.
        - min_length (int): The minimum length of the summary.
        - max_length (int): The maximum length of the summary.

        Returns:
        - str: The generated summary.
        """
        if not self.api_key:
            self.logger.log_error("Missing Hugging Face API key.")
            return "API key missing"

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "inputs": content,
            "parameters": {"min_length": min_length, "max_length": max_length}
        }

        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Check if the response format is as expected
            if isinstance(result, list) and "summary_text" in result[0]:
                return result[0]["summary_text"]
            else:
                self.logger.log_warning("Unexpected response format.")
                return "Unexpected response format"
        except requests.RequestException as e:
            self.logger.log_error(f"Request error in summarization: {e}")
            return "Request error"
        except Exception as e:
            self.logger.log_error(f"Error in summarization: {e}")
            return "Error in summarization"

