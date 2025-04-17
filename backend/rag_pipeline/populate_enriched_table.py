import os
import snowflake.connector
from dotenv import load_dotenv

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
        view_count NUMBER,
        like_count NUMBER,
        comment_count NUMBER,
        resolution STRING,
        artist STRING,
        chatgpt_prompt STRING
    );
    """)

    # Perform batch MERGE from staging to enriched
    cursor.execute("""
    MERGE INTO SAMPLED_SONGS_ENRICHED AS target
    USING (
        SELECT
            title,
            youtube_url,
            start_time,
            end_time,
            sample_type,
            description,
            genre,
            decade,
            start_seconds,
            end_seconds,
            duration,
            query_used,
            timestamp_loaded,
            youtube_rank,
            view_count,
            like_count,
            comment_count,
            resolution,
            artist,
            chatgpt_prompt
        FROM SAMPLED_SONGS_STAGING
    ) AS source
    ON target.youtube_url = source.youtube_url
    WHEN MATCHED THEN UPDATE SET
        title = source.title,
        start_time = source.start_time,
        end_time = source.end_time,
        sample_type = source.sample_type,
        description = source.description,
        genre = source.genre,
        decade = source.decade,
        start_seconds = source.start_seconds,
        end_seconds = source.end_seconds,
        duration = source.duration,
        query_used = source.query_used,
        timestamp_loaded = source.timestamp_loaded,
        youtube_rank = source.youtube_rank,
        view_count = source.view_count,
        like_count = source.like_count,
        comment_count = source.comment_count,
        resolution = source.resolution,
        artist = source.artist,
        chatgpt_prompt = source.chatgpt_prompt
    WHEN NOT MATCHED THEN INSERT (
        title,
        youtube_url,
        start_time,
        end_time,
        sample_type,
        description,
        genre,
        decade,
        start_seconds,
        end_seconds,
        duration,
        query_used,
        timestamp_loaded,
        youtube_rank,
        view_count,
        like_count,
        comment_count,
        resolution,
        artist,
        chatgpt_prompt
    ) VALUES (
        source.title,
        source.youtube_url,
        source.start_time,
        source.end_time,
        source.sample_type,
        source.description,
        source.genre,
        source.decade,
        source.start_seconds,
        source.end_seconds,
        source.duration,
        source.query_used,
        source.timestamp_loaded,
        source.youtube_rank,
        source.view_count,
        source.like_count,
        source.comment_count,
        source.resolution,
        source.artist,
        source.chatgpt_prompt
    );
    """)

    conn.commit()
    print("✅ Enriched table populated with merged rows from staging.")
    cursor.close()
    conn.close()
