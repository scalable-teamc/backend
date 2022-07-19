# import sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy_utils import create_database, database_exists
# from minio import Minio
#
# db_engine = sqlalchemy.create_engine("postgresql://postgres:password@localhost:5432/postgres")
# if not database_exists(db_engine.url):
#     create_database(db_engine.url)
#
# post_db = SQLAlchemy()
#
# # ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
# # SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
#
# MINIO_API_HOST = "localhost:9000"
# # MINIO_URL = os.environ.get("MINIO_URL")
#
# MINIO_CLIENT = Minio(MINIO_API_HOST, access_key="admin", secret_key="password", secure=False)