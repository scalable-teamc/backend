from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy

from model.user_account import UserAccount

database = SQLAlchemy()


def authenticate(username: str, password: str):
    if not username or not password:
        return False
    user: UserAccount = database.session.query(UserAccount).filter_by(username=username).first()
    if user and user.verify_password(password):
        login_user(user)
        return {"message": "Successfully Login as {}".format(username)}
    return {"message": "Login Fail"}


def register(username: str, password: str):
    new_user = UserAccount(username, password)
    database.session.add(new_user)
    database.session.commit()
    if user_exist(username):
        return {"message": f"User {new_user.username} has been created successfully."}
    return {"message": f" Fail to create User {new_user.username}."}


def user_exist(username: str):
    return database.session.query(UserAccount.id).filter_by(username=username).first() is not None
