import json
from tqdm import tqdm
from colorama import Style,Fore
from collections import Counter
import time

def openJson(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def saveJson(path,data):
    with open(path, "w", encoding="utf-8") as f:
       json.dump(data, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)

############### Refining 1

from langdetect import detect

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
  
def RefineLanguage3():
    with open("../jsons/videosR1.json", "r", encoding="utf-8") as file:
        videosR1 = json.load(file)
    with open("../jsons/channelsR1.json", "r", encoding="utf-8") as file:
        channelsR1 = json.load(file)
    
    ################### Channels Countries dictionary
    channels_countries = {}
    for channel in channelsR1:
        channels_countries[channel['id_chaine']]= channel['localisation']
     
    ################## Refine the language with the country Code if existent
    for video in tqdm(videosR1,'Refining3...'):
        if video['langue'] == 'fr':  
            channelId = video['id_chaine']
            try:
                country = channels_countries[channelId]
                if country:
                    video['langue']+=f'-{country}'
            except:
                print(Style.BRIGHT+Fore.YELLOW+f"\n probleme while refining video: {video['id_video']}"+Style.RESET_ALL)
                
    ################## Save the New json file
    with open("../jsons/videosR3.json", "w", encoding="utf-8") as f:
       json.dump(videosR1, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)
   
  