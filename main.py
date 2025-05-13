import torch
import os
from services.api_service import APIService
from agents.agent_manager import AgentManager
from services.rag_service import RAGService
from transformers import pipeline
from config import Config  # Import Config class from config module
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Load API keys from environment variables
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    HUGGINGFACE_API_KEY1 = os.getenv("HUGGINGFACE_API_KEY1")
    HUGGINGFACE_API_KEY2 = os.getenv("HUGGINGFACE_API_KEY2")

    # Define API configurations
    API_CONFIG = {
        'news_api': {'base_url': 'https://api.news.com/v1', 'headers': {}},
        'weather_api': {'base_url': 'https://api.weather.com/v1', 'headers': {}},
        'crypto_api': {'base_url': 'https://api.crypto.com/v1', 'headers': {}},
        'sports_api': {'base_url': 'https://api.sports.com/v1', 'headers': {}},
        'stocks_api': {'base_url': 'https://api.stocks.com/v1', 'headers': {}},
        'finance_api': {'base_url': 'https://api.finance.com/v1', 'headers': {}},
        'health_api': {'base_url': 'https://api.health.com/v1', 'headers': {}},
        'education_api': {'base_url': 'https://api.education.com/v1', 'headers': {}},
        'travel_api': {'base_url': 'https://api.travel.com/v1', 'headers': {}},
        'books_api': {'base_url': 'https://api.books.com/v1', 'headers': {}},
        'music_api': {'base_url': 'https://api.music.com/v1', 'headers': {}},
        'traffic_api': {'base_url': 'https://api.traffic.com/v1', 'headers': {}},
        'shopping_api': {'base_url': 'https://api.shopping.com/v1', 'headers': {}},
        'jobs_api': {'base_url': 'https://api.jobs.com/v1', 'headers': {}},
        'events_api': {'base_url': 'https://api.events.com/v1', 'headers': {}},
        'trends_api': {'base_url': 'https://api.trends.com/v1', 'headers': {}},
        'transport_api': {'base_url': 'https://api.transport.com/v1', 'headers': {}},
    }

def main():
    # Initialize services with API keys
    api_service = APIService()
    agent_manager = AgentManager()
    rag_service = RAGService()

    # Example user query
    user_input = input("Enter your query: ").strip()

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
