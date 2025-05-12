from services.api_service import APIService
from agents.agent_manager import AgentManager
from services.rag_service import RAGService
from transformers import pipeline
from config import Config

def main():
    # Initialize with Hugging Face API Key
    api_key = Config.HUGGINGFACE_API_KEY2
    api_service = APIService()
    agent_manager = AgentManager(api_key)  # Pass the same API key
    rag_service = RAGService(api_key)  # Pass the same API key

    # Example user query
    user_input = input("Enter your query: ").strip()

    # Automatically determine the correct API based on the user's query
    api_name = get_api_name_from_query(user_input)
    if not api_name:
        print("No appropriate API found for your query.")
        return

    # Get the API details from the config
    api_info = Config.API_CONFIG[api_name]
    endpoint = api_info.get('endpoint', '')  # Modify as per your need

    # Fetch data from the selected API
    api_data = api_service.fetch_data(api_name, endpoint)
    if not api_data:
        print(f"Error fetching data from {api_name}, falling back to chatbot mode...")
        chatbot_response = fallback_chatbot(user_input, api_key)
        print("Chatbot Response:", chatbot_response)
        return

    # Process the data with agents
    response = agent_manager.process_request(user_input)
    print("Response from Agents:", response)

    # Process with RAG
    rag_response = rag_service.process(user_input, api_data)
    print("RAG Response:", rag_response)

def get_api_name_from_query(query: str) -> str:
    """
    Dynamically determines the correct API to call based on the query.
    """
    api_keywords = {
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

    query_lower = query.lower()

    # Check which API the query relates to based on keywords
    for keyword, api_name in api_keywords.items():
        if keyword in query_lower:
            return api_name

    return None  # Return None if no relevant API found

def fallback_chatbot(query: str, api_key: str) -> str:
    """
    A simple fallback to a conversational chatbot if no API data is available.
    Uses Hugging Face's T5 model for generating conversational responses.
    """
    chatbot = pipeline("text2text-generation", model="google/flan-t5-large", tokenizer="google/flan-t5-large", use_auth_token=api_key)
    response = chatbot(query, max_length=50, num_return_sequences=1)
    return response[0]['generated_text'].strip()

if __name__ == "__main__":
    main()
