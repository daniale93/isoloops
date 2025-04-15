import os
import random
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

MAX_QUERIES = int(os.getenv("MAX_QUERIES", 10))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPTS = [
    f"Give me a list of {MAX_QUERIES} artists known for having strong isolated percussion or vocal sections, ideal for sampling in Afro, Latin, funk, or world music genres. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} rare or obscure musicians whose tracks include extended drum breaks or acapella sections suitable for sampling in Afrobeat, salsa, funk, or cumbia. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} vintage percussion-heavy artists from the 1960s to 1980s ideal for use in Afro-Latin electronic production. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} African or Caribbean artists known for stripped-down vocal intros or rhythm sections ideal for sampling. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} funk, Latin jazz, or folkloric artists with recordings containing isolated drums or vocals. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} lesser-known bands that often leave space for drum solos or vocal improvisation, ideal for sampling in electronic or hip-hop music. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} artists whose music features sparse arrangements and clean percussive elements, ideal for use in Afro-house or tribal edits. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} artists who use traditional instruments in a way that results in clear isolated grooves. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} global artists from the 1970s and 1980s whose recordings often isolate drums, vocals, or horns. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} musicians from Africa, Latin America, or Southeast Asia whose recordings feature minimal arrangements or clean percussive moments. List only the names—no extra explanation.",
    f"Give me a list of {MAX_QUERIES} YouTube creators who post isolated instrument recordings—especially percussion, bass, or ethnic instruments—ideal for sampling in Afro, Latin, funk, or world music. List only the names—no extra explanation",
    f"Give me a list of {MAX_QUERIES} List 10 field recording sessions where street musicians or traditional performers are playing instruments with no background music. Focus on Latin America, West Africa, or Southeast Asia. List only the names—no extra explanation",
    f"Give me a list of {MAX_QUERIES} videos or creators that showcase traditional or rare instruments (like berimbau, balafon, marimba, handpan, etc.) played solo and in high audio quality. List only the names—no extra explanation",
    f"Give me a list of {MAX_QUERIES} videos of traditional chants, call-and-response, or ritual music from indigenous or rural communities—especially with isolated vocals or percussion. List only the names—no extra explanation",
    f"Give me a list of {MAX_QUERIES}  rare or public domain recordings of political speeches, sermons, or interviews that are clean and have unique vocal tone or delivery style, suitable for sampling. List only the names—no extra explanation",
]

# Store selected prompt in global var
last_prompt = None

def generate_sample_queries():
    global last_prompt
    last_prompt = random.choice(PROMPTS)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": last_prompt}],
        temperature=0.9
    )

    text = response.choices[0].message.content
    queries = [line.strip("0123456789. ").strip() for line in text.splitlines() if line.strip()]
    return queries

def get_prompt_used():
    return last_prompt or ""