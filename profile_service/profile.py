import io

from storage import MINIO_CLIENT
from profile_service import profile_db as database
from profile_account import UserProfile
from sqlalchemy.orm.attributes import flag_modified
import os
import base64


# Take picture and save to minio
def save_avatar(username_bucket, image_file, ctype):

    if ctype == "":
        return

    img = base64.b64decode(bytes(image_file, 'utf-8'))
    ext = '.' + ctype.split('/')[1]
    size = len(img)
    img = io.BytesIO(img)

    # Save profile picture to MINIO
    MINIO_CLIENT.put_object(bucket_name=username_bucket, object_name= username_bucket +
                            "_avatar" + ext, data=img, length=size, content_type=ctype)

    return ext


# Get username's avatar from Minio
def get_avatar(username_bucket):

    pic = None
    # Get picture from MINIO
    for obj in MINIO_CLIENT.list_objects(bucket_name=username_bucket, prefix=username_bucket):
        base_64 = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=obj.object_name)
        pic = base64.b64encode(base_64.read()).decode('utf-8')

    return pic


def add_display_name(user_id: int, display_name: str):

    profile_data: UserProfile = get_profile_by_id(user_id)
    profile_data.display_name.append(display_name)
    flag_modified(profile_data, "display_name")
    database.session.merge(profile_data)
    database.session.commit()
    database.session.refresh(profile_data)

    return {"message": "New display name display_name:[] is added".format(display_name)}


def add_description(user_id: int, description: str):

    profile_data: UserProfile = get_profile_by_id(user_id)
    profile_data.description.append(description)
    flag_modified(profile_data, "description")
    database.session.merge(profile_data)
    database.session.commit()
    database.session.refresh(profile_data)

    return {"message": "New description description:[] is added".format(description)}


def get_profile_by_id(profile_id: int) -> UserProfile:
    return database.session.query(UserProfile).filter_by(id=profile_id).first()


def get_display_name(profile_id: int):
    return database.session.query(UserProfile.display_name).filter_by(id=profile_id).first()


def get_description(profile_id: int):
    return database.session.query(UserProfile.description).filter_by(id=profile_id).first()


