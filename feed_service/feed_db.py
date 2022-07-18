from feed_service import db as database
from datetime import datetime


class Online(database.Model):
    __tablename__ = 'online'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    uid = database.Column(database.Integer())
    sid = database.Column(database.String, unique=True)

    def __init__(self, uid, sid):
        self.uid = uid
        self.sid = sid


class Feed(database.Model):
    __tablename__ = 'feed'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    uid = database.Column(database.Integer())
    post_id = database.Column(database.Integer())
    date = database.Column(database.DateTime(), default=datetime.now)

    def __init__(self, uid, post_id, date):
        self.uid = uid
        self.post_id = post_id
        self.date = date
