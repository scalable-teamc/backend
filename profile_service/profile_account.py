from profile_service import profile_db as database


class UserProfile(database.Model):
    __tablename__ = 'profile'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    uid = database.Column(database.Integer())
    display_name = database.Column(database.String())
    description = database.Column(database.Text())

    def __init__(self, uid, display_name, description):
        self.uid = uid
        self.display_name = display_name
        self.description = description

