from minio import Minio

# ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
# SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"
# MINIO_URL = os.environ.get("MINIO_URL")

MINIO_CLIENT = Minio(MINIO_API_HOST, access_key="admin", secret_key="password", secure=False)