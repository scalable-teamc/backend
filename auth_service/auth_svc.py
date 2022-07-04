from flask_login import login_user

from storage import MINIO_CLIENT
from . import user_db as database
from .user_account import UserAccount


def authenticate(username: str, password: str):
    if not username or not password:
        return {"success": False, "message": "Username or Password is empty"}
    if not user_exist(username):
        return {"success": False, "message": "User:{} does not exist".format(username)}
    user: UserAccount = get_user_by_username(username)
    if user and user.verify_password(password):
        login_user(user)
        return {"success": True, "message": "Successfully Login as {}".format(username)}
    return {"success": False, "message": "Login Fail"}


def register(username: str, password: str):
    if user_exist(username):
        return {"success": False, "message": "User:{} already exist".format(username)}
    new_user = UserAccount(username, password)
    database.session.add(new_user)
    database.session.commit()
    if user_exist(username):
        MINIO_CLIENT.make_bucket(str(new_user.id))
        return {"success": True, "message": f"User {username} has been created successfully."}
    return {"success": False, "message": f" Fail to create User {username}."}


def user_exist(username: str):
    return database.session.query(UserAccount.id).filter_by(username=username).first() is not None


def get_user_by_id(user_id: int) -> UserAccount:
    return database.session.query(UserAccount).filter_by(id=user_id).first()


def get_user_by_username(username: str) -> UserAccount:
    return database.session.query(UserAccount).filter_by(username=username).first()
