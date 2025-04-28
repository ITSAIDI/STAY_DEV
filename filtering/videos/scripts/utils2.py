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

   
############### Refining Channels

from geopy.geocoders import Nominatim
from gliner import GLiNER

NER = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
geolocator = Nominatim(user_agent="geoapi")

labels = [
    "Localisation",
    "Ville",
    "Commune",
    "Pays",
    "Zone géographique",
    "Continent",
    "Région",
    "Département",
    "Code postal",
    "Quartier",
    "Adresse",
    "Lieu-dit",
    "Coordonnées GPS",
    "Latitude",
    "Longitude",
    "Territoire",
    "Aire urbaine",
    "Espace rural",
    "Zone rurale",
    "Zone urbaine",
    "Périmètre géographique",
    "Localité",
]

def getNer(context):
    locations = []
    results =  NER.predict_entities(context, labels)
    if results :
        for result in results :
            if result['score'] > 0.5 :
                locations.append(result['text'])
    return locations

def getGeocoding(locations):
    countries = []
    details = {}
    try :
        for location in locations:
            Adresse = geolocator.geocode(location, language='fr', addressdetails=True, timeout=10)  
            if Adresse and "country_code" in Adresse.raw['address']:
                code = Adresse.raw['address']['country_code'].upper()
                countries.append(code)
                details[location]=code
            #time.sleep(1)  # respecter la limite Nominatim     
        return countries,details
    except:
        print("Error with GeoCoding")
        time.sleep(1)
        return countries,details

def countRepetitions(countries):
    counts = Counter()
    for country in countries:  
        counts[country] +=1
    return counts 

def getVidoesdata(channelId,videos):
    context = ''
    for video in videos:
        if video['id_chaine']==channelId:
            context += video['titre_video']+'\n'
            context += video['description']+'\n'
    return context

def findCountry(locations):
    countries,details = getGeocoding(locations)
    #print("countries ",countries)
    if len(countries)>0:
        if len(countries) == 1:
            return countries[0],details
        else :
            counts = countRepetitions(countries)
            return counts.most_common(1)[0][0],details
    return '',details

def RefineChannel(channel,videos):

    locationsChannel_1 = getNer(channel['nom_chaine']+'\n'+channel['bio'])
    #print("locationsChannel_1",locationsChannel_1)

    if len(locationsChannel_1)>0:
        channelLocation,details = findCountry(locationsChannel_1)  
        return channelLocation,details
    else :
        context = getVidoesdata(channel['id_chaine'],videos)
        locationsChannel_2 = getNer(context)
        #print("locationsChannel_2 ",locationsChannel_2)
        if len(locationsChannel_2)>0:

            channelLocation,details = findCountry(locationsChannel_2) 
            return channelLocation,details
        else:
            return '',{}
    
def RefineAllChannels():

    channels_location_Unknown = openJson("../jsons/channels_location_Unknown.json")
    videos = openJson("../../collecting/jsons/videos.json")
    temp = 0
    for channel in tqdm(channels_location_Unknown,"Channels-Locations Refining..."):
        start = time.time()
        channelLocation,details = RefineChannel(channel,videos)
        end = time.time()
        channel['localisation']=channelLocation
        channel['localisation_details']= details
        channel['localisationTime(s)'] = end-start
       
        temp+=1
        
        if temp >= 100:
            saveJson("../jsons/channels_location_Unknown.json",channels_location_Unknown)
            temp = 0

    saveJson("../jsons/channels_location_Unknown.json",channels_location_Unknown)

