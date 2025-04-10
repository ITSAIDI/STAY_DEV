import json 

with open("../../jsons/channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)
    
print(len(channels))    