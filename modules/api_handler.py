import requests
from utils.logger import Logger
from config import API_CONFIG  # Dict of API metadata

class APIHandler:
    def __init__(self):
        self.logger = Logger()
        self.apis = API_CONFIG

    def fetch_data(self, api_name: str, endpoint: str, params: dict = None) -> dict:
        """
        Fetch data from a specified API endpoint.
        """
        try:
            api_info = self.apis.get(api_name)
            if not api_info:
                raise ValueError(f"API '{api_name}' not found")

            url = api_info["base_url"] + endpoint
            headers = api_info.get("headers", {})
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.HTTPError as http_err:
            self.logger.log_error(f"HTTP error in {api_name}: {http_err}")
        except Exception as err:
            self.logger.log_error(f"Error in {api_name}: {err}")
        return {}
