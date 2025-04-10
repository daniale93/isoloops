from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

CSV_PATH = "/opt/airflow/dags/sample_scope_songs.csv"
OUTPUT_PATH = "/opt/airflow/dags/isoloops_cleaned.parquet"



def clean_and_transform():
    df = pd.read_csv(CSV_PATH)

    def time_to_seconds(t):
        parts = [int(x) for x in t.split(":")]
        return sum(x * 60 ** i for i, x in enumerate(reversed(parts)))

    df["start_seconds"] = df["start_time"].apply(time_to_seconds)
    df["end_seconds"] = df["end_time"].apply(time_to_seconds)
    df["duration"] = df["end_seconds"] - df["start_seconds"]
    df["genre"] = df["genre"].str.title().str.strip()

    df.to_parquet(OUTPUT_PATH, index=False)
    print(f"✅ Wrote cleaned file to {OUTPUT_PATH}")


with DAG(
    dag_id="isoloops_ingest",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["isoloops"],
) as dag:
    clean_task = PythonOperator(
        task_id="clean_and_transform_csv",
        python_callable=clean_and_transform,
    )

    clean_task