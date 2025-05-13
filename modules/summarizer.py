import torch
import os
from services.api_service import APIService
from agents.agent_manager import AgentManager
from services.rag_service import RAGService
from transformers import pipeline
from config import Config  # Import Config class from config module
from dotenv import load_dotenv
from summarizer import Summarizer  # Assuming you have this module for summarization
from reasoning import Reasoning  # Assuming you have this module for reasoning

# Load environment variables
load_dotenv()

class Config:
    # Load API keys from environment variables
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    HUGGINGFACE_API_KEY1 = os.getenv("HUGGINGFACE_API_KEY1")
    HUGGINGFACE_API_KEY2 = os.getenv("HUGGINGFACE_API_KEY2")

def main():
    # Initialize services with API keys
    api_service = APIService()
    agent_manager = AgentManager()
    rag_service = RAGService()

    # Example user query
    user_input = input("Enter your query: ").strip()

    # Summarize and Reasoning with Huggingface keys
    summary_reason_response = summarize_and_reason(user_input)

    if summary_reason_response:
        print("Summary and Reasoning Response:", summary_reason_response)
    else:
        # Determine API based on query
        api_name = get_api_name_from_query(user_input)

        if api_name:
            api_info = Config.API_CONFIG.get(api_name)
            if api_info:
                endpoint = api_info.get('base_url')
                api_data = api_service.fetch_data(api_name, endpoint)
                if api_data:
                    # Process with agents
                    response = agent_manager.process_request(user_input)
                    print("Agent Response:", response)

                    # Process with RAG
                    rag_response = rag_service.process(user_input, api_data)
                    print("RAG Response:", rag_response)
                else:
                    print(f"No data found for {api_name}")
            else:
                print(f"No config found for {api_name}")
        else:
            print("No relevant API found. Falling back to chatbot mode...")
            fallback_response = fallback_chatbot(user_input)
            print("Chatbot Response:", fallback_response)


def get_api_name_from_query(query: str) -> str:
    keywords = {
        'news': 'news_api',
        'weather': 'weather_api',
        'crypto': 'crypto_api',
        'sports': 'sports_api',
        'stocks': 'stocks_api',
        'finance': 'finance_api',
        'health': 'health_api',
        'education': 'education_api',
        'travel': 'travel_api',
        'books': 'books_api',
        'music': 'music_api',
        'traffic': 'traffic_api',
        'shopping': 'shopping_api',
        'jobs': 'jobs_api',
        'events': 'events_api',
        'trends': 'trends_api',
        'transport': 'transport_api',
    }
    for keyword, api_name in keywords.items():
        if keyword in query.lower():
            return api_name
    return None

def summarize_and_reason(query: str):
    # Check if the query should be passed through summarizer or reasoning
    if "summarize" in query.lower():
        print("Using Summarizer API...")
        return summarize(query)
    elif "reason" in query.lower():
        print("Using Reasoning API...")
        return reason(query)
    else:
        return None

def summarize(query: str):
    # Use HUGGINGFACE_API_KEY1 for summarization
    api_key = Config.HUGGINGFACE_API_KEY1
    try:
        summarizer = Summarizer(api_key)
        summary = summarizer.summarize(query)
        return summary
    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        return None

def reason(query: str):
    # Use HUGGINGFACE_API_KEY2 for reasoning
    api_key = Config.HUGGINGFACE_API_KEY2
    try:
        reasoning = Reasoning(api_key)
        reasoning_result = reasoning.reason(query)
        return reasoning_result
    except Exception as e:
        print(f"Error during reasoning: {str(e)}")
        return None

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
