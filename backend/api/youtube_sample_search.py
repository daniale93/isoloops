import os
import requests
import pandas as pd
from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# 🎯 Search query for sample-worthy content
SEARCH_QUERY = "percussion intro"  # Try: "vocal intro", "drum break", etc.

# 🎛 Other config
MAX_RESULTS = 10

def search_youtube(query, max_results=10):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": max_results,
        "videoEmbeddable": "true"
    }

    res = requests.get(url, params=params)
    res.raise_for_status()
    results = res.json()

    videos = []
    for item in results.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        description = item["snippet"]["description"]
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            "title": title,
            "channel": channel,
            "description": description,
            "youtube_url": youtube_url,
            "video_id": video_id,
            "search_query": query
        })

    return pd.DataFrame(videos)

# 🔍 Run search
df = search_youtube(SEARCH_QUERY, MAX_RESULTS)
print(df[["title", "channel", "youtube_url"]])

# 💾 Save to CSV for future tagging
df.to_csv("youtube_sample_candidates.csv", index=False)
print("✅ Saved to youtube_sample_candidates.csv")