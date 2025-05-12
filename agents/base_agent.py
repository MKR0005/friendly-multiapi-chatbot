# base_agent.py

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(self, input_data: dict) -> dict:
        """
        Process the input data and return the response.
        Each agent must implement this method.
        """
        pass

    def get_name(self) -> str:
        """
        Return the name of the agent.
        """
        return self.name
