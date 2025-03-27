############################ Scraping

from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import scrapetube
import json

load_dotenv() 
   
youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

def search_youtube(query, max_results=1):
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()
    return response
  
def search_scrapetube(query, max_results=1):
    videos = scrapetube.get_search(query,limit=max_results,sort_by='relevance')
    return list(videos)

def getChannel_scrapetube(channelId):
    videos = scrapetube.get_channel(channelId)
    return list(videos)

import scrapetube
import json


channel_id = "UC7Q2CIsQreNeaMEeh0Gr_RQ"  # Replace with the actual LAPL YouTube channel ID

videos = list(scrapetube.get_channel(channel_id))
print(len(videos))
print(json.dumps(videos[0],indent=4))

