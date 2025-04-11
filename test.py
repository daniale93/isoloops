import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()  # Load environment variables from .env file

# Snowflake connection parameters
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

# Test the Snowflake query
try:
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM isoloops_db.public.sampled_songs LIMIT 5"  # Example query
    cursor.execute(query)
    result = cursor.fetchall()
    print(result)

    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")