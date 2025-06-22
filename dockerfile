# Base image from the official Airflow image
FROM apache/airflow:3.0.2

# Set the environment variable for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Switch to root user to install system dependencies
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch to airflow user before installing Python packages
USER airflow

# Install Python packages as airflow user
RUN pip install --upgrade pip setuptools wheel \
    && pip install \
        dbt-core \
        dbt-snowflake

# Expose necessary ports for Airflow
EXPOSE 8080

# Set the command to run Airflow's webserver by default
CMD ["webserver"]
