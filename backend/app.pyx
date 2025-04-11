from flask import Flask, jsonify
import snowflake.connector
from dotenv import load_dotenv
import os
from flask_cors import CORS


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
@app.route('/api/songs', methods=['GET'])
def get_songs():
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

    # Query to fetch data from Snowflake
    query = """
    SELECT title, youtube_url, start_time, end_time, sample_type,
           description, genre, decade, start_seconds, end_seconds, duration
    FROM ISOLOOPS_DB.PUBLIC.SAMPLED_SONGS
    """
    cursor.execute(query)

    # Fetch results
    data = cursor.fetchall()

    # Optionally, convert the results into a list of dictionaries
    columns = [col[0] for col in cursor.description]
    data_dict = [dict(zip(columns, row)) for row in data]

    # Close the connection
    cursor.close()
    conn.close()

    return jsonify(data_dict)  # Return data as JSON

if __name__ == '__main__':
    app.run(debug=True)

    