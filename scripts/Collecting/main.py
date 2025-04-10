from utils import scrapeVideos
import json
from tqdm import tqdm

with open("../jsons/queries.json", "r", encoding="utf-8") as file:
    queries = json.load(file)
  
  
for query in tqdm(queries['4'],desc='scraping youtube...',unit='query'):
    scrapeVideos(query,12)
    

       











