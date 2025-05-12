import json
from utils.logger import Logger  # Assuming you have a Logger class for better error handling

class DataManager:
    @staticmethod
    def load_json(file_path: str) -> dict:
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            logger = Logger()
            logger.log_error(f"Error loading JSON file {file_path}: {e}")
            return {}

    @staticmethod
    def save_json(file_path: str, data: dict) -> None:
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            logger = Logger()
            logger.log_info(f"Successfully saved data to {file_path}")
        except Exception as e:
            logger = Logger()
            logger.log_error(f"Error saving JSON file {file_path}: {e}")
