import json
from collections import defaultdict

with open("../jsons/videosF1.json", "r", encoding="utf-8") as f:
    videos = json.load(f)

lang_count = defaultdict(int)

for video in videos:
    lang = video.get("langue", "unknown")
    lang_count[lang] += 1

print(f"Nombre total de vidéos : {len(videos)}\n")
print("Répartition par langue :")
for lang, count in lang_count.items():
    print(f"{lang} : {count}")
