import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
import os
url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ[
    "POSTGRES_PASSWORD"] + "@" + os.environ["POSTGRES_DB"] + "/feed_db"

db_engine = sqlalchemy.create_engine(url)
if not database_exists(db_engine.url):
    create_database(db_engine.url)

feed_db = SQLAlchemy()