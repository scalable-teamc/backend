import uuid
from datetime import datetime

from . import database


class PasteModel(database.Model):
    postID = database.Column(database.String(40), primary_key=True, default=str(uuid.uuid1()))
    userID = database.Column(database.String(40))
    mediaID = database.Column(database.String(40))
    content = database.Column(database.String())
    createdAt = database.Column(database.DateTime(), nullable=False, default=datetime.utcnow()) # .now()

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID" : self.postID,
            "userID" : self.userID,
            "mediaID" : self.mediaID,
            "content" : self.content,
            "createdAt" : str(self.createdAt)
        }

