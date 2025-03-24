from utils import generateQueries,search_youtube,search_scrapetube
import json

queries = generateQueries()

print(queries[2])
#response = search_youtube(queries[2])
response = search_scrapetube(queries[2])
print(json.dumps(response,indent=4,ensure_ascii=False))
#print(" \n Description :",response['items'][0]['snippet']['description'])



















