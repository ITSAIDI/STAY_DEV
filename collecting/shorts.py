import json
from pathlib import Path
from tqdm import tqdm
from ast import literal_eval
from dotenv import load_dotenv
from openai import OpenAI
import os


endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("GITHUB_TOKEN"),
)

json_path = Path("../jsons/shorts_without_links_no_category.json")
batch_size = 4

with open(json_path, "r", encoding="utf-8") as f:
    shorts = json.load(f)


def build_context(batch):
    context = ""
    for i, short in enumerate(batch, start=1):
        context += f"#################### Short {i}\n"
        context += f"id  : {short['id_video']}\n"
        context += f"titre: {short['titre_video']}\n"
        context += f"decrition : {short['description']}\n"
    return context


def Prompter_shorts(context):
    system_prompt = """
        Vous êtes un expert en analyse de contenus YouTube Shorts. Votre tâche est de déterminer le type de chaque vidéo Short liée à l'autosuffisance, en vous basant uniquement sur le titre et la description. 

        Les catégories possibles sont :

        1. **Tutoriel** : Vidéo montrant étape par étape un processus ou une méthode liée à l'autosuffisance (ex : cultiver des légumes, installer un système de récupération d'eau de pluie, etc.).  
        2. **Vlog rapide** : Vidéo à caractère personnel ou expérimental, souvent de format informel, où le créateur partage son expérience ou ses réflexions sur l'autosuffisance.  
        3. **Short explicatif** : Vidéo concise qui explique un concept ou une idée clé de manière claire et didactique, souvent sans interaction personnelle.  
        4. **Autre** : Tout autre type de contenu qui ne correspond pas aux catégories ci-dessus. 

        Vous recevrez plusieurs vidéos à la fois. Pour chacune, analysez le **titre** et la **description** puis assignez-lui une **catégorie**.

        Retournez la réponse sous forme d’un dictionnaire JSON, comme ceci :

        {
            "id_video_1": "categorie",
            "id_video_2": "categorie",
            ...
        }
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            temperature=0.7,
            top_p=1.0,
            max_tokens=500,
            model=model_name
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

for i in tqdm(range(0, len(shorts), batch_size)):
    batch = shorts[i:i + batch_size]

    # Ne traiter que les vidéos sans catégorie
    if all("categorie" in short for short in batch):
        continue

    context = build_context(batch)
    raw_response = Prompter_shorts(context)

    if raw_response:
        try:
            predictions = literal_eval(raw_response)
            for short in batch:
                id_video = short["id_video"]
                if id_video in predictions:
                    short["categorie"] = predictions[id_video]
        except Exception as e:
            print(f"Erreur de parsing : {e}")
            print("Réponse brute :", raw_response)
            continue

        # Sauvegarde après chaque batch
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(shorts, f, ensure_ascii=False, indent=2)

print("\n✅ Traitement terminé. Fichier mis à jour en continu.")




