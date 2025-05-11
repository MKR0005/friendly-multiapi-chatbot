import requests

class APIHandler:
    def __init__(self, name, url, headers):
        self.name = name
        self.url = url
        self.headers = headers

    def get_data(self, params=None):
        try:
            response = requests.get(self.url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from {self.name}: {e}")
            return None
