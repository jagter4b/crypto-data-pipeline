import requests
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine, URL

load_dotenv()

COINGECKO_API_KEY = getenv("COINGECKO_API_KEY")
BASE_URL = "https://api.coingecko.com/api/v3"

def send_request(endpoint: str, params: dict = None) -> dict:
    """ Sends a GET request to the CoinGecko API.
    
    Args:
        endpoint (str): The API endpoint to send the request to.
        params (dict, optional): The query parameters to include in the request.
        
    Returns:
        dict: The JSON response from the API.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API_KEY,
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def get_engine(db_user: str, db_password: str, db_host: str, db_port: str, db_name: str):
    connection_string = URL.create(
        "postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )

    return create_engine(connection_string)