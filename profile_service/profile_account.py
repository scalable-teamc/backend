from profile_service import profile_db as database


class UserProfile(database.Model):
    __tablename__ = 'profile'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    display_name = database.Column(database.String())
    description = database.Column(database.Text())

    def __init__(self, display_name, description):
        self.display_name = display_name
        self.description = description

