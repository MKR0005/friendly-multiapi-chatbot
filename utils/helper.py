import json

class DataManager:
    @staticmethod
    def load_json(file_path: str) -> dict:
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return {}

    @staticmethod
    def save_json(file_path: str, data: dict) -> None:
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving JSON file: {e}")
