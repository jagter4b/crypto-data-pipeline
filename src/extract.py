import requests
import pandas as pd
from utils import send_request

def extract_coins_list(as_frame: bool = False) -> dict | pd.DataFrame:
    """ Extracts the list of coins from CoinGecko API.
    """
    endpoint = "/coins/list"
    data = send_request(endpoint)
    if as_frame:
        return pd.DataFrame(data)
    return data

def extract_market_chart(coin_id: str, vs_currency: str = "usd", days: int = 1) -> dict:
    """ Extracts the market chart data for a specific coin.
    Args:
        coin_id (str): The ID of the coin to extract data for.
        vs_currency (str): The currency to convert to. Default is "usd".
        days (int): The number of days to look back. Default is 1.
    """
    # The function that scrapes crypto prices in 5-minute increment
    endpoint = f"/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
    }
    data = send_request(endpoint, params=params)
    return data