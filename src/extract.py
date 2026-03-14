import requests 
import pandas  as pd
from utils import send_request


def extract_coin_list(as_frame = False): 
    endpoint = "/coins/list"
    data =send_request(endpoint)
    if as_frame: 
        return pd.DataFrame(data)

    return data

def extract_market_chart(coin_id, vs_currency = 'usd', days = 1): 
    # function pulls crypto prices every 5 minute
    endpoint = f'/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days
    }

    data = send_request(endpoint, params=params)
    return  data