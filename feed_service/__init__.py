# import sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_utils import create_database, database_exists
#
# db_engine = sqlalchemy.create_engine("postgresql://postgres:password@localhost:5432/feed_db")
# if not database_exists(db_engine.url):
#     create_database(db_engine.url)
#
# feed_db = SQLAlchemy()