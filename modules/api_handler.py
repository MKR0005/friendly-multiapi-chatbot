import requests
from utils.logger import Logger

class APIHandler:
    def __init__(self):
        self.logger = Logger()

        # Define the 20 APIs
        self.apis = {
            "news_api": "https://api.newsapi.com/v1/",
            "weather_api": "https://api.weather.com/v1/",
            "crypto_api": "https://api.crypto.com/v1/",
            "movies_api": "https://api.movies.com/v1/",
            "agri_api": "https://api.agriculture.com/v1/",
            # Add more APIs as needed
        }

    def fetch_data(self, api_name: str, endpoint: str, params: dict = None) -> dict:
        """Fetch data from a specified API endpoint."""
        try:
            base_url = self.apis.get(api_name)
            if not base_url:
                raise ValueError(f"API '{api_name}' not found")

            url = base_url + endpoint
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except requests.HTTPError as http_err:
            self.logger.log_error(f"HTTP error in {api_name}: {http_err}")
        except Exception as err:
            self.logger.log_error(f"Error in {api_name}: {err}")
        return {}
