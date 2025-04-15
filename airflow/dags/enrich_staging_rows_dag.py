from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add backend directory to path
sys.path.append('/opt/airflow/backend')
from rag_pipeline.enrich_staging_rows import enrich_staging_rows

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 4, 13),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="enrich_staging_rows",
    description="Enrich missing artist and genre fields from SAMPLED_SONGS_STAGING using LLM",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["enrichment", "llm"],
) as dag:

    enrich_task = PythonOperator(
        task_id="run_enrich_staging_rows",
        python_callable=enrich_staging_rows,
    )
