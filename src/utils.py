import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_KEY= getenv("API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"

def send_request(endpoint, params=None): 
    url =f'{BASE_URL}{endpoint}'
    headers = {
        'accept': 'application/json',
        'x-cg-demo-api-key':API_KEY
    }

    response = requests.get(url, headers=headers, params=params )
    response.raise_for_status()
    return response.json()
