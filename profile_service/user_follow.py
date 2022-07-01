from sqlalchemy.dialects.postgresql import ARRAY

from profile_service import profile_db as database


class UserFollow(database.Model):
    __tablename__ = 'follow'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    follower = database.Column(ARRAY(database.Integer()))
    following = database.Column(ARRAY(database.Integer()))

    def __init__(self):
        self.follower = []
        self.following = []

    def __repr__(self):
        return "follower IDs {}\nfollowing IDs {}".format(self.follower, self.following)
