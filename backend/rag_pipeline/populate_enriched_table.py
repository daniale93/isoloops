import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import datetime as dt

# Load environment variables
load_dotenv()

def populate_enriched_table():
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cursor = conn.cursor()

    # Create enriched table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SAMPLED_SONGS_ENRICHED (
        title STRING,
        youtube_url STRING,
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
        video_duration NUMBER,
        view_count NUMBER,
        like_count NUMBER,
        comment_count NUMBER,
        resolution STRING
    );
    """)

    # Read from staging table
    cursor.execute("SELECT * FROM SAMPLED_SONGS_STAGING")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=columns)

    if df.empty:
        print("⚠️ No data in SAMPLED_SONGS_STAGING to enrich.")
        cursor.close()
        conn.close()
        return

    # Drop duplicates based on youtube_url
    df = df.drop_duplicates(subset=["YOUTUBE_URL"])

    for _, row in df.iterrows():
        values = [
            row["YOUTUBE_URL"],
            row["TITLE"],
            row.get("START_TIME", ""),
            row.get("END_TIME", ""),
            row.get("SAMPLE_TYPE", ""),
            row.get("DESCRIPTION", ""),
            row.get("GENRE", ""),
            row.get("DECADE", ""),
            row.get("START_SECONDS", 0),
            row.get("END_SECONDS", 0),
            row.get("DURATION", 0),
            row.get("QUERY_USED", ""),
            str(row.get("TIMESTAMP_LOADED", dt.datetime.now(dt.timezone.utc).isoformat())),
            row.get("YOUTUBE_RANK", 0),
            row.get("VIDEO_DURATION", 0),
            row.get("VIEW_COUNT", 0),
            row.get("LIKE_COUNT", 0),
            row.get("COMMENT_COUNT", 0),
            row.get("RESOLUTION", "")
        ]

        cursor.execute("""
            MERGE INTO SAMPLED_SONGS_ENRICHED AS target
            USING (SELECT %s AS youtube_url) AS source
            ON target.youtube_url = source.youtube_url
            WHEN MATCHED THEN UPDATE SET
                target.title = %s,
                target.start_time = %s,
                target.end_time = %s,
                target.sample_type = %s,
                target.description = %s,
                target.genre = %s,
                target.decade = %s,
                target.start_seconds = %s,
                target.end_seconds = %s,
                target.duration = %s,
                target.query_used = %s,
                target.timestamp_loaded = %s,
                target.youtube_rank = %s,
                target.video_duration = %s,
                target.view_count = %s,
                target.like_count = %s,
                target.comment_count = %s,
                target.resolution = %s
            WHEN NOT MATCHED THEN INSERT (
                youtube_url, title, start_time, end_time, sample_type, description,
                genre, decade, start_seconds, end_seconds, duration,
                query_used, timestamp_loaded, youtube_rank,
                video_duration, view_count, like_count, comment_count, resolution
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, [values[0]] + values[1:] + values)

    conn.commit()
    print(f"✅ Enriched table populated with {len(df)} rows.")
    cursor.close()
    conn.close()