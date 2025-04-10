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
from colorama import Fore, Style, init

load_dotenv() 
init()
   
youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY2"))

#--> Videos
  
def getvideo_details(video_id):
    request = youtube.videos().list(part='snippet,contentDetails', id=video_id)
    response = request.execute()
    videoMetadata = {
        'id_video': response['items'][0]['id'],
        'id_chaine':response['items'][0]['snippet']['channelId'],
        'titre_video': response['items'][0]['snippet']['title'],
        'description':response['items'][0]['snippet']['description'],
        'date_publication':response['items'][0]['snippet']['publishedAt'],
        'duree': response['items'][0]['contentDetails']['duration'],
        'miniature':'',
        'tags':'',
        'langue':'',
        'youtubeCategorie':response['items'][0]['snippet']['categoryId'],
    }
    
    ################# get the highest resolution thumbnail
    resolution_order = ["maxres", "standard", "high", "medium", "default"]
    for res in resolution_order:
        if res in response['items'][0]['snippet']['thumbnails']:
            videoMetadata['miniature']= response['items'][0]['snippet']['thumbnails'][res]['url']
            break
    
    if 'tags' in response['items'][0]['snippet']:
        videoMetadata['tags']= response['items'][0]['snippet']['tags']
        
    if 'defaultAudioLanguage'in response['items'][0]['snippet']:
        videoMetadata['langue']= response['items'][0]['snippet']['defaultAudioLanguage']
        
    return videoMetadata

def getVidoesId(listVideos):
    ids = []
    for videoDic in listVideos:
        ids.append(videoDic['id_video'])
    return ids 
   
def updateVideos(videosMetadata):
    
    print(Style.BRIGHT + Fore.GREEN + '\n Updating...')
    
    with open("../jsons/videos.json", "r", encoding="utf-8") as file:
        videos = json.load(file)
        ids = getVidoesId(videos)
                
    if len(videos) == 0:
        videos.extend(videosMetadata)
    else:
        for video in videosMetadata:
            id = video['id_video']
            query = video['requete'][0]
            if id in ids:
                ###### Select the video dicionary by using the id
                videoDicionary = videos[ids.index(id)]
                videoDicionary['requete'].append(query)
            else:
                videos.append(video)
                   
    ################ Saving       
    with open("../jsons/videos.json", "w", encoding="utf-8") as f:
        print(Style.BRIGHT + Fore.YELLOW + f'\n Actual Nbr videos : {len(videos)}')
        print(Style.BRIGHT + Fore.GREEN + '\n Saving videos...')
        json.dump(videos, f, ensure_ascii=False, indent=2) 
        
def scrapeVideos(query,max_results):
    print(Style.BRIGHT + Fore.GREEN + '\nScraping Videos...')
    ############################## Scrapetube
    videoIds = []
    searchResults = list(scrapetube.get_search(query,limit=max_results,sort_by='relevance',results_type='video'))
    for result in searchResults:
        videoIds.append(result['videoId'])
        
    ############################## Youtube API
    videosMetadata = []
    for videoid in videoIds:
        videodata = getvideo_details(videoid)
        videodata['requete']=[query]
        videosMetadata.append(videodata)
    
    ############################## Update the json
    updateVideos(videosMetadata) 

    print(Style.RESET_ALL)

#--> Channels

def getChannnelsId(videosList):
    Ids = set()
    for video in videosList:
        Ids.add(video['id_chaine'])
    return Ids

def getchannel_details(channel_id):
    request = youtube.channels().list(part='snippet,contentDetails', id=channel_id)
    response = request.execute()    
    channelMetadata = {
        'id_chaine' : response['items'][0]['id'],
        'nom_chaine' :response['items'][0]['snippet']['title'],
        'bio':response['items'][0]['snippet']['description'],
        'date_creation' :response['items'][0]['snippet']['publishedAt'],
        'type_monetisation' :'',
        'details_monetisation' :''
    }
    return channelMetadata
      
def updateChannels(channelMetadata):
    pass

def scrapeChannels():
    with open('../../jsons/videos.json', "r", encoding="utf-8") as f:
        vidoes = json.load(f)
    channelIds = getChannnelsId(vidoes)
    print(len(channelIds))

scrapeChannels()
#--> Statistics

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
            
########################### Constructing queries 

def vocBatching(n_groups=4):
    
    with open("../jsons/Voc.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    secondary_keywords = data["Secondaire"]
    groups = {str(i+1): secondary_keywords[i::n_groups] for i in range(n_groups)}
    updated_data = {
    "Primaire": data["Primaire"],
    "Secondaire": groups
      } 
    ################ Saving       
    with open("../jsons/Voc.json", "w", encoding="utf-8") as f:
       json.dump(updated_data, f, ensure_ascii=False, indent=2)  

def getQueries(batchId):
    with open("../jsons/Voc.json", "r", encoding="utf-8") as file:
        Vocabulary = json.load(file)
    with open("../jsons/queries.json", "r", encoding="utf-8") as file:
        Queries = json.load(file)
        
    Queries[batchId] = []
    for pkeyword in Vocabulary['Primaire']:
        for skeyword in Vocabulary['Secondaire'][batchId]:
            query  = f'{pkeyword} {skeyword}'
            Queries[batchId].append(query)
            
    ############### Upsdate Queries json file
    with open("../jsons/queries.json", "w", encoding="utf-8") as f:
       json.dump(Queries, f, ensure_ascii=False, indent=2)  

