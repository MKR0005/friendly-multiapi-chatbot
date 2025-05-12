from abc import ABC, abstractmethod
from utils.logger import Logger

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.logger = Logger()  # Add a logger for all agents to use

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

    def log_info(self, message: str):
        """Convenient method to log info-level messages."""
        self.logger.log_info(f"{self.name}: {message}")

    def log_warning(self, message: str):
        """Convenient method to log warning-level messages."""
        self.logger.log_warning(f"{self.name}: {message}")

    def log_error(self, message: str):
        """Convenient method to log error-level messages."""
        self.logger.log_error(f"{self.name}: {message}")
