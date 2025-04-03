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


def parseScrapetube(videos):
    parsed_data = []
    
    for video in videos:
        best_thumbnail = max(video['thumbnail']['thumbnails'], key=lambda x: x['width'])
        
        video_data = {
            "id_video": video["videoId"],
            "id_chaine": video["longBylineText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            "titre_video": video["title"]["runs"][0]["text"],
            "nom_chaine": video["longBylineText"]["runs"][0]["text"],
            "date_publication": video["publishedTimeText"]["simpleText"],
            "durée": video["lengthText"]["simpleText"],
            "miniature": best_thumbnail["url"]
        }
        
        parsed_data.append(video_data)
    
    return parsed_data

def getvideo_description(video_id):
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    
    print('Response :',json.dumps(response,indent=2,ensure_ascii=False))
    
    if 'items' in response and len(response['items']) > 0:
        video_details = response['items'][0]['snippet']
        description = video_details.get('description', 'No description available')
        return description
    return None
