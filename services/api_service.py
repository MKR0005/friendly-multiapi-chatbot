import requests
from config import API_CONFIG

class APIManager:
    def __init__(self):
        self.api_handlers = {}
        self.load_apis()

    def load_apis(self):
        for api_name, api_info in API_CONFIG.items():
            self.api_handlers[api_name] = APIHandler(
                api_name,
                api_info['url'],
                api_info.get('headers', {}),
                api_info.get('params', {})
            )

    def fetch_data(self, api_name, params=None):
        if api_name in self.api_handlers:
            return self.api_handlers[api_name].get_data(params)
        else:
            print(f"API {api_name} not found")
            return None

class APIHandler:
    def __init__(self, name, url, headers, params):
        self.name = name
        self.url = url
        self.headers = headers
        self.params = params

    def get_data(self, additional_params=None):
        try:
            params = {**self.params, **(additional_params or {})}
            response = requests.get(self.url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from {self.name}: {e}")
            return None
