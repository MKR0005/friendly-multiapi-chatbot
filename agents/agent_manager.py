from agents.base_agent import BaseAgent
from agents.summarizer import Summarizer
from agents.reasoning import Reasoning
from utils.logger import Logger

class AgentManager:
    def __init__(self, api_key=None):
        self.logger = Logger()
        self.api_key = api_key
        self.agents = {}
        self._load_agents()

    def _load_agents(self):
        self._register_agent("summarize", Summarizer(self.api_key), ["summarize", "summary"])
        self._register_agent("reasoning", Reasoning(self.api_key), ["why", "because", "explain"])
        # Add more agents as needed

    def _register_agent(self, name: str, agent: BaseAgent, keywords: list):
        self.agents[name] = {
            "instance": agent,
            "keywords": keywords,
        }

    def _route_to_agents(self, text: str) -> list:
        matched = []
        for name, data in self.agents.items():
            if any(keyword.lower() in text.lower() for keyword in data["keywords"]):
                matched.append(data["instance"])
        return matched

    def process_request(self, text: str) -> dict:
        try:
            selected_agents = self._route_to_agents(text)
            if not selected_agents:
                return {"error": "No suitable agent found for the input."}

            responses = {}
            for agent in selected_agents:
                # Adjust based on your agent interface
                if hasattr(agent, "summarize"):
                    responses[agent.__class__.__name__] = agent.summarize(text)
                elif hasattr(agent, "reason"):
                    responses[agent.__class__.__name__] = agent.reason(text, text)
                else:
                    responses[agent.__class__.__name__] = "Agent method not found"
            return responses

        except Exception as e:
            self.logger.log_error(f"Error in AgentManager: {e}")
            return {"error": str(e)}
