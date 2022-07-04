from app import app
from storage import MINIO_CLIENT
import os
import base64


# Take picture and save to minio
def save_avatar(image_file, username_bucket):

    image = open(image_file, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)

    # Save profile picture to MINIO
    MINIO_CLIENT.put_object(username_bucket, object_name=username_bucket + "_avatar", data=image_64_encode)

    return "Picture saved to Minio"


# Get username's avatar from Minio
def get_avatar_file(username_bucket):

    # Get picture from MINIO
    image_64 = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=username_bucket + "_avatar")
    image_64_decode = base64.b64decode(image_64)

    return image_64_decode

