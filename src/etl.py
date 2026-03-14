from sys import argv
from os import getenv
from dotenv import load_dotenv
import utils
import extract, transform, load

if __name__=="__main__":

    # Check if the script is run with the correct argument
    task_to_run = argv[1] if len(argv) > 1 else None
    if task_to_run not in ["coins_list", "market_chart"]:
        raise ValueError("Please provide a valid task to run: 'coins_list' or 'market_chart'.")

    load_dotenv()

    # Load environment variables
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_NAME = getenv("DB_NAME")

    print("DB_USER", DB_USER)
    print("DB_PASSWORD", DB_PASSWORD)
    print("DB_HOST", DB_HOST)
    print("DB_PORT", DB_PORT)
    print("DB_NAME", DB_NAME)

    engine = utils.get_engine(
        db_user=DB_USER,
        db_password=DB_PASSWORD,
        db_host=DB_HOST,
        db_port=DB_PORT,
        db_name=DB_NAME
    )

    if task_to_run=="coins_list":
         
        # Extract
        df_coins_list = extract.extract_coins_list(as_frame=True)

        # Load
        transform.truncate_table(engine, "coins_list")
        load.load_df_to_table(df_coins_list, engine, "coins_list")

        n_records = df_coins_list.shape[0]
        print(f"Loaded {n_records} into coins_list table.")
    
    else:
        with open("coins.txt") as fp:
            coin_ids = [line.strip() for line in fp.readlines() if line.strip()]

        for coin_id in coin_ids:
            # Extract
            market_chart_eth = extract.extract_market_chart(coin_id=coin_id)

            # Transform 
            df_market_chart_eth = transform.transform_market_chart(coin_id=coin_id, data=market_chart_eth)
            last_timestamp = transform.get_last_market_chart_timestamp(coin_id=coin_id, engine=engine)
            df_market_chart_eth_filtered = transform.filter_new_records(df_market_chart_eth, last_timestamp)

            n_records = df_market_chart_eth_filtered.shape[0]

            # Load 
            load.load_df_to_table(df_market_chart_eth_filtered, engine, "market_chart")

            print(f"{coin_id}: Loaded {n_records} into market_chart table.")