import json
from langdetect import detect
from tqdm import tqdm
from colorama import Style,Fore

def RefineLanguage1():
    with open("../../collecting/jsons/videos.json", "r", encoding="utf-8") as file:
        videos = json.load(file)
        
    for video in tqdm(videos,'refining the language...'):
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
   
    
def RefineLanguage2():
    with open("../jsons/videosR1.json", "r", encoding="utf-8") as file:
        videosF1 = json.load(file)
    with open("../../collecting/jsons/channels.json", "r", encoding="utf-8") as file:
        channels = json.load(file)
    
    ################### Channels Countries dictionary
    channels_countries = {}
    for channel in tqdm(channels,'channels-countries...'):
        channels_countries[channel['id_chaine']]= channel['localisation']
     
    ################## Refine the language with the country Code if existent
    for video in tqdm(videosF1,'Refining language...'):
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
       json.dump(videosF1, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)