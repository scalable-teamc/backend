from app import app
from storage import MINIO_CLIENT
import os

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
