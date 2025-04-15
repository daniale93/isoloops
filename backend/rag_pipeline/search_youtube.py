import os
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# YouTube API config
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"

# Throttle limits with sensible defaults
MAX_QUERIES = int(os.getenv("MAX_QUERIES", 10))
MAX_RESULTS_PER_QUERY = int(os.getenv("MAX_RESULTS", 1))

def iso_duration_to_seconds(duration_str):
    try:
        from isodate import parse_duration
        return int(parse_duration(duration_str).total_seconds())
    except Exception:
        return 0

def fetch_video_details(video_ids):
    if not video_ids:
        return []

    params = {
        "part": "snippet,contentDetails,statistics",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(YOUTUBE_VIDEO_DETAILS_URL, params=params)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error fetching video details: {e}")
        return []

    detailed_videos = []
    for item in response.json().get("items", []):
        video_id = item["id"]
        snippet = item.get("snippet", {})
        content_details = item.get("contentDetails", {})
        stats = item.get("statistics", {})

        duration_seconds = iso_duration_to_seconds(content_details.get("duration", "PT0S"))
        if duration_seconds < 60 or duration_seconds > 600:
            print(f"⏩ Skipping {video_id} due to duration ({duration_seconds}s)")
            continue

        thumbnails = snippet.get("thumbnails", {})
        high_thumb = thumbnails.get("high")
        if not high_thumb:
            print(f"🖼️ Skipping {video_id} due to missing high resolution thumbnail")
            continue

        # Estimate resolution from thumbnail
        resolution = f'{high_thumb.get("width", "NA")}x{high_thumb.get("height", "NA")}'

        video_data = {
            "title": snippet.get("title"),
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
            "duration": duration_seconds,
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "resolution": resolution
        }
        detailed_videos.append(video_data)

    return detailed_videos

def search_youtube(query: str, max_results: int = MAX_RESULTS_PER_QUERY) -> list:
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoEmbeddable": "true",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"❌ YouTube API error for query '{query}': {e}")
        return []

    items = response.json().get("items", [])
    video_ids = [item["id"]["videoId"] for item in items if item.get("id", {}).get("videoId")]

    return fetch_video_details(video_ids)

def search_many(queries, max_results=MAX_RESULTS_PER_QUERY):
    all_results = []
    timestamp_loaded = datetime.now(timezone.utc).isoformat()

    for i, query in enumerate(queries[:MAX_QUERIES]):
        print(f"🔍 Searching for: {query}")
        vids = search_youtube(query, max_results=max_results)
        for rank, video in enumerate(vids):
            video["query_used"] = query
            video["timestamp_loaded"] = timestamp_loaded
            video["llm_rank"] = i + 1
            video["youtube_rank"] = rank + 1
        all_results.extend(vids)

    return pd.DataFrame(all_results)

# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def enrich_with_llm(title, description=""):
#     prompt = f"""
# Given the following YouTube title and description, identify:

# 1. The artist name(s)
# 2. The genre
# 3. Whether the sample likely includes: isolated drums, vocals, both, or neither
# 4. Decade song was released, using the format "1970s", "1980s", etc.

# Respond with JSON like:
# {{
#   "artist": "artist name",
#   "genre": "genre name",
#   "sample_type": "drums | vocals | both | neither"
#   "decade": "decade"
# }}

# Title: {title}
# Description: {description}
# """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7
#         )
#         text = response.choices[0].message.content
#         return json.loads(text)
#     except Exception as e:
#         print(f"⚠️ LLM enrichment failed: {e}")
#         return {"artist": "", "genre": "", "sample_type": "", "decade": ""}