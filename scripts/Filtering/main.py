import json

with open('../../jsons/videos.json', "r", encoding="utf-8") as f:
    videos = json.load(f)
    
print(len(videos))