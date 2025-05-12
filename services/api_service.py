import requests
from config import Config
from utils.logger import Logger
import time

class APIService:
    def __init__(self, retries: int = 3, timeout: int = 10):
        self.logger = Logger()
        self.retries = retries
        self.timeout = timeout

    def fetch_data(self, api_name: str, endpoint: str = "", params: dict = None) -> dict:
        """
        Fetch data from the specified API using the API name and endpoint.
        Implements retries in case of transient errors.
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

            # Attempt to fetch data, with retries
            for attempt in range(self.retries):
                try:
                    response = requests.get(url, headers=headers, params=final_params, timeout=self.timeout)
                    response.raise_for_status()
                    return response.json()  # Return the successful response

                except requests.RequestException as e:
                    if attempt < self.retries - 1:
                        self.logger.log_warning(f"Error fetching data from API '{api_name}', retrying ({attempt + 1}/{self.retries}): {e}")
                        time.sleep(2)  # Wait before retrying
                    else:
                        self.logger.log_error(f"Error fetching data from API '{api_name}' after {self.retries} attempts: {e}")
                        return {}

        except Exception as e:
            self.logger.log_error(f"An unexpected error occurred while fetching data from API '{api_name}': {e}")
            return {}
