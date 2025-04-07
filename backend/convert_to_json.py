import pandas as pd

df = pd.read_csv("backend/data/sample_scope_songs.csv")
df.to_json("frontend/src/data/songs.json", orient="records", indent=2)
print("✅ JSON file created at frontend/src/data/songs.json")