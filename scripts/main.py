from utils import generateQueries,scrapeDetailsAll
import json

#queries = generateQueries()
#videosData = searchYoutube(queries[0],max_results=2)
#print(len(queries))
#print(queries)
#print(queries[:-3])
#print(json.dumps(videosData,indent=4,ensure_ascii=False))
#searchYoutube("Filtre Berkey")
#print(queries[:2])
#results = scrapeDetailsAll(queries[:2])
#print(json.dumps(results,indent=3,ensure_ascii=False))
#scrapeDetailsAll(queries)
"""
with open("scrape.json", "r", encoding="utf-8") as f:
    scrapeData = json.load(f)
    print(len(scrapeData))
    print(scrapeData[0])
"""
with open("Voc.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    print(len(data['Primaire']))
    print(len(data['Secondaire']))
       











