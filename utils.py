############################ Generating Queries
import itertools

def generateQueries():
    sujets = ["autosuffisance", "permaculture", "potager en autonomie", "maraîchage bio", "agriculture durable"]
    cultures = ["tomates", "pommes de terre", "blé", "arbres fruitiers", "poules"]
    techniques = ["paillage", "compostage", "engrais naturels", "rotation des cultures"]

    combinaisons = list(itertools.product(sujets, cultures + techniques))
    requêtes = [" ".join(comb) for comb in combinaisons]
    return requêtes
 

 
############################ Scraping

from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
import scrapetube
from tqdm import tqdm
import json

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
    
    
########################### Keywords augmentation 
from dotenv import load_dotenv
from openai import OpenAI
import os
import time

endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("GITHUB_TOKEN"),
)

def scrapeDetailsOne(query,max_results = 5):
    "Get the videos details (title, description)"
    #print(query)
    videos_details = {}
    
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    )
    response = request.execute()
    for item in response['items']:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        ################## Get the description with videos function
        video_request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()
        if video_response["items"]:
            description = video_response["items"][0]["snippet"]["description"]
            
        if len(description)>0: # Keep only videos with description
          videos_details[video_id] = {'title':title,'description':description,'query':query,'id':video_id}
    
    return videos_details

def scrapeDetailsAll(queries):
    "Run the scrapeDetailsOne throw all the queries"
    scrape = []
    for query in tqdm(queries, desc="Scraping en cours", unit="requête"):
        videosDetails = scrapeDetailsOne(query)
        scrape.extend(videosDetails.values())
        
    ################### Save in json file
    
    with open('scrape.json', "w", encoding="utf-8") as f:
        json.dump(scrape, f, ensure_ascii=False, indent=4)

def Prompter(descriptions,titles):
    system_prompt = """
        Vous êtes un expert en autosuffisance et autonomie (alimentaire, énergétique, en eau, etc.).
        Vous recevez en entrée des titres et descriptions de vidéos YouTube obtenus à partir de requêtes telles que :
        ['autosuffisance tomates', 'maraîchage bio poules', 'potager en autonomie tomates', ...].

        ## Types de mots-clés :

        - **Mots-clés primaires** : Essentiels pour la recherche YouTube mais insuffisants seuls. Ils doivent être combinés avec des mots-clés secondaires pour obtenir des résultats pertinents.
        - **Mots-clés secondaires** : Termes qui ne doivent pas être utilisés seuls dans les recherches YouTube sur l'autosuffisance, sous peine d'obtenir des vidéos hors sujet.

        ## Exemples de mots-clés :

        - **Primaires** : autosuffisance, autonomie alimentaire, autonomie énergétique, autonomie en eau, vie en autarcie, habitats autonomes...
        - **Secondaires** : potager, filtre Berkey, permaculture, filtre Doulton, poêle à bois bouilleur, poêle de masse, cuve eau pluie, maison terre-paille, maison torchis, ferme en pierre, maraîchage, culture en lasagnes, aquaponie...

        ## Votre mission :

        1. **Extraire** les mots-clés primaires et secondaires présents dans les titres et descriptions fournis.
        2. **Retourner la réponse structuré comme suit :
        {
            "Primaire": [],
            "Secondaire": []
        }
        
    - Tous les mots-clés extraits doivent être en minuscules.
      """
    try :
        response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Titres des vidéos : {titles}\nDescriptions des vidéos : {descriptions}"},
        ],
        temperature=0.7,  
        top_p=1.0,
        max_tokens=500,  
        model=model_name
        )
        return  response
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def Batching():
    ################# Read the scrape.json
    with open("scrape.json", "r", encoding="utf-8") as f:
      scrapeData = json.load(f)
         
    ################ Process in batch of 4
    batchs = []
    for i in range(0, len(scrapeData), 4):
        batch = scrapeData[i:i+4]  

        ##### Extract and concatenate titles and descriptions
        titles = "  ##############  ".join(item["title"] for item in batch)
        descriptions = "  ######################  ".join(item["description"] for item in batch)

        batchs.append({"titles": titles, "descriptions": descriptions})
    
    ################### Save in json file
    with open('scrapeBatches.json', "w", encoding="utf-8") as f:
        json.dump(batchs, f, ensure_ascii=False, indent=4)

def Updating(NewVoc):
    
    with open("vocabulary.json", "r", encoding="utf-8") as file:
       data = json.load(file)
       
    ################### Filtring
    for keyword in NewVoc['Primaire']:
        if keyword not in data['Primaire'] and keyword not in data['Secondaire']:
            data['Primaire'].append(keyword)
            
    for keyword in NewVoc['Secondaire']:
        if keyword not in data['Primaire'] and keyword not in data['Secondaire']:
            data['Secondaire'].append(keyword)
    
    print('\n  New Voc :  ',NewVoc)
    print(f"\n len(Secondaire) :{len(data['Secondaire'])}") 
    print(f"\n len(Primaire)   :  {len(data['Primaire'])}")
    
    ################ Saving       
    with open("vocabulary.json", "w", encoding="utf-8") as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
    
       
def getExtensions():
    ################# Read the json
    with open("scrapeBatches.json", "r", encoding="utf-8") as f:
      batchs = json.load(f)
         
    ################ Prompter
    nbrRequestes = 0
    for batch in tqdm(batchs,desc="Augmenting...", unit="batch"):
        llmResponse = Prompter(batch['descriptions'],batch['titles'])
        if llmResponse:
            json_string = llmResponse.choices[0].message.content
            newVoc = json.loads(json_string)
            Updating(newVoc)
            nbrRequestes+=1
            if nbrRequestes == 10:
                print('----------------Sleeping for 60s ...')
                time.sleep(60)
                nbrRequestes=0
        else :
            print('---------Empty Chatgpt response')
            

   
    
#getExtensions()    
#Filtring()


