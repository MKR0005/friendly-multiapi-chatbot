import os
import torch
from services.api_service import APIService
from agents.agent_manager import AgentManager
from services.rag_service import RAGService
from transformers import pipeline
from config import Config  # Import Config class from config module
from dotenv import load_dotenv
from modules.summarizer import Summarizer  # Import the Summarizer class
from modules.reasoning import Reasoning  # Import the Reasoning class

# Load environment variables
load_dotenv()

def main():
    # Initialize services with API keys
    api_service = APIService()
    agent_manager = AgentManager()
    rag_service = RAGService()

    # Example user query
    user_input = input("Enter your query: ").strip()

    # Initialize Summarizer and Reasoning agents
    summarizer = Summarizer(api_key=Config.API_CONFIG["summarizer_api_key"]["headers"]["Authorization"])
  # Use HUGGINGFACE_API_KEY1 for summarization
    reasoning_api_key = Config.API_CONFIG["reasoning_api_key"]["headers"]["Authorization"]
  # Use HUGGINGFACE_API_KEY for reasoning

    # First, try to summarize or reason based on the query before falling back to chatbot
    summary_response = summarize_and_reason(user_input, summarizer, reasoning)
    if summary_response:
        print("Summarize and Reason Response:", summary_response)
    else:
        print("No relevant API found. Falling back to chatbot mode...")
        fallback_response = fallback_chatbot(user_input)
        print("Chatbot Response:", fallback_response)


def summarize_and_reason(query: str, summarizer: Summarizer, reasoning: Reasoning) -> str:
    # Check if the query requires summarization or reasoning
    if 'summarize' in query.lower():
        return summarizer.summarize(query)
    elif 'reason' in query.lower():
        # Assuming the context is provided for reasoning, pass it here
        context = "Sample context for reasoning"  # Example context
        return reasoning.reason(query, context)
    return None  # No action taken if not a summarization or reasoning query


def fallback_chatbot(query: str) -> str:
    api_keys = [Config.HUGGINGFACE_API_KEY, Config.HUGGINGFACE_API_KEY1, Config.HUGGINGFACE_API_KEY2]

    for key in api_keys:
        if key:
            try:
                # Updated pipeline initialization without use_auth_token
                chatbot = pipeline(
                    "text2text-generation", 
                    model="google/flan-t5-large",
                    token=key,  # Use token parameter instead
                    device="cuda" if torch.cuda.is_available() else "cpu"
                )

                response = chatbot(
                    query,
                    max_length=100,
                    do_sample=True,  # Enable sampling for varied responses
                    temperature=0.7,  # Controls randomness
                    repetition_penalty=1.2,  # Prevent repetitive responses
                    num_beams=4  # Better quality through beam search
                )

                # Add post-processing
                clean_response = response[0]['generated_text'].strip()
                return clean_response.replace("  ", " ")  # Fix double spaces

            except Exception as e:
                print(f"Chatbot error with API key: {str(e)}")
                continue

    return "I'm unable to process your request at the moment. Please try again later."


if __name__ == "__main__":
    main()
