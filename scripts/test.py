import json
from utils import scrapeVideos


with open("../jsons/videos.json", "r", encoding="utf-8") as file:
    videos = json.load(file)
    print(len(videos))
    
    
#scrapeVideos('autosuffisance',1)