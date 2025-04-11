import requests
from bs4 import BeautifulSoup

# The WhoSampled sample detail page
url = "https://www.whosampled.com/sample/1023/MF-DOOM-Rhymes-Like-Dimes-Quincy-Jones-James-Ingram-One-Hundred-Ways/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Request and parse the page
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# DEBUG: save the raw HTML to check in browser if needed
with open("whosampled_debug.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

def get_track_info(section):
    try:
        title = section.select_one('.trackName').text.strip()
        artist = section.select_one('.trackArtist').text.strip()
        return title, artist
    except AttributeError:
        return "Unknown", "Unknown"

try:
    left_section = soup.select_one("div.sampleEntryLeft")
    right_section = soup.select_one("div.sampleEntryRight")

    if not left_section or not right_section:
        raise Exception("Could not find sampleEntryLeft or sampleEntryRight")

    # Extract track info
    left_title, left_artist = get_track_info(left_section)
    right_title, right_artist = get_track_info(right_section)

    # Extract sample appearance times
    left_time = left_section.select_one(".trackTimes")
    left_time_text = left_time.text.strip() if left_time else "Unknown"

    right_time = right_section.select_one(".trackTimes")
    right_time_text = right_time.text.strip() if right_time else "Unknown"

    # Output results
    print("🔁 Sampling Song:", left_title, "by", left_artist)
    print("➡️  Sample Appears At:", left_time_text)
    print("🎵 Sampled Song:", right_title, "by", right_artist)
    print("⬅️  Sample Appears At:", right_time_text)

except Exception as e:
    print("❌ Error parsing page:", str(e))