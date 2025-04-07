import json
import requests
from tqdm import tqdm

# Charger les données JSON depuis le fichier
with open("../jsons/echantillon.json", "r", encoding="utf-8") as f:
    echantillon = json.load(f)

# Clé API YouTube Data (remplacer par la vôtre)
api_key = "AIzaSyC7fRtrFt_eykZpSSBVg-o6q9EWBFR3Wiw"

# Fonction pour obtenir le nom de la chaîne à partir de l'ID
def get_channel_name(channel_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data and data['items']:
        return data['items'][0]['snippet']['title']
    else:
        return None  # Si aucun résultat trouvé pour l'ID de la chaîne

# Collecter les IDs des chaînes
channel_ids = {video['id_chaine'] for video in echantillon}

# Créer un dictionnaire pour stocker les noms des chaînes
channel_names = {}

# Utilisation de tqdm pour afficher une barre de progression
for channel_id in tqdm(channel_ids, desc="Récupération des noms de chaînes", unit="chaîne"):
    name = get_channel_name(channel_id, api_key)
    if name:
        channel_names[channel_id] = name
    else:
        channel_names[channel_id] = "Nom non trouvé"  # Si le nom n'est pas trouvé

# Sauvegarder les noms des chaînes dans un fichier JSON
with open("../jsons/channel_names.json", "w", encoding="utf-8") as f:
    json.dump(channel_names, f, ensure_ascii=False, indent=4)

print("Les noms des chaînes ont été sauvegardés dans 'channel_names.json'")
