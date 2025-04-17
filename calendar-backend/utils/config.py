from dotenv import load_dotenv
import os

load_dotenv(override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

URI = os.getenv("connection_string")
DB_NAME = os.getenv("db_name")
COLLECTION_NAME = os.getenv("collection_name")