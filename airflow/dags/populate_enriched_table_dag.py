import os
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd


sys.path.append('/opt/airflow/backend')
from rag_pipeline.populate_enriched_table import populate_enriched_table  # Adjust path if needed
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='populate_sampled_songs_enriched',
    default_args=default_args,
    description='Populate enriched metadata table for sampled songs',
    schedule=None,
    start_date=datetime(2025, 4, 11),
    catchup=False,
    tags=['isoloops', 'enrichment'],
) as dag:

    run_population = PythonOperator(
        task_id='populate_enriched_table',
        python_callable=populate_enriched_table,
    )

    run_population