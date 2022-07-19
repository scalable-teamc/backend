from feed_init import feed_db as database
from feed_db import Feed, Online
from datetime import datetime


# Function for Online Table
def add_online(uid: int, sid: str):
    # online_data = get_online_by_uid(uid)
    # if online_data is None:
    user = Online(uid, sid)
    database.session.add(user)
    database.session.commit()

    return "Added"


# Function for Online Table
def remove_online(sid: int):
    online_data = get_online_by_sid(sid)
    if online_data:
        database.session.query(Online).filter_by(sid=sid).delete()
        database.session.commit()

    return "Deleted"


# Function for Online Table
def get_online_by_sid(sid: int):
    return database.session.query(Online).filter_by(sid=sid).first()


def get_online_by_uid(uid: int):
    return database.session.query(Online).filter_by(uid=uid).all()


# Function for Feed Table
def add_feed(uid: int, post_id: int, date: datetime):
    post = Feed(uid, post_id, date)
    database.session.add(post)
    database.session.commit()
    return "Feed added"


# Function for Feed Table
def remove_feed(uid: int):
    feed_data = get_feed_by_uid(uid)
    if feed_data:
        database.session.query(Feed).filter_by(uid=uid).delete()
        database.session.commit()

    return "Feed Deleted"


# Function for Feed Table
def get_feed_by_uid(uid: int, offset: int):
    return database.session.query(Feed).filter_by(uid=uid).order_by(Feed.date.desc()).limit(10).offset(offset).all()
