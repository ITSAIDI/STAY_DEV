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
            "lien_video": f"https://www.youtube.com/watch?v={video['videoId']}",
            "lien_chaine": f"https://www.youtube.com/channel/{video['longBylineText']['runs'][0]['navigationEndpoint']['browseEndpoint']['browseId']}",
            "durée": video["lengthText"]["simpleText"],
            "miniature": best_thumbnail["url"]
        }
        
        parsed_data.append(video_data)
    
    return parsed_data

def getvideo_description(video_id):
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        video_details = response['items'][0]['snippet']
        description = video_details.get('description', 'No description available')
        title = video_details.get('title', 'No title available')
        return description
    return None

def getchannel_details(channel_id):
    request = youtube.channels().list(part='snippet,contentDetails', id=channel_id)
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        channel_details = response['items'][0]
        bio = channel_details['snippet'].get('description', 'No bio available')
        creation_date = channel_details['snippet'].get('publishedAt', 'No creation date available')
        return  bio,creation_date
    return None

def searchYoutube(query,max_results=1):
    ############################## Scrapetube
    videos = list(scrapetube.get_search(query,limit=max_results,sort_by='relevance'))
    videosData = parseScrapetube(videos)
    
    ######################### Youtube API
    for videodata in videosData:
        videodata['description'] = getvideo_description(videodata['id_video'])
        videodata['bio'],videodata['date_creation'] = getchannel_details(videodata['id_chaine'])
    
    return videosData
    
    


