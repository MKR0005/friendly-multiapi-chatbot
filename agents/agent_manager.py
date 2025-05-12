from agents.base_agent import BaseAgent
from utils.logger import Logger

class AgentManager:
    def __init__(self):
        self.logger = Logger()
        self.agents = {}  # Dictionary to store agents by name/keywords
        self._load_agents()

    def _load_agents(self):
        """
        Dynamically load and register all available agents.
        You can add more here as needed.
        """
        from modules.summarizer import Summarizer
        from modules.reasoning import Reasoning
        from modules.weather import WeatherAgent
        from modules.stock import StockAgent
        # Add your own imports...

        # Register agents with routing keywords
        self._register_agent("summarize", Summarizer(), ["summarize", "summary"])
        self._register_agent("reasoning", Reasoning(), ["why", "because", "explain"])
        self._register_agent("weather", WeatherAgent(), ["weather", "temperature"])
        self._register_agent("stock", StockAgent(), ["stock", "price", "market"])

    def _register_agent(self, name: str, agent: BaseAgent, keywords: list):
        self.agents[name] = {
            "instance": agent,
            "keywords": keywords,
        }

    def _route_to_agents(self, text: str) -> list:
        """Find agents whose keywords match the input text."""
        matched = []
        for name, data in self.agents.items():
            if any(keyword.lower() in text.lower() for keyword in data["keywords"]):
                matched.append(data["instance"])
        return matched

    def process_request(self, text: str) -> dict:
        """
        Process the user request by routing to appropriate agents.
        """
        try:
            selected_agents = self._route_to_agents(text)
            if not selected_agents:
                return {"error": "No suitable agent found for the input."}

            responses = {}
            for agent in selected_agents:
                output = agent.run(text)
                responses[agent.__class__.__name__] = output

            return responses

        except Exception as e:
            self.logger.log_error(f"Error in AgentManager: {e}")
            return {"error": str(e)}
