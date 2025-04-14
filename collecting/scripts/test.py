import json 

with open("../../jsons/channels.json", "r", encoding="utf-8") as f:
    vidoes = json.load(f)
    
print(len(vidoes))    