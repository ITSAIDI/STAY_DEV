import psycopg
import json
import os
from dotenv import load_dotenv
load_dotenv()


def openJson(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

jsonfile = './jsons/output.json'
data = openJson(jsonfile)
print(len(data))

# Connect to youtubstay

"""conn = psycopg.connect(
    dbname="youtubestay",
    user="postgres",
    password=os.getenv("POSTGRE_PASSWORD"),
    host="localhost",
    port="5432"
)


cur = conn.cursor()"""

import folium

location_data = {
        "lat": 49.5532646,
        "lon": 2.9392577,
        "ent": "ville"
      }

map_obj = folium.Map(location=[location_data["lat"], location_data["lon"]], zoom_start=13)

folium.Marker(
    [location_data["lat"], location_data["lon"]],
    popup=location_data["ent"],
    tooltip=location_data["ent"]
).add_to(map_obj)

map_obj.save("map_janze.html")









