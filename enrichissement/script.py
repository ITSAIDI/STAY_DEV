import psycopg
import json
import os
import sys
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

def openJson(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Global variables

jsonfile = sys.argv[1]
data = openJson(jsonfile)

# Connect to youtubstay

conn = psycopg.connect(
    dbname="youtubestay",
    user="postgres",
    password=os.getenv("POSTGRE_PASSWORD"),
    host="localhost",
    port="5432"
)


cur = conn.cursor()

def labelExist(label):
    cur.execute("""
      SELECT label FROM entites_spatiales; 
        """)
    rows = cur.fetchall()
    for row in rows:
        if row[0]==label:
            return True
    return False

def generateId():
    cur.execute("""
      SELECT count(*) FROM entites_spatiales; 
        """)
    rows = cur.fetchall()
    count = rows[0][0]
    return f'es{count+1}'
    
def getEntityID(label):
    if labelExist(label):
        cur.execute("SELECT id_entite_spatiale FROM entites_spatiales WHERE label = %s;", (label,))
        rows = cur.fetchall()
        return rows[0][0]
    return generateId()

def updateTables():
    for video in tqdm(data):
        if 'output' in video:
            for entity in video['output']:
                entId = getEntityID(entity['ent'])
            
                if labelExist(entity['ent'])==False:
                    cur.execute("insert into entites_spatiales values (%s, %s, %s, %s)",(entId, entity['ent'], entity['lat'], entity['lon']))
                    
                cur.execute("insert into entites_spatiales_videos values (%s, %s) ON CONFLICT DO NOTHING",(entId, video['id_video']))
    
                     
#print(labelExist('paris'))
#print(generateId())
#print(getEntityID('paris'))


updateTables()

#print(len(data))


conn.commit()
cur.close()
conn.close()






