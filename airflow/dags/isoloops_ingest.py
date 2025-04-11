from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import pandas as pd
import os

# Define CSV and Parquet file paths
CSV_PATH = '/opt/airflow/data/sample_scope_songs.csv'
OUTPUT_PARQUET_PATH = '/opt/airflow/dags/isoloops_cleaned.parquet'


# Function to convert CSV to Parquet
def csv_to_parquet():
    df = pd.read_csv(CSV_PATH)
    df.to_parquet(OUTPUT_PARQUET_PATH, index=False)
    print(f"✅ Wrote cleaned file to {OUTPUT_PARQUET_PATH}")


# The function to run the Snowflake loader script
def run_loader():
    subprocess.run(["python3", "/opt/airflow/dags/load_to_snowflake.py"], check=True)


# Create the DAG
def create_dag():
    with DAG(
        dag_id='isoloops_ingest',  # Make sure this is the same name
        schedule_interval=None,  # No schedule (triggered manually)
        start_date=datetime(2023, 1, 1),
        catchup=False,
        concurrency=1,
        tags=["isoloops"],  # Add tags if needed
    ) as dag:

        # Task to convert CSV to Parquet
        convert_task = PythonOperator(
            task_id='convert_csv_to_parquet',
            python_callable=csv_to_parquet
        )

        # Task to load data into Snowflake
        load_task = PythonOperator(
            task_id='load_to_snowflake',
            python_callable=run_loader,
        )

        # Define the task dependencies: convert first, then load to Snowflake
        convert_task >> load_task

    return dag


# Register the DAG globally
globals()['isoloops_ingest'] = create_dag()