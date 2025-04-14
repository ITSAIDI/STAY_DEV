import json
from langdetect import detect
from tqdm import tqdm
from colorama import Style,Fore

def filterByLanguage():
    with open("../collecting/jsons/videos.json", "r", encoding="utf-8") as file:
        videos = json.load(file)
        
    for video in tqdm(videos,'refining the language...'):
        try:
            lg = detect(video['titre_video'])
            if lg == 'fr':
                video['langue'] = 'fr'
            else:
                video['langue'] = 'autre'
        except:
            print(Style.BRIGHT+Fore.YELLOW+f"Detection failed for video : {video['id_video']}"+Style.RESET_ALL)
            
    with open("./jsons/videosF1.json", "w", encoding="utf-8") as f:
       json.dump(videos, f, ensure_ascii=False, indent=2)
       print(Style.BRIGHT+Fore.GREEN+'json saved'+Style.RESET_ALL)
       
    