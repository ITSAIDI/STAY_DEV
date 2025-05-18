import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    dbname="mydatabase",
    user="postgres",
    password=os.getenv("POSTGRE_PASSWORD"),
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE chaines (
        id_chaine TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        bio TEXT,
        localisation CHAR(2),
        categorie_chaine TEXT,
        date_creation DATE NOT NULL,
        pertinente BOOLEAN
    )
""")

cur.execute("""
    CREATE TABLE videos (
        id_video TEXT PRIMARY KEY,
        titre TEXT NOT NULL,
        description TEXT,
        date_publication DATE NOT NULL,
        categorie_video TEXT,
        duree INTEGER,
        miniature TEXT,
        langue CHAR(2),
        transcription TEXT,
        tags TEXT[],
        requetes TEXT[],
        id_chaine TEXT REFERENCES chaines(id_chaine)
    )
""")

cur.execute("""
    CREATE TABLE chaines_metriques (
        id_chaine TEXT REFERENCES chaines(id_chaine),
        date_releve_chaine DATE NOT NULL,
        nombre_vues_total INTEGER,
        nombre_abonnes_total INTEGER,
        nombre_videos_total INTEGER,
        PRIMARY KEY (id_chaine, date_releve_chaine)
    )
""")

cur.execute("""
    CREATE TABLE videos_metriques (
        id_video TEXT REFERENCES videos(id_video),
        date_releve_video DATE NOT NULL,
        nombre_vues  INTEGER,
        nombre_likes INTEGER,
        PRIMARY KEY (id_video, date_releve_video)
    )
""")

cur.execute("""
    CREATE TABLE mentions (
        id_chaine TEXT REFERENCES chaines(id_chaine),
        id_video TEXT REFERENCES videos(id_video),
        mention_titre BOOLEAN ,
        mention_tags BOOLEAN ,
        mention_description BOOLEAN ,
        PRIMARY KEY (id_chaine, id_video)
    )
""")


cur.execute("""
    CREATE TABLE utilisateurs (
        id_utilisateur TEXT PRIMARY KEY,
        nom_utilisateur TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE commentaires (
        id_commentaire TEXT PRIMARY KEY,
        contenu TEXT NOT NULL,
        date_commentaire DATE NOT NULL,
        id_video TEXT REFERENCES videos(id_video),
        id_utilisateur TEXT REFERENCES utilisateurs(id_utilisateur),
        id_commentaire_parent TEXT REFERENCES commentaires(id_commentaire)
    )
""")


conn.commit()
cur.close()
conn.close()
