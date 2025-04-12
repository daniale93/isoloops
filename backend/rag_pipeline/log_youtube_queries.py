import os
from dotenv import load_dotenv
from pathlib import Path
from generate_sample_targets import generate_sample_queries

# Load .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

def log_queries():
    queries = generate_sample_queries()
    print("✅ Queries to be searched on YouTube:")
    for idx, q in enumerate(queries):
        print(f"{idx+1}. {q}")

if __name__ == "__main__":
    log_queries()