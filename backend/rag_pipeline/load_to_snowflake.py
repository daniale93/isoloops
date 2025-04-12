import os
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

def load_to_snowflake(df: pd.DataFrame):
    if df.empty:
        print("⚠️ No data to load.")
        return

    # Establish connection
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SAMPLED_SONGS_STAGING (
        title STRING,
        youtube_url STRING PRIMARY KEY,
        start_time STRING,
        end_time STRING,
        sample_type STRING,
        description STRING,
        genre STRING,
        decade STRING,
        start_seconds NUMBER,
        end_seconds NUMBER,
        duration NUMBER,
        query_used STRING,
        timestamp_loaded TIMESTAMP_TZ,
        youtube_rank NUMBER,
        view_count NUMBER,
        like_count NUMBER,
        comment_count NUMBER,
        resolution STRING
    )
    """)

    merge_sql = """
    MERGE INTO SAMPLED_SONGS_STAGING AS target
    USING (SELECT %s AS youtube_url) AS source
    ON target.youtube_url = source.youtube_url
    WHEN NOT MATCHED THEN
      INSERT (
        title, youtube_url, start_time, end_time, sample_type,
        description, genre, decade, start_seconds, end_seconds,
        duration, query_used, timestamp_loaded, youtube_rank,
        view_count, like_count, comment_count, resolution
      )
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            row.get("youtube_url"),
            row.get("title"),
            row.get("youtube_url"),
            "",  # start_time
            "",  # end_time
            "",  # sample_type
            row.get("description", ""),
            "",  # genre
            "",  # decade
            0,   # start_seconds
            0,   # end_seconds
            row.get("duration", 0),
            row.get("query_used"),
            row.get("timestamp_loaded"),
            row.get("youtube_rank"),
            row.get("view_count"),
            row.get("like_count"),
            row.get("comment_count"),
            row.get("resolution"),
        )
        cursor.execute(merge_sql, values)

    conn.commit()
    print(f"✅ Loaded {len(df)} rows to Snowflake.")

    cursor.close()
    conn.close()