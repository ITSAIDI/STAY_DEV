import json

with open('../jsons/shorts.json', "r", encoding="utf-8") as f:
    shorts_without_links = json.load(f)
    
print(len(shorts_without_links))