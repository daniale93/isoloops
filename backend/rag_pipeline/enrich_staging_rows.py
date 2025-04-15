import os
import time
import json
import re
import pandas as pd
import snowflake.connector
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_staging_rows():
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

    # Fetch rows where enrichment is needed
    cursor.execute("SELECT * FROM SAMPLED_SONGS_STAGING WHERE artist IS NULL OR genre IS NULL")
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    if df.empty:
        print("✅ No rows to enrich.")
        return

    enriched_count = 0

    for _, row in df.iterrows():
        try:
            prompt = f"""
Based on the title and video link, describe what this video likely contains, especially in terms of its usefulness for sampling for a music producer. Then infer and return the most likely genre, decade, artist, and sample_type. Use this format:

Title: {row['TITLE']}
YouTube URL: {row['YOUTUBE_URL']}

{{
  "artist": "...",
  "genre": "...",  # Choose from: ["Afrobeat", "Latin Jazz", "Funk", "Cumbia", "Salsa", "Reggae", "World Music", "Jazz", "Tropicália", "Blues", "Soul", "MPB", "Highlife", "Folk", "Bolero", "Rock", "Pop", "Classical", "Hip Hop", "Bluegrass", "Electronic", "Neo Soul"]
  "description": "...",  # Describe what kind of sampling potential this has
  "decade": "...",  # Format: 1960s, 1970s, etc.
  "sample_type": "..."  # Choose from: ["isolated percussion", "isolated vocals", "instrumental section", "live performance", "full track", "intro", "breakdown", "remix"]

}}


Respond ONLY with valid JSON. Do not include markdown or any explanation — just the JSON object.
"""
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            raw = response.choices[0].message.content.strip()
            print("🔍 LLM raw response:", raw)

            # Strip markdown formatting
            clean = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE)
            data = json.loads(clean)

            cursor.execute("""
                UPDATE SAMPLED_SONGS_STAGING
                SET artist = %s,
                    genre = %s,
                    description = %s,
                    decade = %s,
                    sample_type = %s
                WHERE youtube_url = %s
            """, (
                data.get("artist"),
                data.get("genre"),
                data.get("description"),
                data.get("decade"),
                data.get("sample_type"),
                row["YOUTUBE_URL"]
            ))

            enriched_count += 1
        except Exception as e:
            print("⚠️ Failed to parse LLM response:", e)
            print("Response content:", raw)
            continue

        time.sleep(1.5)  # Throttle to avoid rate limits

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Enriched {enriched_count} rows in Snowflake.")

if __name__ == "__main__":
    enrich_staging_rows()