from dotenv import load_dotenv
import os

load_dotenv()

START_URL = os.getenv("START_URL")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")
SCRAPE_TIME = os.getenv("SCRAPE_TIME")
DUMP_TIME = os.getenv("DUMP_TIME")
