from utils import generateQueries,scrapeDetailsAll
import json

queries = generateQueries()
#videosData = searchYoutube(queries[0],max_results=2)

#print(queries[0])
#print(json.dumps(videosData,indent=4,ensure_ascii=False))
#searchYoutube("Filtre Berkey")
#print(queries[:2])
#results = scrapeDetailsAll(queries[:2])
#print(json.dumps(results,indent=3,ensure_ascii=False))
scrapeDetailsAll(queries)












