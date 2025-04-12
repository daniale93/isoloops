import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sample_queries():
    prompt = (
        "Give me a list of 40 songs or artists known for strong isolated percussion or vocal sections "
        "ideal for sampling, across Afro, Latin, funk, or world genres. Format as a numbered list with just names."
        "For example, grab songs from groups like Percussioney, Quinta Feira, Rubens Bassini, Mongo santamaria"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    text = response.choices[0].message.content
    queries = [line.strip("0123456789. ").strip() for line in text.splitlines() if line.strip()]
    return queries

if __name__ == "__main__":
    queries = generate_sample_queries()
    for q in queries:
        print("-", q)