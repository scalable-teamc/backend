import hashlib

from app import database
from model.user_account import UserAccount


def authenticate(username: str, password: str) -> bool:
    if not username or not password:
        return False
    db_user: UserAccount = database.session.query(UserAccount).filter_by(username=username).first()
    if db_user and compare_password(password, db_user.password):
        print("Successfully Login as {}".format(username))
        return True
    return False


def compare_password(input_password: str, db_hash_password: str) -> bool:
    input_hash_password = hashlib.md5(input_password.encode()).hexdigest()
    return input_hash_password == db_hash_password


def register(username: str, password: str):
    hash_password = hashlib.md5(password.encode()).hexdigest()
    new_user = UserAccount(username, hash_password)
    database.session.add(new_user)
    database.session.commit()
    if database.session.query(UserAccount.id).filter_by(username=username).first() is not None:
        return {"message": f"User {new_user.username} has been created successfully."}
    return {"message": f" Fail to create User {new_user.username}."}
