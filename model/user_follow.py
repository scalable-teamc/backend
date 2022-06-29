from sqlalchemy.dialects.postgresql import ARRAY

from model import database


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

    def add_follower(self, new_follower_id):
        self.follower += [new_follower_id]

    def add_following(self, new_following_id):
        self.following += [new_following_id]
