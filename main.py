from utils import generateQueries,search_youtube
import json

queries = generateQueries()
response = search_youtube(queries[0])
print(json.dumps(response,indent=4))
print(queries[0])



















