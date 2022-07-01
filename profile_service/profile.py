from storage import MINIO_CLIENT


# Take picture and save to minio
def save_avatar(image_path, username_bucket):

    # Save profile picture to MINIO
    MINIO_CLIENT.fput_object(username_bucket, object_name=username_bucket + "_avatar", file_path=image_path
                             , content_type="image/jpg")

    return "Picture saved to Minio"


# Get username's avatar from Minio
def get_avatar_file(username_bucket):

    # Get picture from MINIO
    return MINIO_CLIENT.fget_object(bucket_name=username_bucket, object_name=username_bucket + "_avatar")

