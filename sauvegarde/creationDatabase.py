import psycopg
import os
from dotenv import load_dotenv

load_dotenv()


# Connexion à PostgreSQL (à la base par défaut, souvent 'postgres')
conn = psycopg.connect(
    dbname="postgres",
    user="postgres",
    password=os.getenv("POSTGRE_PASSWORD"),
    host="localhost", 
    port="5432"           
)

conn.autocommit = True
cur = conn.cursor()
nom_base = "myDatabase"
cur.execute(f"CREATE DATABASE {nom_base}")
cur.close()
conn.close()

print(f"Base de données '{nom_base}' créée avec succès.")













