import requests
from dotenv import load_dotenv
import os

load_dotenv() 

url = "https://www.googleapis.com/youtube/v3/videoCategories"
params = {
    "part": "snippet",
    "regionCode": "FR", 
    "key": os.getenv("YOUTUBE_API_KEY")
}

response = requests.get(url, params=params)

if response.status_code == 200:
    categories = response.json().get("items", [])
    print("YouTube Video Categories in France:")
    for category in categories:
        category_id = category["id"]
        category_name = category["snippet"]["title"]
        print(f"{category_id}: {category_name}")
else:
    print("Error:", response.json())
