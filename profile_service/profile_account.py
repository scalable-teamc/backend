from profile_service import profile_db as database


class UserProfile(database.Model):
    __tablename__ = 'profile'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String())
    uid = database.Column(database.Integer())
    display_name = database.Column(database.String())
    description = database.Column(database.Text())
    follower = database.Column(database.ARRAY(database.Integer), default="{}")
    following = database.Column(database.ARRAY(database.Integer), default="{}")
    post_id_archive = database.Column(database.ARRAY(database.Integer), default="{}")

    def __init__(self, uid, username, display_name, description):
        self.uid = uid
        self.username = username
        self.display_name = display_name
        self.description = description
