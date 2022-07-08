import base64
import io

from sqlalchemy.orm.attributes import flag_modified

from profile_account import UserProfile
from profile_service import profile_db as database
from storage import MINIO_CLIENT


# Take picture and save to minio
def save_avatar(username_bucket, image_file, ctype):
    if ctype == "":
        return

    img = base64.b64decode(bytes(image_file, 'utf-8'))
    ext = '.' + ctype.split('/')[1]
    size = len(img)
    img = io.BytesIO(img)

    # Save profile picture to MINIO
    MINIO_CLIENT.put_object(bucket_name=username_bucket, object_name=username_bucket +
                                                                     "_avatar" + ext, data=img, length=size,
                            content_type=ctype)

    return ext


# Get username's avatar from Minio
def get_avatar(username_bucket):
    content = ""
    content_type = ""
    # Get picture from MINIO
    for obj in MINIO_CLIENT.list_objects(bucket_name=username_bucket, prefix=username_bucket):
        if obj is None:
            return ""
        pic = MINIO_CLIENT.get_object(bucket_name=username_bucket, object_name=obj.object_name)
        content = base64.b64encode(pic.read()).decode('utf-8')
        ext = obj.object_name.split('.')[1]
        # content_type = "data:" + obj.content_type + ";base64,"
        content_type = "data:" + ext + ";base64,"
    return content_type + content


def add_profile(user_id: int, username: str, display_name: str, description: str):
    profile_data = get_profile_by_id(user_id)
    if profile_data is None:
        user = UserProfile(user_id, username, display_name, description)
        database.session.add(user)
        database.session.commit()
    else:
        profile_data.display_name = display_name
        profile_data.description = description
        flag_modified(profile_data, "display_name")
        flag_modified(profile_data, "description")
        database.session.merge(profile_data)
        database.session.commit()
        database.session.refresh(profile_data)

    return "New Profile is added"


def add_new_following(user_id: int, new_following_id: int) -> dict:
    profile: UserProfile = get_profile_by_id(user_id)
    if new_following_id in profile.following:
        return {"success": False,
                "message": "ID:{} already exist in ID:{} following list.".format(new_following_id, user_id)}
    profile.following.append(new_following_id)
    flag_modified(profile, "following")
    database.session.merge(profile)
    database.session.commit()
    database.session.refresh(profile)
    if new_following_id in profile.following:
        return {"success": True,
                "message": "Successfully add ID:{} to ID:{} following list.".format(new_following_id, user_id)}
    return {"success": False, "message": "Fail to add ID:{} to ID:{} following list.".format(new_following_id, user_id)}


def remove_following(user_id: int, remove_id: int) -> dict:
    profile: UserProfile = get_profile_by_id(user_id)
    if remove_id not in profile.following:
        return {"success": True}
    profile.following.remove(remove_id)
    flag_modified(profile, "following")
    database.session.merge(profile)
    database.session.commit()
    return {"success": True, "message": "Finish remove ID:{} from ID:{} following list".format(remove_id, user_id)}


def add_new_follower(user_id: int, new_follower_id: int) -> dict:
    profile: UserProfile = get_profile_by_id(user_id)
    if new_follower_id in profile.following:
        return {"success": False,
                "message": "ID:{} already exist in ID:{} follower list.".format(new_follower_id, user_id)}
    profile.follower.append(new_follower_id)
    flag_modified(profile, "follower")
    database.session.merge(profile)
    database.session.commit()
    database.session.refresh(profile)
    if new_follower_id in profile.follower:
        return {"success": True,
                "message": "Successfully add ID:{} to ID:{} follower list.".format(new_follower_id, user_id)}
    return {"success": False, "message": "Fail to add ID:{} to ID:{} follower list.".format(new_follower_id, user_id)}


def remove_follower(user_id: int, remove_id: int) -> dict:
    profile: UserProfile = get_profile_by_id(user_id)
    if remove_id not in profile.follower:
        return {"success": True}
    profile.follower.remove(remove_id)
    flag_modified(profile, "follower")
    database.session.merge(profile)
    database.session.commit()
    return {"success": True, "message": "Finish remove ID:{} from ID:{} follower list".format(remove_id, user_id)}


def get_profile_by_id(profile_id: int) -> UserProfile:
    return database.session.query(UserProfile).filter_by(uid=profile_id).first()


def get_display_name(profile_id: int):
    return database.session.query(UserProfile.display_name).filter_by(uid=profile_id).first()


def get_description(profile_id: int):
    return database.session.query(UserProfile.description).filter_by(uid=profile_id).first()


def find_by_username(username: str):
    return database.session.query(UserProfile).filter_by(username=username).first()
