import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
load_dotenv()  
import os

# Path to your cleaned parquet file from Airflow
PARQUET_PATH = "/opt/airflow/dags/isoloops_cleaned.parquet"

# Load the file into a pandas DataFrame
df = pd.read_parquet(PARQUET_PATH)

def time_to_seconds(time_str):
    if isinstance(time_str, str):  # Ensure time_str is a string
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    return 0  # In case the time is invalid or empty

# Apply the time_to_seconds function to the 'start_time' and 'end_time' columns
df['start_seconds'] = df['start_time'].apply(time_to_seconds)
df['end_seconds'] = df['end_time'].apply(time_to_seconds)

# Calculate duration (end_seconds - start_seconds)
df['duration'] = df['end_seconds'] - df['start_seconds']

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
    duration INT,
    CONSTRAINT unique_sample UNIQUE (youtube_url, start_time, end_time)
);
"""
cursor.execute(create_table_sql)

# Insert data row by row (can be optimized later)
for _, row in df.iterrows():
    # print(f"Row data: {row}")  # Debug: check the row values

    insert_sql = """
    MERGE INTO SAMPLED_SONGS AS target
    USING (SELECT %s AS title, %s AS youtube_url, %s AS start_time, %s AS end_time,
                  %s AS sample_type, %s AS description, %s AS genre, %s AS decade,
                  %s AS start_seconds, %s AS end_seconds, %s AS duration) AS source
    ON target.youtube_url = source.youtube_url
       AND target.start_time = source.start_time
       AND target.end_time = source.end_time
    WHEN NOT MATCHED THEN
        INSERT (title, youtube_url, start_time, end_time, sample_type, description,
                genre, decade, start_seconds, end_seconds, duration)
        VALUES (source.title, source.youtube_url, source.start_time, source.end_time,
                source.sample_type, source.description, source.genre, source.decade,
                source.start_seconds, source.end_seconds, source.duration);
    """
    
    cursor.execute(insert_sql, tuple(row))

print("Data uploaded to Snowflake!")

cursor.close()
conn.close()