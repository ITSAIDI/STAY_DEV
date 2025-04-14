import json
videos =[]
with open("./jsons/videosF1.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)