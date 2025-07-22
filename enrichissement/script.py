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

conn = psycopg.connect(
    dbname="youtubestay",
    user="postgres",
    password=os.getenv("POSTGRE_PASSWORD"),
    host="localhost",
    port="5432"
)


cur = conn.cursor()








