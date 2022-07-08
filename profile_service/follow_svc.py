from sqlalchemy.orm.attributes import flag_modified

from profile_service import profile_db as database
from user_follow import UserFollow


def add_new_following(user_id: int, new_following_id: int) -> dict:
    follow_data: UserFollow = get_follow_by_user_id(user_id)
    if new_following_id in follow_data.following:
        return {"success": False,
                "message": "ID:{} already exist in ID:{} following list.".format(new_following_id, user_id)}
    follow_data.following.append(new_following_id)
    flag_modified(follow_data, "following")
    database.session.merge(follow_data)
    database.session.commit()
    database.session.refresh(follow_data)
    if new_following_id in follow_data.following:
        return {"success": True,
                "message": "Successfully add ID:{} to ID:{} following list.".format(new_following_id, user_id)}
    return {"success": False, "message": "Fail to add ID:{} to ID:{} following list.".format(new_following_id, user_id)}


def remove_following(user_id: int, remove_id: int) -> dict:
    follow_data: UserFollow = get_follow_by_user_id(user_id)
    if remove_id not in follow_data.following:
        return {"success": True}
    follow_data.following.remove(remove_id)
    flag_modified(follow_data, "following")
    database.session.merge(follow_data)
    database.session.commit()
    return {"success": True, "message": "Finish remove ID:{} from ID:{} following list".format(remove_id, user_id)}


def add_new_follower(user_id: int, new_follower_id: int) -> dict:
    follow_data: UserFollow = get_follow_by_user_id(user_id)
    if new_follower_id in follow_data.following:
        return {"success": False,
                "message": "ID:{} already exist in ID:{} follower list.".format(new_follower_id, user_id)}
    follow_data.follower.append(new_follower_id)
    flag_modified(follow_data, "follower")
    database.session.merge(follow_data)
    database.session.commit()
    database.session.refresh(follow_data)
    if new_follower_id in follow_data.follower:
        return {"success": True,
                "message": "Successfully add ID:{} to ID:{} follower list.".format(new_follower_id, user_id)}
    return {"success": False, "message": "Fail to add ID:{} to ID:{} follower list.".format(new_follower_id, user_id)}


def remove_follower(user_id: int, remove_id: int) -> dict:
    follow_data: UserFollow = get_follow_by_user_id(user_id)
    if remove_id not in follow_data.follower:
        return {"success": True}
    follow_data.follower.remove(remove_id)
    flag_modified(follow_data, "follower")
    database.session.merge(follow_data)
    database.session.commit()
    return {"success": True, "message": "Finish remove ID:{} from ID:{} follower list".format(remove_id, user_id)}


def get_follow_by_user_id(user_id: int) -> UserFollow:
    return database.session.query(UserFollow).filter_by(user_id=user_id).first()
