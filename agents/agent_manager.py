from agents.base_agent import BaseAgent
from modules.summarizer import Summarizer
from modules.reasoning import Reasoning

class AgentManager:
    def __init__(self, api_key: str):
        self.summarizer = Summarizer(api_key)
        self.reasoning = Reasoning(api_key)

    def process_request(self, text: str) -> dict:
        """Process user request using summarizer and reasoning agents."""
        try:
            summary = self.summarizer.summarize(text)
            reasoning_output = self.reasoning.reason(text)
            return {
                "summary": summary,
                "reasoning": reasoning_output
            }
        except Exception as e:
            print(f"Error in AgentManager: {e}")
            return {"error": str(e)}
