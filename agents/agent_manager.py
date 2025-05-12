from agents.base_agent import BaseAgent
from modules.summarizer import Summarizer
from modules.reasoning import Reasoning
from utils.logger import Logger

class AgentManager:
    def __init__(self):
        self.logger = Logger()
        self.summarizer = Summarizer()
        self.reasoning = Reasoning()

    def process_request(self, text: str) -> dict:
        """Process user request using summarizer and reasoning agents."""
        try:
            summary = self.summarizer.summarize(text)
            reasoning_output = self.reasoning.reason(text, summary)
            return {
                "summary": summary,
                "reasoning": reasoning_output
            }
        except Exception as e:
            self.logger.log_error(f"Error in AgentManager: {e}")
            return {"error": str(e)}
