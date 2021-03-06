from datetime import datetime, timedelta
from flask import current_app, jsonify
from flask_login import login_user
from auth_init import user_db as database
from auth_init import MINIO_CLIENT
from user_account import UserAccount
import jwt


def authenticate(username: str, password: str):
    if not username or not password:
        return {"success": False, "message": "Username or Password is empty"}
    if not user_exist(username):
        return {"success": False, "message": "User:{} does not exist".format(username)}
    user: UserAccount = get_user_by_username(username)
    if user and user.verify_password(password):
        login_user(user)
        token = jwt.encode({
            'id': user.id,
            'sub': username,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
            current_app.config['SECRET_KEY'])
        return {"success": True, "uid": user.id, "message": "Successfully Login as {}".format(username),
                'token': token}
    return {"success": False, "message": "Login Fail"}


def register(username: str, password: str):
    if user_exist(username):
        return {"success": False, "message": "User:{} already exist".format(username)}
    new_user = UserAccount(username, password)
    database.session.add(new_user)
    database.session.commit()
    database.session.refresh(new_user)
    if user_exist(username):
        MINIO_CLIENT.make_bucket(username)
        return {"success": True, "uid": new_user.id, "message": f"User {username} has been created successfully."}
    return {"success": False, "message": f" Fail to create User {username}."}


def remove_user(username: str):
    if not user_exist(username):
        return {"success": True, "message": "User not exist"}
    database.session.query(UserAccount).filter_by(username=username).delete()
    database.session.commit()
    if not user_exist(username):
        return {"success": True, "message": "Removed User:{}".format(username)}
    return {"success": False, "message": "Fail to remove User:{}".format(username)}


def user_exist(username: str):
    return database.session.query(UserAccount.id).filter_by(username=username).first() is not None


def get_user_by_id(user_id: int) -> UserAccount:
    return database.session.query(UserAccount).filter_by(id=user_id).first()


def get_user_by_username(username: str) -> UserAccount:
    return database.session.query(UserAccount).filter_by(username=username).first()


def get_id_by_token(token):
    invalid_msg = {
        'message': 'Invalid token. Registeration and / or authentication required',
        'authenticated': False
    }
    expired_msg = {
        'message': 'Expired token. Reauthentication required.',
        'authenticated': False
    }
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
        user = get_user_by_username(data['sub'])
        if not user:
            return 'user not found'
        return {'uid': user.id, 'username': user.username, 'success': True}
    except jwt.ExpiredSignatureError:
        return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
    except (jwt.InvalidTokenError, Exception) as e:
        print(e)
        return jsonify(invalid_msg), 401
