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
            # Ensure that the API configuration exists
            api_info = self.apis.get(api_name)
            if not api_info:
                raise ValueError(f"API '{api_name}' not found in the configuration.")

            # Construct the final URL
            url = api_info["base_url"] + endpoint
            
            # Merge default parameters with the user-provided ones
            default_params = api_info.get("params", {})
            final_params = {**default_params, **(params or {})}  # Merge dicts
            
            headers = api_info.get("headers", {})
            
            # Make the GET request to the API
            response = requests.get(url, params=final_params, headers=headers)
            response.raise_for_status()

            # Return the response as JSON
            return response.json()

        except requests.HTTPError as http_err:
            self.logger.log_error(f"HTTP error in {api_name}: {http_err}")
        except ValueError as val_err:
            self.logger.log_error(f"Configuration error in {api_name}: {val_err}")
        except Exception as err:
            self.logger.log_error(f"Error in {api_name}: {err}")
        
        # Return empty dictionary if there's an error
        return {}
