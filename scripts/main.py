from utils import searchYoutube
import json

with open("../jsons/queries.json", "r", encoding="utf-8") as file:
    queries = json.load(file)
    
    
results = searchYoutube(queries['1'][0],max_results=1)  
#print(json.dumps(results,indent=2,ensure_ascii=False))
       











