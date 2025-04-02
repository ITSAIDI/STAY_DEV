from dotenv import load_dotenv
from openai import OpenAI
import os
import json


load_dotenv()


endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("GITHUB_TOKEN"),
)

with open("scrape.json", "r", encoding="utf-8") as f:
    data = json.load(f) 

print(len(data))
print(data[20])

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
2. **Retourner la réponse au format dictionaire python** structuré comme suit :
{
    "Primaires": [],
    "Secondaires": []
}
"""

"""
response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Titres des vidéos : {Titles}\nDescriptions des vidéos : {Descriptions}"},
    ],
    temperature=0.7,  
    top_p=1.0,
    max_tokens=500,  
    model=model_name
)

json_output = response.choices[0].message.content
parsed_data = json.loads(json_output)

# Now `parsed_data` is a Python dictionary
print(parsed_data)  # Full dictionary
print(parsed_data["Primaires"])  # Access "Primaires"
print(parsed_data["Secondaires"])  # Access "Secondaires"
"""