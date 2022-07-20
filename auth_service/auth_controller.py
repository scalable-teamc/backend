from functools import wraps

from flask import Blueprint, request

from auth_svc import *

auth_controller = Blueprint('auth_controller', __name__)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization')

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        try:
            token = auth_headers[0]
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401  # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    return _verify


@auth_controller.route('/auth/register', methods=['POST'])
def register_post():
    data = request.json
    username = data['username']
    password = data['password']
    return register(username, password)


@auth_controller.route('/auth/login', methods=['POST'])
def login_post():
    credentials = request.json
    if credentials:
        username = credentials['username']
        password = credentials['password']
        return authenticate(username, password)


@token_required
@auth_controller.route('/auth/remove', methods=['DELETE'])
def user_delete():
    data = request.json
    username = data['username']
    return remove_user(username)


@token_required
@auth_controller.route('/auth/token', methods=['POST'])
def get_by_token():
    auth_headers = request.headers.get('Authorization')
    print(auth_headers)
    token = request.json['token']
    return get_id_by_token(token)

