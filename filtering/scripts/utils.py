import json
from langdetect import detect
from tqdm import tqdm
from colorama import Style,Fore

############### Refining 1

def RefineLanguage1():
    with open("../../collecting/jsons/videos.json", "r", encoding="utf-8") as file:
        videos = json.load(file)
        
    for video in tqdm(videos,'Refining1...'):
        try:
            lg = detect((video['titre_video']+video['description']).lower())
            if lg == 'fr':
                video['langue'] = 'fr'
            else:
                video['langue'] = 'autre'
        except:
            try :
                lg = detect(video['description'])
                if lg == 'fr':
                    video['langue'] = 'fr'
                else:
                    video['langue'] = 'autre'
            except:
                print(Style.BRIGHT+Fore.YELLOW+f"\n Detection failed for video : {video['id_video']}"+Style.RESET_ALL)
            
    with open("../jsons/videosR1.json", "w", encoding="utf-8") as f:
       json.dump(videos, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)
  
############### Refining 2
  
def RefineLanguage2():
    with open("../jsons/videosR1.json", "r", encoding="utf-8") as file:
        videosR1 = json.load(file)
    with open("../../collecting/jsons/channels.json", "r", encoding="utf-8") as file:
        channels = json.load(file)
    
    ################### Channels Countries dictionary
    channels_countries = {}
    for channel in channels:
        channels_countries[channel['id_chaine']]= channel['localisation']
     
    ################## Refine the language with the country Code if existent
    for video in tqdm(videosR1,'Refining2...'):
        if video['langue'] == 'fr':  
            channelId = video['id_chaine']
            try:
                country = channels_countries[channelId]
                if country:
                    video['langue']+=f'-{country}'
            except:
                print(Style.BRIGHT+Fore.YELLOW+f"\n probleme while refining video: {video['id_video']}"+Style.RESET_ALL)
                
    ################## Save the New json file
    with open("../jsons/videosR2.json", "w", encoding="utf-8") as f:
       json.dump(videosR1, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)
   
   
############### Refining 3

from collections import Counter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time 
  
from tqdm import tqdm
from flair.models import SequenceTagger
from flair.data import Sentence

tagger = SequenceTagger.load("flair/ner-french")
geolocator = Nominatim(user_agent="geoapi")


def getContext(channelId,videos,channels):
    # Return the Channel Bio and Vidoes Descriptions+Titles from what we collect        
    for channel in channels:
        if channel['id_chaine']==channelId:
            bio = channel['bio']
    descriptions = []
    titles = []
    for video in videos:
        if video['id_chaine']==channelId:
           descriptions.append(video['description']) 
           titles.append(video['titre_video']) 
           
    context = f"Le bio de la chaine : \n {bio}"
    for des in descriptions:
        context+= f"""
        \n###############
        \nDescription : {des}
        """
    for tit in titles:
        context+= f"""
        \n###############\n
        titre : {tit}
        """
    return context

def getContextAll():
    with open("../../collecting/jsons/videos.json", "r", encoding="utf-8") as file:
        videos = json.load(file)
        
    with open("../../collecting/jsons/channels.json", "r", encoding="utf-8") as file:
        channels = json.load(file)
        
    with open("../jsons/videosfr.json", "r", encoding="utf-8") as file:
        videosfr = json.load(file)
    vidoesfrR3 = []
    for videofr in tqdm(videosfr):
        context = getContext(videofr['id_chaine'],videos,channels)
        vidoesfrR3.append(
              {
                'id_chaine':videofr['id_chaine'],
                'videofr_id':videofr['id_video'],
                'context':context
              }
            )
    with open("../jsons/videosfrR3.json", "w", encoding="utf-8") as f:
       json.dump(vidoesfrR3, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)
       print(Style.BRIGHT+Fore.YELLOW+f'\n json length is : {len(vidoesfrR3)}'+Style.RESET_ALL)
 
def getCountry(text):
    sentence = Sentence(text)
    tagger.predict(sentence)
    country_codes = Counter()
    entities_countries = {}
    
    for entity in sentence.get_spans('ner'):
        label = entity.get_label("ner")
        if label.value == "LOC" and label.score >= 0.6:
            try:
                location = geolocator.geocode(entity.text, language='fr', addressdetails=True, timeout=10)
                if location and "country_code" in location.raw['address']:
                    code = location.raw['address']['country_code'].upper()
                    country_codes[code] += 1
                    entities_countries[entity.text] = code
                time.sleep(1)  # respecter la limite Nominatim
            except GeocoderTimedOut:
                continue
            except Exception as e:
                print(f"Erreur avec '{entity.text}':", e)

    if country_codes:
        return country_codes.most_common(1)[0][0],entities_countries
    else:
        return 'unknown', {}
       
def RefineLanguage3():
    with open("../jsons/videosfrR3.json", "r", encoding="utf-8") as file:
        videosfrR3 = json.load(file)
    
    tempsave = 0 # For safety reason,in case the loop is breaked a temporary save is executed.
    
    for videofr in tqdm(videosfrR3):
        country,locations = getCountry(videofr['context'])
        videofr['country'] = country
        videofr['finded_locations'] = locations
        
        print(Style.BRIGHT+Fore.GREEN+ f'\n--{country}--\n'+Style.RESET_ALL)
        #print(locations)
        print(json.dumps(locations, indent=2, ensure_ascii=False))
        
        tempsave+=1
        if tempsave>=300 :
            with open("../jsons/videosfrR3.json", "w", encoding="utf-8") as f:
                json.dump(videosfrR3, f, ensure_ascii=False, indent=2)
                print(Style.BRIGHT+Fore.GREEN+ f'\n json saved --{tempsave}--'+Style.RESET_ALL)
            tempsave = 0
                
    with open("../jsons/videosfrR3.json", "w", encoding="utf-8") as f:
        json.dump(videosfrR3, f, ensure_ascii=False, indent=2)
        print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)
        print(Style.BRIGHT+Fore.YELLOW+f'\n json length is : {len(videosfrR3)}'+Style.RESET_ALL)
            