import torch
import os
from services.api_service import APIService
from agents.agent_manager import AgentManager
from services.rag_service import RAGService
from transformers import pipeline
from config import Config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Initialize services
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
        print("No relevant API found.")
        
        # Attempt summarize and reason
        summary_reason_response = summarize_and_reason(user_input)
        if summary_reason_response:
            print("Summary/Reason Response:", summary_reason_response)
        else:
            # Fallback to chatbot mode
            fallback_response = fallback_chatbot(user_input)
            print("Fallback Chatbot Response:", fallback_response)


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


def get_model_pipeline(api_keys):
    """ Initialize the shared model pipeline. """
    for key in api_keys:
        if key:
            try:
                return pipeline(
                    "text2text-generation",
                    model="google/flan-t5-large",
                    token=key,
                    device="cuda" if torch.cuda.is_available() else "cpu"
                )
            except Exception as e:
                print(f"Model Initialization Error: {e}")
                continue
    return None


def summarize_and_reason(query: str) -> str:
    api_keys = [Config.HUGGINGFACE_API_KEY, Config.HUGGINGFACE_API_KEY1, Config.HUGGINGFACE_API_KEY2]
    model_pipeline = get_model_pipeline(api_keys)

    if not model_pipeline:
        return None

    try:
        # Summarize
        summary_prompt = f"Summarize this: {query}"
        summary_response = model_pipeline(summary_prompt, max_length=100, do_sample=True, temperature=0.7)
        summary_text = summary_response[0]['generated_text'].strip()

        # Reason
        reason_prompt = f"Analyze and reason about: {summary_text}"
        reasoning_response = model_pipeline(reason_prompt, max_length=100, do_sample=True, temperature=0.7)
        reasoning_text = reasoning_response[0]['generated_text'].strip()

        return f"Summary: {summary_text}\nReasoning: {reasoning_text}"

    except Exception as e:
        print(f"Summarize/Reason Error: {e}")
        return None


def fallback_chatbot(query: str) -> str:
    api_keys = [Config.HUGGINGFACE_API_KEY, Config.HUGGINGFACE_API_KEY1, Config.HUGGINGFACE_API_KEY2]
    model_pipeline = get_model_pipeline(api_keys)

    if not model_pipeline:
        return "I'm unable to process your request at the moment. Please try again later."

    try:
        response = model_pipeline(query, max_length=100, do_sample=True, temperature=0.7)
        return response[0]['generated_text'].strip()

    except Exception as e:
        print(f"Fallback Chatbot Error: {e}")
        return "I'm unable to process your request at the moment. Please try again later."


if __name__ == "__main__":
    main()
