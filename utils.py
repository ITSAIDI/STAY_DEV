############################ Generating Queries
import itertools

def generateQueries():
    sujets = ["autosuffisance", "permaculture", "potager en autonomie", "maraîchage bio", "agriculture durable"]
    actions = ["comment faire", "techniques", "astuces", "conseils", "expérience"]
    cultures = ["tomates", "pommes de terre", "blé", "arbres fruitiers", "poules"]
    techniques = ["paillage", "compostage", "engrais naturels", "rotation des cultures"]

    combinaisons = list(itertools.product(sujets, actions, cultures + techniques))
    requêtes = [" ".join(comb) for comb in combinaisons]
    return requêtes
 
############################ Scraping

from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import scrapetube
  
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








