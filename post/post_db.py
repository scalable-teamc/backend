from post import post_db as db
from datetime import datetime
from post_app import app


class PasteModel(db.Model):
    postID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer())
    username = db.Column(db.String())
    likedUser = db.Column(db.ARRAY(db.Integer))
    content = db.Column(db.String())
    createdAt = db.Column(db.DateTime(), nullable=False, default=datetime.now)  # .now()

    # Return as dict to be send over HTTP response
    def to_dict(self):
        return {
            "postID": self.postID,
            "userID": self.userID,
            "username": self.username,
            "likedUser": self.likedUser,
            "content": self.content,
            "createdAt": self.createdAt
        }


@app.before_first_request
def create_tables():
    db.create_all()