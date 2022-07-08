from sqlalchemy.dialects.postgresql import ARRAY

from profile_service import profile_db as database


class UserFollow(database.Model):
    __tablename__ = 'follow'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    user_id = database.Column(database.Integer, nullable=False)
    follower = database.Column(ARRAY(database.Integer()))
    following = database.Column(ARRAY(database.Integer()))

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.follower = []
        self.following = []

    def __repr__(self):
        return "follower IDs {}\nfollowing IDs {}".format(self.follower, self.following)
