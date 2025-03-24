from utils import generateQueries,searchYoutube
import json

queries = generateQueries()
videosData = searchYoutube(queries[0],max_results=2)

print(queries[0])
print(json.dumps(videosData,indent=4,ensure_ascii=False))
#searchYoutube("Filtre Berkey")
















