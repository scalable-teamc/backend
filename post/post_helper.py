from . import MINIO_CLIENT
import base64
import io
from . import MINIO_CLIENT


def save_image(username_bucket, postID, image_file, ctype):
    if ctype == "":
        return

    img = base64.b64decode(bytes(image_file, 'utf-8'))
    ext = '.' + ctype.split('/')[1]
    size = len(img)
    img = io.BytesIO(img)

    # Save image to MINIO. Image name will be <postID>_image.ext
    MINIO_CLIENT.put_object(bucket_name=username_bucket, object_name=postID + "_image" + ext, data=img, length=size,
                            content_type=ctype)
    return ext
    # return username_bucket, postID, image_file, ctype


# Helper function for get_api() and recent_api()
def get_image(username_bucket, postID):
    content = ""
    content_type = ""
    # Get picture from MINIO
    for obj in MINIO_CLIENT.list_objects(bucket_name=username_bucket, prefix=str(postID) + "_image"):
        if obj is None:
            return None
        pic = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=obj.object_name)
        content = base64.b64encode(pic.read()).decode('utf-8')
        ext = obj.object_name.split('.')[1]
        # content_type = "data:" + obj.content_type + ";base64,"
        content_type = "data:" + ext + ";base64,"
    return content_type + content
    # return str(username_bucket) + "_IMAGEIMAGE"