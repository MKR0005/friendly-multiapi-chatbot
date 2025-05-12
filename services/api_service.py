import requests
from config import Config
from utils.logger import Logger

class APIService:
    def __init__(self):
        self.logger = Logger()

    def fetch_data(self, api_name: str, endpoint: str = "", params: dict = None) -> dict:
        """
        Fetch data from the specified API using the API name and endpoint.
        """
        try:
            # Get API info from the config
            api_info = Config.API_CONFIG.get(api_name)
            if not api_info:
                self.logger.log_error(f"API '{api_name}' not found in the configuration.")
                return {}

            # Construct the full URL for the API call
            base_url = api_info.get("base_url", "")
            if not base_url:
                self.logger.log_error(f"Base URL for API '{api_name}' is not defined.")
                return {}

            url = base_url + endpoint
            headers = api_info.get("headers", {})
            final_params = {**api_info.get("params", {}), **(params or {})}

            # Send the GET request to the API
            response = requests.get(url, headers=headers, params=final_params, timeout=10)
            response.raise_for_status()

            # Return the API response as a JSON object
            return response.json()
        
        except requests.RequestException as e:
            self.logger.log_error(f"Error fetching data from API '{api_name}': {e}")
            return {}
        except Exception as e:
            self.logger.log_error(f"An unexpected error occurred while fetching data from API '{api_name}': {e}")
            return {}

