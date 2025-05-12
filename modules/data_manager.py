import os
import json
from utils.logger import Logger

class DataManager:
    def __init__(self):
        self.logger = Logger()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.responses_dir = os.path.join(base_dir, "..", "data", "responses")
        os.makedirs(self.responses_dir, exist_ok=True)

    def save_response(self, api_name: str, response_data: dict):
        try:
            file_path = os.path.join(self.responses_dir, f"{api_name}.json")
            with open(file_path, "w") as file:
                json.dump(response_data, file, indent=4)
            self.logger.log_info(f"Response saved for {api_name}")
        except Exception as e:
            self.logger.log_error(f"Error saving response for {api_name}: {e}")

    def load_response(self, api_name: str) -> dict:
        try:
            file_path = os.path.join(self.responses_dir, f"{api_name}.json")
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.log_warning(f"No data found for {api_name}")
            return {}
        except Exception as e:
            self.logger.log_error(f"Error loading response for {api_name}: {e}")
            return {}
