import os
import datetime as dt
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    "owner": "mahmoud",
    "start_date": dt.datetime(2026, 3, 14),
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
    dag_id="market_chart_dag",
    description="Run crypto_scraper to scrape crypto data",
    # Set your desired schedule interval or use None for manual triggering
    schedule_interval="0 */2 * * *", # every 2 hours
    catchup=False, # avoid running previous schedules
) as dag:
    
    market_chart = DockerOperator(
        task_id="market_chart",
        docker_url="unix://var/run/docker.sock",  # Use the default Docker socket
        api_version="auto",  # Use "auto" to let Docker select the appropriate API version
        auto_remove="success",  # Remove the container when the task completes
        image="crypto-scraper",  # Replace with your Docker image and tag
        command="market_chart",  # Replace with the command you want to run inside the container
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

    market_chart