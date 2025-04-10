import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()  
import os

# Path to your cleaned parquet file from Airflow
PARQUET_PATH = "airflow/dags/isoloops_cleaned.parquet"

# Load the file into a pandas DataFrame
df = pd.read_parquet(PARQUET_PATH)

# Snowflake connection
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_sql = """
CREATE TABLE IF NOT EXISTS SAMPLED_SONGS (
    title STRING,
    youtube_url STRING,
    start_time STRING,
    end_time STRING,
    sample_type STRING,
    description STRING,
    genre STRING,
    decade STRING,
    start_seconds INT,
    end_seconds INT,
    duration INT
);
"""
cursor.execute(create_table_sql)

# Insert data row by row (can be optimized later)
for _, row in df.iterrows():
    insert_sql = f"""
    INSERT INTO SAMPLED_SONGS (
        title, youtube_url, start_time, end_time, sample_type,
        description, genre, decade, start_seconds, end_seconds, duration
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_sql, tuple(row))

print("✅ Data uploaded to Snowflake!")

cursor.close()
conn.close()