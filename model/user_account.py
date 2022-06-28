from app import database


class UserAccount(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(), unique=True)
    password = database.Column(database.String())

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<Username: {self.username}>"
