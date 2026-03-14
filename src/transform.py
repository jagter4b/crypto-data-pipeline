import pandas as pd
from sqlalchemy import Engine

def get_last_market_chart_tinestamp(coin_id, engine): 
    sql = f'''
        SELECT COALESCE(MAX(TIMESTAMP), '1900-01-01') AS last_timestamp
        FROM market_chart 
        WHERE coinm_id = "{coin_id}"
    '''
    df = pd.read_sql(sql, con=engine)
    return df['last_timestamp'].values[0]


def filter_new_records(df, last_timestamp):
    new_records = df[df['timestamp'] > last_timestamp]
    return new_records

def tranform_market_chart(coin_id, data, vs_currency='usd'): 
    prices = data['prices']
    market_caps = data['market_caps']
    total_volumes   = data['total_volumes']
    df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df_market_caps = pd.DataFrame(market_caps, columns = ['timestamp', 'market_cap'] )
    df_total_volumes = pd.DataFrame(total_volumes, columns= ['timestamp', 'total_volume'])

    df_market_chart= (

    df_prices.merge(df_market_caps, on='timestamp', how='inner')
    .merge(df_total_volumes, on='timestamp', how='inner')
    )
    df_market_chart['timestamp'] = pd.to_datetime(df_market_chart['timestamp'], unit='ms')
    df_market_chart['coin_id'] = coin_id
    df_market_chart['vs_currency'] = vs_currency

    return df_market_chart