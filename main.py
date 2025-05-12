from config import Config
from services.api_service import APIService
from agents.agent_manager import AgentManager
from services.rag_service import RAGService

def main():
    # Initialize
    api_key = Config.HUGGINGFACE_API_KEY
    api_service = APIService()
    agent_manager = AgentManager(api_key)
    rag_service = RAGService()

    # Example input
    user_input = "Tell me the latest news in technology."
    api_name = "news_api"
    endpoint = "latest-news"
    params = {"category": "technology", "apiKey": Config.NEWS_API_KEY}

    # Fetch data from a specific API
    api_data = api_service.fetch_data(api_name, endpoint, params)

    # Process the data with agents
    response = agent_manager.process_request(user_input)
    print("Response from Agents:", response)

    # Process with RAG
    rag_response = rag_service.process_data(user_input, api_data)
    print("RAG Response:", rag_response)

if __name__ == "__main__":
    main()
