from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import database


class UserAccount(UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer(), primary_key=True, autoincrement=True)
    username = database.Column(database.String(), unique=True, nullable=False)
    password = database.Column(database.String(), nullable=False)
    followID = database.Column(database.Integer(), nullable=False)

    def __init__(self, username: str, password: str, follow_id: int):
        self.username = username
        self.password = generate_password_hash(password)
        self.followID = follow_id

    def __repr__(self):
        return f"<Username: {self.username}>"

    def verify_password(self, password):
        return check_password_hash(self.password, password)
