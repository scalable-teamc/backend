import uuid
from datetime import datetime

from . import database


class PasteModel(database.Model):
    __tablename__ = 'posts'

    postID = database.Column(database.Integer(), primary_key=True, autoincrement=True)
    userID = database.Column(database.Integer(), autoincrement=True)
    mediaID = database.Column(database.Integer(), autoincrement=True)
    content = database.Column(database.String())
    createdAt = database.Column(database.DateTime(), nullable=False, default=datetime.utcnow()) # .utcnow() to store createdAt in a standard time. Display it as .now() for local time

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
            "mediaID" : self.mediaID,
            "content" : self.content,
            "createdAt" : self.createdAt
        }

