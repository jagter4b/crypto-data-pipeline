import os
import datetime as dt
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "mahmoud",
    "start_date": dt.datetime(2025, 4, 19),
    "retries": 0,
    # "retry_delay": dt.timedelta(minutes=3),
    # Add other default args like retries, etc.
}

COINGECKO_API_KEY=os.getenv("COINGECKO_API_KEY")
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")

with DAG(
    default_args=default_args,
    dag_id="coins_list_dag",
    description="Run  coins list",
    # Set your desired schedule interval or use None for manual triggering
    schedule_interval="0 0 1 * *", # every 1st day of the month
    catchup=False, # avoid running previous schedules
) as dag:
    
    coins_list = DockerOperator(
        task_id="docker_crypto_scraper_coins_list",
        docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        api_version="auto",  # Use "auto" to let Docker select the appropriate API version
        auto_remove="success",  # Remove the container when the task completes
        image="crypto-scraper",  # Replace with your Docker image and tag
        command="coins_list",  # Replace with the command you want to run inside the container
        environment={
            "COINGECKO_API_KEY": COINGECKO_API_KEY,
            "DB_USER": DB_USER,
            "DB_PASSWORD": DB_PASSWORD,
            "DB_HOST": DB_HOST,
            "DB_PORT": DB_PORT,
            "DB_NAME": DB_NAME,
        },
        network_mode="crypto_data_pipeline_default",
    )

    coins_list