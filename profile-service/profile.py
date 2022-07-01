import os

from minio import Minio

# ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
# SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')

MINIO_API_HOST = "http://localhost:9000"
# MINIO_URL = os.environ.get("MINIO_URL")

# MINIO_CLIENT = Minio(MINIO_URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
MINIO_CLIENT = Minio(MINIO_API_HOST, access_key="admin", secret_key="password", secure=False)

# generate bucket of avatar
found = MINIO_CLIENT.bucket_exists("avatar")
if not found:
    MINIO_CLIENT.make_bucket("avatar")


def save_avatar(image, name, bucket):

    # Save profile picture to MINIO
    MINIO_CLIENT.fget_object(bucket_name=bucket, object_name=image, file_path=image)

    if not os.path.exists("images"):
        os.mkdir("images")

    MINIO_CLIENT.fput_object("avatar", object_name=name + ".png", file_path="images/" + name + ".png",
                             content_type="image/png")
    try:
        os.remove("images/" + name + ".png")
    except:
        pass


# def set_avatar(image, bucket):
#
#     MINIO_CLIENT.fget_object("avatar", )
