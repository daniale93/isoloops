from http.server import BaseHTTPRequestHandler
from snowflake_api import query_snowflake
import json

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        try:
            sql = """
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
                    duration
                FROM SAMPLED_SONGS
                WHERE sample_type IN ('vocals_only', 'drums_only', 'percussion_intro')
                ORDER BY RANDOM()
                LIMIT 50
            """

            results = query_snowflake(sql)

            columns = [
                "title", "youtube_url", "start_time", "end_time", "sample_type",
                "description", "genre", "decade", "start_seconds", "end_seconds", "duration"
            ]
            data = [dict(zip(columns, row)) for row in results]

            self._set_headers()
            self.wfile.write(json.dumps({"samples": data}, indent=2).encode())

        except Exception as e:
            self._set_headers(status=500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())