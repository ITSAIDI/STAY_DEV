import json
from langdetect import detect
from tqdm import tqdm
from colorama import Style,Fore
from searchAgent import main

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
    with open("../jsons/vidoesfrR3.json", "w", encoding="utf-8") as f:
       json.dump(vidoesfrR3, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'\n json saved'+Style.RESET_ALL)
       print(Style.BRIGHT+Fore.YELLOW+f'\n json length is : {len(vidoesfrR3)}'+Style.RESET_ALL)
 
       
def getLocation():
    # Pass throw the videosfr get the channelid --> getContext 
    # --> Context --> Gemini --> Country,Justification --> Save in vidoesfrR3.json
    # chnnelid,videoid,Context,Country,Justification (Only 5 fields)
    pass

