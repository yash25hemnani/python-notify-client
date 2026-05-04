import requests
from .env import ENV

class ApiClient:
    def __init__(self):
        self.api_key = ENV["API_KEY"]
        self.base_url = ENV["BASE_URL"]
        
    def _headers(self):
            return {
                "x-api-key": f"{self.api_key}",
                "Accept": "application/json"
            }
    
    def get(self, endpoint:str, params:dict = None):
         return requests.get(f"{self.base_url}{endpoint}",
            headers=self._headers(), params=params)
        
    def post(self, endpoint:str, data=None, files=None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            headers=self._headers(),
            data=data if files else None,
            json=data if not files else None,
            files=files
        )
        