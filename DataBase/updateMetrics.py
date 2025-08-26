import psycopg
from googleapiclient.discovery import build
import sys
from datetime import date
from tqdm import tqdm

POSTGRE_PASSWORD = sys.argv[1]
YOUTUBE_API_KEY  = sys.argv[2]


conn = psycopg.connect(
    dbname="youtubestay",
    user="postgres",
    password=POSTGRE_PASSWORD,
    host="localhost",
    port="5432"
)

cur = conn.cursor()
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def CloseConnection():
    cur.close()
    conn.close()

def getVideosMetrics(batchVideoIds):
    
    # maximum of 50 video IDs per request    
    # costs 1 unit per call, regardless of how many video IDs
    
    resultats = []
    todayDate = date.today().isoformat()
    
    try:
        response = youtube.videos().list(
            part="statistics",
            id=",".join(batchVideoIds)  
        ).execute()

        for video in response.get("items", []):
            stats = video["statistics"]
            resultats.append({
                "id_video": video["id"],
                "date_releve_video": todayDate,
                "nombre_vues": int(stats.get("viewCount", 0)),
                "nombre_likes": int(stats.get("likeCount", 0)) if "likeCount" in stats else None
            })

    except Exception as e:
        print(f"Erreur while featching videos metrics: {e}")

    return resultats

def getChanneslMetrics(batchChannelIds):
    
    # maximum is 50 channel IDs per request
    # costs 1 unit per call, regardless of how many channel IDs
    
    resultats = []
    todayDate = date.today().isoformat()
    
    response = youtube.channels().list(
        part='statistics',
        id=",".join(batchChannelIds) 
    ).execute()
    try:
        for channel in response.get("items", []):
                stats = channel["statistics"]
                resultats.append({
                    "id_chaine": channel["id"],
                    "date_releve_chaine": todayDate,
                    "nombre_vues_total": int(stats.get("viewCount", 0)),
                    "nombre_abonnes_total": int(stats.get('subscriberCount', 0)),
                    'nombre_videos_total':int(stats.get('videoCount', 0))
                })
    except Exception as e:
        print(f"Erreur while featching videos metrics: {e}")

    return resultats

        
def getVideosDatabase():
    cur.execute("SELECT id_video FROM videos;")
    videosIds = [row[0] for row in cur.fetchall()]
    return videosIds

def getChannelDatabase():
    cur.execute("SELECT id_chaine FROM chaines WHERE pertinente = true;")
    channelsIds = [row[0] for row in cur.fetchall()]
    return channelsIds

def updateVideosMetrics():
    videosIds = getVideosDatabase()
    all_results = []

    # process in chunks of 50
    for i in tqdm(range(0, len(videosIds), 50),  desc="Fetching video metrics"):
        batch = videosIds[i:i+50]
        batch_results = getVideosMetrics(batch)
        all_results.extend(batch_results)
        
    # Save to Database
    for m in all_results:
        cur.execute("""
                INSERT INTO videos_metriques (id_video, date_releve_video, nombre_vues, nombre_likes)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_video, date_releve_video) DO NOTHING
            """, (m["id_video"], m["date_releve_video"], m["nombre_vues"], m["nombre_likes"]))
        
    # Commit Changes
    conn.commit()

def updateChannelsMetrics():
    channelsIds = getChannelDatabase()
    all_results = []

    # process in chunks of 50
    for i in tqdm(range(0, len(channelsIds), 50),  desc="Fetching channels metrics"):
        batch = channelsIds[i:i+50]
        batch_results = getChanneslMetrics(batch)
        all_results.extend(batch_results)
        
    # Save to Database
    for m in all_results:
        cur.execute("""
                    INSERT INTO chaines_metriques (id_chaine, date_releve_chaine,nombre_vues_total, nombre_abonnes_total, nombre_videos_total)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id_chaine, date_releve_chaine) DO NOTHING
                """, (m['id_chaine'],m['date_releve_chaine'],m['nombre_vues_total'],m['nombre_abonnes_total'],m['nombre_videos_total']))
        
    # Commit Changes
    conn.commit()



#testVideos = ['--0UsZzb0rQ','--4CMODK4SE']
#print(getVideosMetrics(testVideos))

#testChannels = ['UCVQeGg4Fdrrr8vDXa7yjOYg','UCSKdJoK73RLL-zOs4Sq_tTQ']
#print(getChanneslMetrics(testChannels))

#print(updateChannelsMetrics()[:3])

updateChannelsMetrics()

updateVideosMetrics()

CloseConnection()



