import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from minio import Minio
from auth_service import auth_controller, auth_app, auth_svc, user_account
import os

url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ[
    "POSTGRES_PASSWORD"] + "@" + os.environ["POSTGRES_DB"] + "/user_db"
db_engine = sqlalchemy.create_engine(url)
if not database_exists(db_engine.url):
    create_database(db_engine.url)

user_db = SQLAlchemy()

ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')

# MINIO_API_HOST = "localhost:9000"
MINIO_URL = os.environ.get("MINIO_URL")

MINIO_CLIENT = Minio(MINIO_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)