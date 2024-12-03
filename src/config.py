import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": 'localhost',                  #BANNED WHILE WORKING WITH DOCKER   os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT")
}