from flask_login import login_user
from storage import MINIO_CLIENT

from model import database
from model.user_account import UserAccount
from model.user_follow import UserFollow


def authenticate(username: str, password: str):
    if not username or not password:
        return False
    if not user_exist(username):
        return {"message": "User:{} does not exist".format(username)}
    user: UserAccount = get_user_by_username(username)
    if user and user.verify_password(password):
        login_user(user)
        return {"message": "Successfully Login as {}".format(username)}
    return {"message": "Login Fail"}


def register(username: str, password: str):
    if user_exist(username):
        return {"message": "User:{} already exist".format(username)}
    new_follow_data = UserFollow()
    database.session.add(new_follow_data)
    database.session.commit()
    database.session.refresh(new_follow_data)
    follow_id = new_follow_data.id
    new_user = UserAccount(username, password, follow_id)
    database.session.add(new_user)
    database.session.commit()
    if user_exist(username):
        MINIO_CLIENT.make_bucket(username)
        return {"message": f"User {username} has been created successfully."}
    return {"message": f" Fail to create User {username}."}


def user_exist(username: str):
    return database.session.query(UserAccount.id).filter_by(username=username).first() is not None


def get_user_by_id(user_id: int) -> UserAccount:
    return database.session.query(UserAccount).filter_by(id=user_id).first()


def get_user_by_username(username: str) -> UserAccount:
    return database.session.query(UserAccount).filter_by(username=username).first()
