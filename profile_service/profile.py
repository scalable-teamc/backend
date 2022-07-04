import io

from storage import MINIO_CLIENT
import os
import base64


# Take picture and save to minio
def save_avatar(username_bucket, image_file, ctype):

    img = base64.b64decode(bytes(image_file, 'utf-8'))
    ext = '.' + ctype.split('/')[1]
    size = len(img)
    img = io.BytesIO(img)

    # Save profile picture to MINIO
    MINIO_CLIENT.put_object(bucket_name=username_bucket, object_name=username_bucket + "_avatar" + ext, data=img,
                            length=size, content_type=ctype)

    return "Picture saved to Minio"

# Get username's avatar from Minio
# def get_avatar_file(username_bucket):
#
#     # Get picture from MINIO
#     image_64 = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=username_bucket + "_avatar")
#     image_64_decode = base64.b64decode(image_64)
#
#     return image_64_decode
