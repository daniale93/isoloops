import sys
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
sys.path.append('/opt/airflow/backend')

from rag_pipeline.generate_sample_targets import generate_sample_queries, get_prompt_used
from rag_pipeline.search_youtube import search_many
from rag_pipeline.load_to_snowflake import load_to_snowflake

def discovery_flow():
    # Generate queries and capture the selected prompt
    queries = generate_sample_queries()
    prompt_used = get_prompt_used()

    print("🔍 Raw queries from LLM:", queries)
    print("🧠 Prompt used:", prompt_used)

    cleaned_queries = []
    for q in queries:
        if "-" in q:
            cleaned_queries.append(q.strip())
        elif len(q.split()) <= 6:
            cleaned_queries.append(q.strip())

    if not cleaned_queries:
        print("⚠️ No valid search queries after cleaning.")
        return

    results_df = search_many(cleaned_queries)
    results_df["chatgpt_prompt"] = prompt_used

    load_to_snowflake(results_df, chatgpt_prompt=prompt_used)

with DAG(
    dag_id='rag_daily_discovery',
    schedule='@daily',
    start_date=datetime(2024, 4, 10),
    catchup=False
) as dag:
    run_discovery = PythonOperator(
        task_id='run_discovery_flow',
        python_callable=discovery_flow
    )