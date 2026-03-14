FROM python:3.11-slim-bookworm

# Set working directory inside container
WORKDIR /app

# Install dependencies required for psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Copy requirements and install dependencies first (for caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY src/ src/
COPY coins.txt .
COPY .env .

# Set default command (overridden when passing arguments)
ENTRYPOINT ["python", "src/etl.py"]