from sqlalchemy.orm.attributes import flag_modified

from profile_service import profile_db as database
from user_follow import UserFollow


def add_new_following(follow_id: int, new_following_id: int):
    follow_data: UserFollow = get_follow_by_id(follow_id)
    if new_following_id in follow_data.following:
        return {"message": "ID:{} already exist in ID:{} following list.".format(new_following_id, follow_id)}
    follow_data.following.append(new_following_id)
    flag_modified(follow_data, "following")
    database.session.merge(follow_data)
    database.session.commit()
    database.session.refresh(follow_data)
    if new_following_id in follow_data.following:
        return {"message": "Successfully add ID:{} to ID:{} following list.".format(new_following_id, follow_id)}
    return {"message": "Fail to add ID:{} to ID:{} following list.".format(new_following_id, follow_id)}


def remove_following(follow_id: int, remove_id: int):
    follow_data: UserFollow = get_follow_by_id(follow_id)
    if remove_id not in follow_data.following:
        return
    follow_data.following.remove(remove_id)
    flag_modified(follow_data, "following")
    database.session.merge(follow_data)
    database.session.commit()
    return {"message": "Finish remove ID:{} from ID:{} following list".format(remove_id, follow_id)}


def add_new_follower(follow_id: int, new_follower_id: int):
    follow_data: UserFollow = get_follow_by_id(follow_id)
    if new_follower_id in follow_data.following:
        return {"message": "ID:{} already exist in ID:{} follower list.".format(new_follower_id, follow_id)}
    follow_data.follower.append(new_follower_id)
    flag_modified(follow_data, "follower")
    database.session.merge(follow_data)
    database.session.commit()
    database.session.refresh(follow_data)
    if new_follower_id in follow_data.follower:
        return {"message": "Successfully add ID:{} to ID:{} follower list.".format(new_follower_id, follow_id)}
    return {"message": "Fail to add ID:{} to ID:{} follower list.".format(new_follower_id, follow_id)}


def remove_follower(follow_id: int, remove_id: int):
    follow_data: UserFollow = get_follow_by_id(follow_id)
    if remove_id not in follow_data.follower:
        return
    follow_data.follower.remove(remove_id)
    flag_modified(follow_data, "follower")
    database.session.merge(follow_data)
    database.session.commit()
    return {"message": "Finish remove ID:{} from ID:{} follower list".format(remove_id, follow_id)}


def get_follow_by_id(follow_id: int) -> UserFollow:
    return database.session.query(UserFollow).filter_by(id=follow_id).first()
