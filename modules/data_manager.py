import os
import json

class DataManager:
    def __init__(self):
        self.responses_dir = os.path.join(os.getcwd(), "data", "responses")
        os.makedirs(self.responses_dir, exist_ok=True)

    def save_response(self, api_name: str, response_data: dict):
        try:
            file_path = os.path.join(self.responses_dir, f"{api_name}.json")
            with open(file_path, "w") as file:
                json.dump(response_data, file)
            print(f"Response saved for {api_name}")
        except Exception as e:
            print(f"Error saving response for {api_name}: {e}")

    def load_response(self, api_name: str) -> dict:
        try:
            file_path = os.path.join(self.responses_dir, f"{api_name}.json")
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"No data found for {api_name}")
            return {}
        except Exception as e:
            print(f"Error loading response for {api_name}: {e}")
            return {}
