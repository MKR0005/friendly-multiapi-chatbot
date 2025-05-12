from agents.base_agent import BaseAgent
from agents.summarizer import Summarizer
from agents.reasoning import Reasoning
from services.api_service import APIService
from utils.logger import Logger

class AgentManager:
    def __init__(self, api_key=None):
        self.logger = Logger()
        self.api_key = api_key
        self.agents = {}
        self.api_service = APIService()  # Dynamically handle APIs
        self._load_agents()

    def _load_agents(self):
        self._register_agent("summarize", Summarizer(self.api_key), ["summarize", "summary"])
        self._register_agent("reasoning", Reasoning(self.api_key), ["why", "because", "explain"])
        # You can dynamically add more agents here in the future

    def _register_agent(self, name: str, agent: BaseAgent, keywords: list):
        """
        Register agents dynamically by name, agent instance, and associated keywords.
        """
        self.agents[name] = {
            "instance": agent,
            "keywords": keywords,
        }

    def _route_to_agents(self, text: str) -> list:
        """
        Match user input text to the appropriate agents based on keywords.
        Returns a list of matched agent instances.
        """
        matched = []
        for name, data in self.agents.items():
            if any(keyword.lower() in text.lower() for keyword in data["keywords"]):
                matched.append(data["instance"])
        return matched

    def process_request(self, text: str, api_name: str = None, endpoint: str = None, params: dict = None) -> dict:
        """
        Process user input text and route it to the appropriate agents or APIs for action.
        """
        try:
            selected_agents = self._route_to_agents(text)
            if not selected_agents:
                # If no agent found, check if the request needs API handling
                if api_name:
                    api_data = self.api_service.fetch_data(api_name, endpoint, params)
                    return {"api_data": api_data}
                return {"error": "No suitable agent found for the input."}

            responses = {}
            for agent in selected_agents:
                # Handle different agent methods dynamically
                if hasattr(agent, "summarize"):
                    responses["summarize"] = agent.summarize(text)
                elif hasattr(agent, "reason"):
                    responses["reasoning"] = agent.reason(text, text)
                else:
                    responses["error"] = f"{agent.__class__.__name__} method not found"

            return responses

        except Exception as e:
            self.logger.log_error(f"Error in AgentManager: {e}")
            return {"error": str(e)}
